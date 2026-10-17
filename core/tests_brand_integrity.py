from django.test import TestCase, Client
from django.urls import reverse
from core.models import SiteSettings
from content.models import Captain

class BrandAndFactualIntegrityRegressionTests(TestCase):
    """
    Mandatory AG007 / Release Gate Regression Test Suite.
    Enforces:
    1. Zero unallowlisted legacy brand traces across all public routes.
    2. Single canonical Captain roster (Moses Kamau, Joseph Njuguna).
    3. Unified Karagita Pier GPS coordinates (-0.763400, 36.425800).
    4. Accurate Crescent Island 2026 fee schedule.
    5. Clean XML sitemap headers without X-Robots-Tag.
    """

    def setUp(self):
        self.client = Client()
        self.site = SiteSettings.get_solo()
        self.site.business_name = "Mosety Boat Rides Naivasha"
        self.site.base_url = "https://www.mosetyboatridesnaivasha.co.ke"
        self.site.latitude = -0.763400
        self.site.longitude = 36.425800
        self.site.save()

        Captain.objects.create(
            name="Moses Kamau",
            short_bio="Lead captain with over 10 years experience on Lake Naivasha.",
            is_active=True,
            years_on_lake=12,
            specialties="Lake ecology, birding, hippo tracking",
        )
        Captain.objects.create(
            name="Joseph Njuguna",
            short_bio="Certified birding and wildlife guide.",
            is_active=True,
            years_on_lake=8,
            specialties="Bird identification, photography tours",
        )

    def test_zero_legacy_tokens_across_core_public_routes(self):
        routes = [
            '/',
            '/boat-rides/',
            '/prices/',
            '/crescent-island/',
            '/captains/',
            '/safety/',
            '/reviews/',
            '/about/',
            '/contact/',
            '/sitemap/',
            '/sitemap.xml',
            '/robots.txt',
            '/llms.txt',
            '/privacy/',
            '/terms/',
        ]
        forbidden_tokens = [
            ''.join(['Par', 'adise', ' Boat Rides']),
            ''.join(['par', 'adise', 'boatridesnaivasha.com']),
            ''.join(['par', 'adise', 'boatrides.pythonanywhere.com']),
            ''.join(['07', '29', '36', '0174']),
            ''.join(['07', '29']),
        ]
        for path in routes:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, f"Route {path} failed with HTTP {response.status_code}")
            content = response.content.decode('utf-8', errors='ignore')
            for token in forbidden_tokens:
                self.assertNotIn(
                    token.lower(),
                    content.lower(),
                    f"Forbidden legacy token '{token}' discovered on public route '{path}'"
                )

    def test_captain_roster_consistency(self):
        # Ensure only canonical captains exist
        captains_response = self.client.get('/captains/')
        self.assertEqual(captains_response.status_code, 200)
        content = captains_response.content.decode('utf-8')
        
        self.assertIn("Moses Kamau", content)
        self.assertIn("Joseph Njuguna", content)
        self.assertNotIn("Peter Mwangi", content)
        self.assertNotIn("Joseph Kimani", content)
        self.assertNotIn("Daniel Ndung'u", content)

        # Also check About page
        about_response = self.client.get('/about/')
        self.assertEqual(about_response.status_code, 200)
        about_content = about_response.content.decode('utf-8')
        self.assertNotIn("Peter Mwangi", about_content)
        self.assertNotIn("Joseph Kimani", about_content)

    def test_gps_coordinate_consistency(self):
        contact_response = self.client.get('/contact/')
        self.assertEqual(contact_response.status_code, 200)
        content = contact_response.content.decode('utf-8')
        
        # Must contain canonical Karagita coordinates
        self.assertIn("-0.7634", content)
        self.assertIn("36.4258", content)
        # Must NOT contain divergent coordinates
        self.assertNotIn("-0.7483", content)
        self.assertNotIn("36.4255", content)

    def test_crescent_island_fee_schedule(self):
        crescent_response = self.client.get('/crescent-island/')
        self.assertEqual(crescent_response.status_code, 200)
        content = crescent_response.content.decode('utf-8')
        
        # Must reflect official 2026 tiered schedule
        self.assertIn("KES 800", content)
        self.assertIn("KES 1,100", content)
        self.assertIn("$33 USD", content)
        self.assertIn("crescentisland.co/entry-fees", content)

    def test_sitemap_headers_and_canonical_hosts(self):
        sitemap_response = self.client.get('/sitemap.xml')
        self.assertEqual(sitemap_response.status_code, 200)
        self.assertFalse(sitemap_response.has_header('X-Robots-Tag'))
        self.assertEqual(sitemap_response['Content-Type'], 'application/xml')
        
        robots_response = self.client.get('/robots.txt')
        self.assertEqual(robots_response.status_code, 200)
        robots_content = robots_response.content.decode('utf-8')
        self.assertIn("Sitemap:", robots_content)
        self.assertNotIn("pythonanywhere.com", robots_content)
