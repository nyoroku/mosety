import datetime
from django.test import TestCase, Client
from django.utils import timezone
from tours.models import Tour, PriceTier
from bookings.models import BookingLead
from core.models import SiteSettings


class BookingLeadViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.site = SiteSettings.get_solo()
        self.site.business_name = "Mosety Boat Rides Naivasha"
        self.site.whatsapp_number = "+254 700 123456"
        self.site.save()

        self.tour = Tour.objects.create(
            name="Hippo & Bird Safari",
            slug="hippo-bird-safari",
            summary="Standard 1-hour safari across hippo bays.",
            duration_minutes=60,
            min_guests=1,
            max_guests=7,
            is_active=True
        )

        self.tier = PriceTier.objects.create(
            tour=self.tour,
            label="Standard Private Boat",
            amount_kes=3500,
            pricing_mode="PER_BOAT",
            is_active=True
        )

    def test_book_get_page_200(self):
        response = self.client.get('/book/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reserve Your Lake Naivasha Boat Ride")
        self.assertContains(response, "Direct Lead Capture")

    def test_book_get_with_preselected_tour(self):
        response = self.client.get(f'/book/{self.tour.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hippo &amp; Bird Safari")

    def test_book_post_creates_lead_and_reference(self):
        trip_date = (timezone.now() + datetime.timedelta(days=3)).strftime('%Y-%m-%d')
        post_data = {
            'name': 'Wanjiku Kamau',
            'phone': '+254 712 345 678',
            'email': 'wanjiku@example.com',
            'tour': self.tour.id,
            'booking_type': 'PRIVATE',
            'trip_date': trip_date,
            'preferred_time': 'Mid-Morning (08:30 - 11:30)',
            'adults': 2,
            'children': 2,
            'notes': 'Visiting with 2 kids, need child life vests.',
        }
        response = self.client.post('/book/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Booking Request Received")
        self.assertContains(response, "MOS-")

        lead = BookingLead.objects.filter(phone='+254 712 345 678').first()
        self.assertIsNotNone(lead)
        self.assertTrue(lead.reference.startswith("MOS-"))
        self.assertEqual(lead.name, 'Wanjiku Kamau')
        self.assertEqual(lead.party_size, 4)
        self.assertEqual(lead.estimated_total, 3500)

    def test_book_post_htmx_returns_partial(self):
        trip_date = (timezone.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        post_data = {
            'name': 'Brian Omondi',
            'phone': '+254 722 000 111',
            'email': 'brian@example.com',
            'tour': self.tour.id,
            'booking_type': 'PRIVATE',
            'trip_date': trip_date,
            'preferred_time': 'Sunset Golden Hour (16:30 - 18:30)',
            'adults': 2,
            'children': 0,
        }
        response = self.client.post('/book/', post_data, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/partials/booking_success.html')
        self.assertContains(response, "Fast-Track Confirmation on WhatsApp")

    def test_book_persists_utm_attribution(self):
        # 1. Visit with UTM params to populate session via UTMMiddleware
        self.client.get('/?utm_source=google&utm_medium=cpc&utm_campaign=safari_search')

        trip_date = (timezone.now() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
        post_data = {
            'name': 'Sarah Jenkins',
            'phone': '+44 7700 900077',
            'email': 'sarah@example.co.uk',
            'tour': self.tour.id,
            'booking_type': 'PRIVATE',
            'trip_date': trip_date,
            'preferred_time': 'Early Morning (06:30 - 08:30)',
            'adults': 2,
            'children': 0,
        }
        response = self.client.post('/book/', post_data)
        self.assertEqual(response.status_code, 200)

        lead = BookingLead.objects.filter(name='Sarah Jenkins').first()
        self.assertIsNotNone(lead)
        self.assertEqual(lead.utm_source, 'google')
        self.assertEqual(lead.utm_medium, 'cpc')
        self.assertEqual(lead.utm_campaign, 'safari_search')
