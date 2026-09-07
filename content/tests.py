from django.test import TestCase, Client
from django.utils import timezone
from core.models import SiteSettings
from tours.models import Tour, PriceTier
from content.models import Captain, GuideArticle, QuestionAnswer, Testimonial


class ContentAppViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.site = SiteSettings.get_solo()
        self.site.business_name = "Mosety Boat Rides Naivasha"
        self.site.whatsapp_number = "+254 700 123456"
        self.site.save()

        self.tour = Tour.objects.create(
            name="Crescent Island Boat Ride & Walk",
            slug="crescent-island",
            summary="Scenic boat ride to Crescent Island Game Sanctuary.",
            duration_minutes=120,
            is_active=True
        )

        self.captain = Captain.objects.create(
            name="Peter Mwangi",
            slug="peter-mwangi",
            short_bio="Born and raised on the shores of Lake Naivasha.",
            years_on_lake=14,
            specialties="Hippo pod behavior & raptors",
            languages="English, Swahili",
            is_active=True
        )

        self.faq = QuestionAnswer.objects.create(
            question="How much are Crescent Island sanctuary entrance fees?",
            answer="Citizens pay KES 1,000 and non-residents pay $33 USD directly at the sanctuary gate.",
            category="Pricing",
            related_tour=self.tour,
            is_active=True
        )

        self.review = Testimonial.objects.create(
            display_name="David M.",
            rating=5,
            review_text="Walking among giraffes after a smooth boat ride was magical.",
            source="Google Review",
            is_active=True
        )

        self.article = GuideArticle.objects.create(
            title="Where & How Lake Naivasha Hippos Are Viewed Safely",
            slug="hippo-viewing-guide-naivasha",
            excerpt="A captain's guide to pod dynamics and 30-50m safety buffers.",
            body="Hippos are territorial mammals that require respect.",
            author_name="Captain Peter Mwangi",
            content_type="JOURNAL",
            is_active=True
        )

    def test_crescent_island_pillar_view(self):
        response = self.client.get('/crescent-island/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Crescent Island Game Sanctuary")
        self.assertContains(response, "KES 1,000 / $33 USD")
        self.assertContains(response, "Understanding the Two Separate Costs")

    def test_safety_standards_view(self):
        response = self.client.get('/safety/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Safety on Lake Naivasha Starts Before Boarding")
        self.assertContains(response, "30–50m Ethical Hippo Buffer")
        self.assertContains(response, "Mandatory Fitted Life Jackets")

    def test_captains_view(self):
        response = self.client.get('/captains/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Captain Peter Mwangi")
        self.assertContains(response, "14+ Years on Lake Naivasha")

    def test_reviews_view(self):
        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Real Stories from the Water")
        self.assertContains(response, "Our Zero-Fabrication Integrity Policy")
        self.assertContains(response, "David M.")

    def test_about_view(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Built on Lake Naivasha Waters")
        self.assertContains(response, "Direct Pier Pricing")

    def test_contact_location_view(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Karagita Boat Launch Pier")
        self.assertContains(response, "-0.7483° S, 36.4255° E")
        self.assertContains(response, "Mai Mahiu")

    def test_faq_hub_view(self):
        response = self.client.get('/questions/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frequently Asked Questions")
        self.assertContains(response, "How much are Crescent Island sanctuary entrance fees?")

    def test_plan_your_visit_subpages(self):
        endpoints = [
            '/plan-your-visit/',
            '/plan-your-visit/getting-here/',
            '/plan-your-visit/best-time-to-go/',
            '/plan-your-visit/what-to-bring/',
            '/plan-your-visit/children/',
        ]
        for url in endpoints:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed at {url}")

    def test_naivasha_guide_subpages(self):
        endpoints = [
            '/naivasha-guide/',
            '/naivasha-guide/hippos/',
            '/naivasha-guide/birds/',
            '/naivasha-guide/wildlife/',
        ]
        for url in endpoints:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed at {url}")

    def test_journal_views(self):
        res = self.client.get('/journal/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Where &amp; How Lake Naivasha Hippos Are Viewed Safely")

        res_detail = self.client.get('/journal/hippo-viewing-guide-naivasha/')
        self.assertEqual(res_detail.status_code, 200)
        self.assertContains(res_detail, "Captain Peter Mwangi")

    def test_zero_residue_across_views(self):
        endpoints = [
            '/crescent-island/', '/safety/', '/captains/', '/reviews/',
            '/about/', '/contact/', '/questions/', '/plan-your-visit/',
            '/naivasha-guide/', '/journal/'
        ]
        forbidden = ['Paradise Boat Rides', '0729360174', 'paradiseboatridesnaivasha.com']
        for url in endpoints:
            res = self.client.get(url)
            body = res.content.decode('utf-8')
            for bad_str in forbidden:
                self.assertNotIn(bad_str.lower(), body.lower(), f"Residue '{bad_str}' found in {url}")
