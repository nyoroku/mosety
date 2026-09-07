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
            'Database Sunset Cruise', 'Dynamic Photography',
            'Dynamic Journal Guide', 'Verified Guest',
            'Dynamic Lakeside Stay', 'Is this FAQ dynamic?',
        ]:
            self.assertIn(value, html)

        schemas = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            html,
            flags=re.DOTALL,
        )
        business, faq = [json.loads(schema) for schema in schemas]
        self.assertEqual(business['aggregateRating']['reviewCount'], 1)
        self.assertEqual(business['telephone'], '+254729360174')
        self.assertEqual(business['name'], 'Paradise Boat Rides Naivasha')
        self.assertIn('hasOfferCatalog', business)
        self.assertTrue(business['logo'].endswith('/static/images/paradise-logo.jpeg'))
        self.assertEqual(faq['mainEntity'][0]['name'], 'Is this FAQ dynamic?')
        self.assertIn('tel:+254729360174', html)
        self.assertIn('https://wa.me/254729360174', html)
        self.assertIn('0729360174', html)
        self.assertIn('/static/images/paradise-logo.jpeg', html)
        self.assertNotIn('brand-mark-image', html)
        self.assertNotIn('Memories on Water', html)

    def test_tour_routes_use_the_booking_model(self):
        list_response = self.client.get('/tours/')
        self.assertContains(list_response, self.tour.name)
        detail_response = self.client.get(self.tour.get_absolute_url(), follow=True)
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, self.tour.description)
        self.assertContains(detail_response, '5.0')

    def test_sitemaps_llms_and_internal_routes_remain_dynamic(self):
        sitemap = self.client.get('/sitemap.xml').content.decode()
        for path in [
            self.tour.get_absolute_url(), '/dynamic-destination/',
            '/blog/dynamic-journal-guide/', '/faq/', '/destinations/',
        ]:
            self.assertIn(path, sitemap)

        llms = self.client.get('/llms.txt')
        self.assertContains(llms, self.tour.name)
        self.assertContains(llms, 'Dynamic Journal Guide')

        robots = self.client.get('/robots.txt')
        self.assertNotContains(robots, 'Disallow: /destinations/')
        self.assertNotContains(robots, 'Disallow: /best-boat-rides-')
        self.assertEqual(self.client.get('/about/').status_code, 404)

    def test_brand_call_and_tour_internal_links_are_available(self):
        self.assertTrue(InternalLink.objects.filter(keyword='Paradise Boat Rides', url='/').exists())
        self.assertTrue(InternalLink.objects.filter(keyword='call Paradise Boat Rides', url='tel:+254729360174').exists())
        self.assertTrue(InternalLink.objects.filter(keyword='book Paradise Boat Rides', url='/tours/').exists())
        linked = str(auto_link('<p>Paradise Boat Rides Naivasha tours. Call Paradise Boat Rides.</p>'))
        self.assertIn('href="/"', linked)
        self.assertIn('href="tel:+254729360174"', linked)
        self.assertNotIn('katrue', linked.lower())
