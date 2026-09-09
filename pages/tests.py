import json
import re

from django.contrib.auth import get_user_model
from django.test import TestCase

from accommodation.models import PartnerHotel
from blog.models import Post
from bookings.models import Tour
from seo.models import FAQ, LocalPage, InternalLink
from services.models import Service
from testimonials.models import Testimonial
from utils import auto_link


class ParadiseDynamicSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = get_user_model().objects.create_user(username='guide')
        cls.tour = Tour.objects.create(
            name='Database Sunset Cruise', slug='database-sunset-cruise',
            description='A tour stored in the booking database.',
            location='Lake Naivasha', duration_hours='1.5',
            price_resident='3500', price_international='45', max_people=8,
            is_active=True, allow_indexing=True,
        )
        Service.objects.create(
            title='Dynamic Photography', slug='dynamic-photography',
            description='A service managed in the dashboard.',
            icon_class='fas fa-camera', is_active=True,
        )
        FAQ.objects.create(
            question='Is this FAQ dynamic?',
            plain_answer='Yes. It comes from the FAQ model.',
            answer='<p>Yes. It comes from the FAQ model.</p>',
            is_active=True, allow_indexing=True,
        )
        LocalPage.objects.create(
            title='Dynamic Destination', slug='dynamic-destination',
            primary_keyword='Lake Naivasha destination', location='Naivasha',
            content='<p>A destination managed in the dashboard.</p>',
            is_active=True, allow_indexing=True,
        )
        Post.objects.create(
            title='Dynamic Journal Guide', slug='dynamic-journal-guide',
            author=author, content='<p>A published guide.</p>',
            status='published', meta_description='A dynamic journal entry.',
        )
        Testimonial.objects.create(
            customer_name='Verified Guest', rating=5,
            testimonial_text='The lake was calm and beautiful.',
            tour=cls.tour, is_active=True,
        )
        PartnerHotel.objects.create(
            name='Dynamic Lakeside Stay', slug='dynamic-lakeside-stay',
            description='A stay managed in the dashboard.',
            location='South Lake', is_active=True,
        )

    def test_home_renders_model_content_and_dynamic_schema(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertEqual(html.count('<h1'), 1)
        for value in [
            'Mosety', 'Boat Rides', 'Naivasha',
            'Karagita', 'Crescent Island',
        ]:
            self.assertIn(value, html)

        schemas = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            html,
            flags=re.DOTALL,
        )
        self.assertTrue(len(schemas) >= 1)
        business = json.loads(schemas[0])
        self.assertIn('telephone', business)
        self.assertIn('name', business)
        self.assertIn('tel:+254114182706', html)
        self.assertIn('https://wa.me/254114182706', html)
        self.assertIn('114182706', html)

    def test_tour_routes_use_the_booking_model(self):
        list_response = self.client.get('/boat-rides/')
        self.assertEqual(list_response.status_code, 200)
        detail_response = self.client.get(self.tour.get_absolute_url(), follow=True)
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, self.tour.description)
        self.assertContains(detail_response, '5.0')

    def test_sitemaps_llms_and_internal_routes_remain_dynamic(self):
        sitemap = self.client.get('/sitemap.xml').content.decode()
        for path in [
            '/dynamic-destination/',
            '/blog/dynamic-journal-guide/', '/faq/', '/destinations/',
        ]:
            self.assertIn(path, sitemap)

        llms = self.client.get('/llms.txt')
        self.assertContains(llms, self.tour.name)

        robots = self.client.get('/robots.txt')
        self.assertNotContains(robots, 'Disallow: /destinations/')
        self.assertNotContains(robots, 'Disallow: /best-boat-rides-')
        self.assertEqual(self.client.get('/about/').status_code, 200)

    def test_brand_call_and_tour_internal_links_are_available(self):
        self.assertEqual(self.client.get('/prices/').status_code, 200)
        self.assertEqual(self.client.get('/safety/').status_code, 200)
        self.assertEqual(self.client.get('/journal/').status_code, 200)

