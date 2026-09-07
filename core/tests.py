import json
import re
from django.test import TestCase, RequestFactory
from django.urls import reverse
from core.models import SiteSettings
from seo.models import Redirect
from seo.utils import clean_canonical_url, build_local_business_schema, build_faq_schema
from analytics.middleware import UTMMiddleware
from seo.middleware import SEORedirectMiddleware


class TestSiteSettingsAndWhatsApp(TestCase):
    def setUp(self):
        self.site = SiteSettings.get_solo()
        self.site.business_name = "Mosety Boat Rides Naivasha"
        self.site.phone = "+254 700 123456"
        self.site.whatsapp_number = "+254 700 123456"
        self.site.base_url = "https://mosety.co.ke"
        self.site.save()

    def test_singleton_nature(self):
        site2 = SiteSettings.get_solo()
        self.assertEqual(self.site.id, site2.id)
        self.assertEqual(site2.business_name, "Mosety Boat Rides Naivasha")

    def test_phone_and_whatsapp_formatting(self):
        self.assertEqual(self.site.whatsapp_digits, "254700123456")
        self.assertEqual(self.site.phone_e164, "+254700123456")
        self.assertEqual(self.site.tel_url, "tel:+254700123456")

    def test_whatsapp_url_encoding(self):
        url = self.site.build_whatsapp_url("Hello Mosety! Testing quote.")
        self.assertIn("https://wa.me/254700123456?text=", url)
        self.assertIn("Hello%20Mosety%21%20Testing%20quote.", url)


class TestCanonicalURLStripping(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = SiteSettings.get_solo()
        self.site.base_url = "https://mosety.co.ke"
        self.site.save()

    def test_tracking_parameters_stripped_from_canonical(self):
        request = self.factory.get('/boat-rides/?utm_source=facebook&utm_medium=cpc&gclid=xyz123&ref=partner')
        canonical = clean_canonical_url(request)
        self.assertEqual(canonical, "https://mosety.co.ke/boat-rides/")

    def test_pagination_preserved_when_greater_than_one(self):
        request = self.factory.get('/journal/?page=3&utm_source=newsletter')
        canonical = clean_canonical_url(request)
        self.assertEqual(canonical, "https://mosety.co.ke/journal/?page=3")

    def test_page_one_stripped_to_clean_root(self):
        request = self.factory.get('/journal/?page=1&utm_campaign=autumn')
        canonical = clean_canonical_url(request)
        self.assertEqual(canonical, "https://mosety.co.ke/journal/")


class TestStructuredData(TestCase):
    def setUp(self):
        self.site = SiteSettings.get_solo()
        self.site.business_name = "Mosety Boat Rides Naivasha"
        self.site.base_url = "https://mosety.co.ke"
        self.site.latitude = -0.763400
        self.site.longitude = 36.425800
        self.site.save()

    def test_local_business_schema_structure(self):
        schema = build_local_business_schema(self.site)
        self.assertEqual(schema["@context"], "https://schema.org")
        self.assertIn("TouristAttraction", schema["@type"])
        self.assertIn("LocalBusiness", schema["@type"])
        self.assertEqual(schema["@id"], "https://mosety.co.ke/#business")
        self.assertEqual(schema["name"], "Mosety Boat Rides Naivasha")
        self.assertEqual(schema["geo"]["latitude"], -0.7634)
        self.assertEqual(schema["geo"]["longitude"], 36.4258)

    def test_faq_schema_generation(self):
        sample_faqs = [
            ("Are life jackets provided?", "Yes, certified life jackets are provided for all passengers."),
            ("How long does a boat ride take?", "A standard ride is 1 to 2 hours.")
        ]
        schema = build_faq_schema(sample_faqs)
        self.assertEqual(schema["@type"], "FAQPage")
        self.assertEqual(len(schema["mainEntity"]), 2)
        self.assertEqual(schema["mainEntity"][0]["name"], "Are life jackets provided?")


class TestMiddleware(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_utm_middleware_persists_attribution_in_session(self):
        request = self.factory.get('/?utm_source=instagram&utm_medium=bio_link&utm_campaign=sunset_special')
        request.session = {}

        middleware = UTMMiddleware(lambda r: None)
        middleware(request)

        self.assertIn('utm_data', request.session)
        utm = request.session['utm_data']
        self.assertEqual(utm.get('utm_source'), 'instagram')
        self.assertEqual(utm.get('utm_medium'), 'bio_link')
        self.assertEqual(utm.get('utm_campaign'), 'sunset_special')

    def test_seo_redirect_middleware(self):
        Redirect.objects.create(
            old_path='/legacy-tour/',
            new_path='/boat-rides/hippo-bird-safari/',
            status_code=301,
            is_active=True
        )
        request = self.factory.get('/legacy-tour/')
        middleware = SEORedirectMiddleware(lambda r: None)
        response = middleware(request)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], '/boat-rides/hippo-bird-safari/')


class TestHomepageShellAndZeroResidue(TestCase):
    def setUp(self):
        SiteSettings.get_solo()

    def test_homepage_shell_renders_200_with_single_h1(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        
        # Verify single H1 tag on homepage
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        self.assertEqual(len(h1_matches), 1, f"Expected exactly 1 H1 tag, found {len(h1_matches)}")
        self.assertIn("Unforgettable boat rides on Lake Naivasha", h1_matches[0])

        # Verify page title and meta description
        self.assertIn("<title>Mosety Boat Rides Naivasha", content)
        self.assertIn('<meta name="description"', content)
        self.assertIn('<link rel="canonical" href="https://mosety.co.ke/"', content)

        # Verify Rift Gold tokens in stylesheet link
        self.assertIn('mosety.css', content)

        # Verify Alpine.js and HTMX inclusion
        self.assertIn('alpinejs', content)
        self.assertIn('htmx.org', content)

    def test_zero_paradise_residue_in_homepage(self):
        response = self.client.get('/')
        content = response.content.decode('utf-8')

        # Check for forbidden legacy brand residue
        self.assertNotIn("Paradise Boat Rides", content)
        self.assertNotIn("paradiseboatridesnaivasha.com", content)
        self.assertNotIn("0729360174", content)
        self.assertNotIn("Memories on Water", content)

    def test_robots_txt_uses_mosety_domain(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn("Sitemap: https://mosety.co.ke/sitemap.xml", content)
        self.assertNotIn("paradiseboatridesnaivasha.com", content)
