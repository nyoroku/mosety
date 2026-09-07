from django.test import TestCase, RequestFactory
from tours.models import Tour, PriceTier
from tours.views import FindYourRideView, PriceEstimateView
from core.models import SiteSettings


class ToursAndCalculatorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = SiteSettings.get_solo()
        self.site.business_name = "Mosety Boat Rides Naivasha"
        self.site.base_url = "https://mosety.co.ke"
        self.site.whatsapp_number = "+254 700 123456"
        self.site.save()

        self.tour = Tour.objects.create(
            name="Hippo & Bird Safari",
            slug="hippo-bird-safari",
            summary="Standard 1-hour safari across hippo bays.",
            description="Detailed description.",
            duration_minutes=60,
            min_guests=1,
            max_guests=7,
            is_active=True
        )

        self.tier_private = PriceTier.objects.create(
            tour=self.tour,
            label="Standard Private Boat",
            amount_kes=3500,
            pricing_mode="PER_BOAT",
            is_active=True
        )

        self.tier_shared = PriceTier.objects.create(
            tour=self.tour,
            label="Shared Ride",
            amount_kes=1200,
            pricing_mode="PER_PERSON",
            is_active=True
        )

    def test_tour_list_view_200(self):
        response = self.client.get('/boat-rides/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hippo &amp; Bird Safari")
        self.assertContains(response, "KES 3,500")

    def test_tour_detail_view_200(self):
        response = self.client.get('/boat-rides/hippo-bird-safari/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hippo &amp; Bird Safari")
        self.assertContains(response, "KES 3,500")
        self.assertContains(response, "https://wa.me/254700123456")

    def test_find_your_ride_htmx_endpoint(self):
        response = self.client.post('/find-your-ride/', {'intent': 'wildlife'}, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hippo &amp; Bird Safari")
        self.assertContains(response, "Recommended For You")

    def test_price_estimate_private_calculation(self):
        response = self.client.post('/prices/estimate/', {
            'tour_id': self.tour.id,
            'adults': '4',
            'children': '0',
            'booking_type': 'PRIVATE',
        }, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "KES 3,500")
        self.assertContains(response, "Approx. KES 875 per person")

    def test_price_estimate_shared_calculation(self):
        response = self.client.post('/prices/estimate/', {
            'tour_id': self.tour.id,
            'adults': '3',
            'children': '0',
            'booking_type': 'SHARED',
        }, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "KES 3,600")
        self.assertContains(response, "Approx. KES 1,200 per person")

    def test_prices_page_view_200(self):
        response = self.client.get('/prices/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Instant Ride Quote Calculator")
        self.assertContains(response, "Hippo &amp; Bird Safari")
