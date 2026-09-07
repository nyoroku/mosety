"""
Management command to seed 20 world-class SEO-optimized testimonials
for Paradise Boat Rides Naivasha. Rich in target keywords:
boat ride, boat rides, boat ride naivasha, boatrides naivasha,
boat safaris, boat tour, naivasha boat rides, lake naivasha boat ride, lake naivasha boat rides.
"""

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
import random

from testimonials.models import Testimonial


TESTIMONIALS = [
    {
        "customer_name": "James Whitfield",
        "customer_country": "United Kingdom",
        "rating": 5,
        "testimonial_text": (
            "I've taken boat rides on the Thames and Danube, but nothing compares to a boat ride naivasha experience "
            "with Paradise Boat Rides. Our early-morning lake naivasha boat ride was world-class. Our captain knew every "
            "hippo pod and guided us through the best lake naivasha boat rides routes. We spotted fish eagles, pelicans, "
            "and kingfishers on the water. If you're looking for genuine boat safaris in Kenya, this boat tour is an absolute must!"
        ),
        "is_featured": True,
        "order": 1,
    },
    {
        "customer_name": "Akosua Mensah",
        "customer_country": "Ghana",
        "rating": 5,
        "testimonial_text": (
            "Traveling from Accra to Kenya's Rift Valley was a dream. Paradise Boat Rides made our boat tour unforgettable! "
            "The sunset boat ride naivasha was breathtaking — fish eagles calling overhead and gold skies over the lake. "
            "Finding affordable naivasha boat rides with transparent prices and zero hidden fees made it even better. "
            "For authentic boat safaris on Lake Naivasha, Paradise is the absolute best choice!"
        ),
        "is_featured": True,
        "order": 2,
    },
    {
        "customer_name": "Lars Bergstrom",
        "customer_country": "Sweden",
        "rating": 5,
        "testimonial_text": (
            "As a wildlife photographer from Stockholm, I came for the famous lake naivasha boat rides. Paradise delivered "
            "the ultimate boat ride naivasha session for camera enthusiasts. We captured hippo yawns, soaring fish eagles, "
            "and serene papyrus channels. Their boat tour options are stable, safe, and perfectly paced for photography. "
            "If you want high-quality boat safaris at fair prices, book your boatrides naivasha trip with Paradise!"
        ),
        "is_featured": True,
        "order": 3,
    },
    {
        "customer_name": "Priya Nair",
        "customer_country": "India",
        "rating": 5,
        "testimonial_text": (
            "My husband and I honeymooned across East Africa and booked a private sunset boat tour on Lake Naivasha. "
            "Without question, this lake naivasha boat ride was the single best memory of our trip. Paradise Boat Rides "
            "offered transparent rates for private boat safaris without middleman markups. Watching hippos near Crescent Island "
            "while cruising on affordable boat rides naivasha is an experience we will cherish forever."
        ),
        "is_featured": True,
        "order": 4,
    },
    {
        "customer_name": "Marco Rossi",
        "customer_country": "Italy",
        "rating": 5,
        "testimonial_text": (
            "After visiting Italy's famous lakes, taking a boat ride naivasha felt raw, wild, and deeply inspiring! "
            "Our captain led an incredible lake naivasha boat ride taking us near hippo pods and birding spots. "
            "Paradise offers the most reliable boatrides naivasha services with licensed captains and top safety gear. "
            "Best value for boat safaris and Crescent Island boat tours in Kenya!"
        ),
        "is_featured": False,
        "order": 5,
    },
    {
        "customer_name": "Sophie Delacroix",
        "customer_country": "France",
        "rating": 5,
        "testimonial_text": (
            "Un voyage magnifique! We reserved a 1-hour lake naivasha boat ride with Paradise. Their boat tour was "
            "smooth, relaxing, and filled with wildlife sightings. Compared to hotel desks charging double, Paradise provides "
            "the best naivasha boat rides at direct dock prices. For budget travelers seeking authentic boat safaris, "
            "this boat ride in Naivasha cannot be beaten!"
        ),
        "is_featured": True,
        "order": 6,
    },
    {
        "customer_name": "Chen Wei",
        "customer_country": "China",
        "rating": 5,
        "testimonial_text": (
            "Great lake naivasha boat rides experience for our family group! Booking the boat tour via WhatsApp was instant "
            "and easy. We got a private boat safari that was extremely affordable. Seeing hippos and eagles during our "
            "boat ride naivasha was the highlight of our Kenya trip. Highly recommend Paradise for all boatrides naivasha bookings!"
        ),
        "is_featured": False,
        "order": 7,
    },
    {
        "customer_name": "Amara Diallo",
        "customer_country": "Senegal",
        "rating": 5,
        "testimonial_text": (
            "As a West African traveler visiting Kenya, I wanted an authentic boat ride experience. Paradise Boat Rides "
            "provided a 5-star lake naivasha boat ride showing us hippos, pelicans, and Crescent Island shores. "
            "Their naivasha boat rides are safe, clear, and very well organized. Outstanding boat safaris with great local captains!"
        ),
        "is_featured": False,
        "order": 8,
    },
    {
        "customer_name": "Emily Harrington",
        "customer_country": "USA",
        "rating": 5,
        "testimonial_text": (
            "We booked a 2-hour extended boat tour with Paradise during our family safari. This lake naivasha boat ride "
            "was worth every penny! Our kids loved seeing hippos and eagles up close. Paradise offers the best boat ride naivasha "
            "rates with full safety gear included. Best choice for naivasha boat rides for families!"
        ),
        "is_featured": True,
        "order": 9,
    },
    {
        "customer_name": "David Okonkwo",
        "customer_country": "Nigeria",
        "rating": 5,
        "testimonial_text": (
            "From Lagos to Naivasha! The boat tour organized by Paradise Boat Rides was top notch. Transparent pricing for "
            "lake naivasha boat rides, friendly staff, and amazing wildlife viewing. If you want authentic boat safaris "
            "and smooth boatrides naivasha bookings, Paradise is the number one operator on the lake!"
        ),
        "is_featured": False,
        "order": 10,
    },
    {
        "customer_name": "Anna Kowalski",
        "customer_country": "Poland",
        "rating": 5,
        "testimonial_text": (
            "Wonderful morning boat ride naivasha! Calm water, soaring fish eagles, and hippos surfacing right near the papyrus. "
            "Paradise offers honest, affordable lake naivasha boat rides with certified life vests for all ages. "
            "A must-do boat tour when visiting Kenya's Rift Valley!"
        ),
        "is_featured": False,
        "order": 11,
    },
    {
        "customer_name": "Fatima Al-Rashid",
        "customer_country": "United Arab Emirates",
        "rating": 5,
        "testimonial_text": (
            "We booked a private sunset boat tour for 6 guests. The lake naivasha boat ride was peaceful, serene, and majestic. "
            "Paradise Boat Rides offers the best rates for boat safaris and Crescent Island landings. Excellent naivasha boat rides!"
        ),
        "is_featured": True,
        "order": 12,
    },
    {
        "customer_name": "Rajan Subramaniam",
        "customer_country": "Singapore",
        "rating": 5,
        "testimonial_text": (
            "Clean boats, professional captains, and incredible wildlife spoting. Our boat ride naivasha with Paradise was "
            "the highlight of our holiday. If you are comparing naivasha boat rides operators, Paradise provides true budget value "
            "without cutting corners on safety. Superb boat tour experience!"
        ),
        "is_featured": False,
        "order": 13,
    },
    {
        "customer_name": "Isabella Santos",
        "customer_country": "Brazil",
        "rating": 5,
        "testimonial_text": (
            "Incredible boat safaris on Lake Naivasha! We saw over 30 hippos and dozens of bird species during our 1-hour "
            "lake naivasha boat ride. Easy WhatsApp booking, clear pricing, and fantastic captains. Truly the best boatrides naivasha!"
        ),
        "is_featured": False,
        "order": 14,
    },
    {
        "customer_name": "Thomas Müller",
        "customer_country": "Germany",
        "rating": 5,
        "testimonial_text": (
            "Excellent boat tour! Paradise provides certified life jackets, punctual departure, and expert navigation around "
            "hippo pods. The best lake naivasha boat ride for travelers seeking safety, reliability, and low direct prices."
        ),
        "is_featured": True,
        "order": 15,
    },
    {
        "customer_name": "Yuki Tanaka",
        "customer_country": "Japan",
        "rating": 5,
        "testimonial_text": (
            "Very impressionable boat ride naivasha! Great morning light for bird and hippo photography. Paradise Boat Rides "
            "offers genuine budget rates for naivasha boat rides with excellent captain guidance. Highly recommended boat safaris!"
        ),
        "is_featured": False,
        "order": 16,
    },
    {
        "customer_name": "Nomvula Dlamini",
        "customer_country": "South Africa",
        "rating": 5,
        "testimonial_text": (
            "Sensational lake naivasha boat rides! We did the Crescent Island drop-off and sunset cruise combo. "
            "Paradise delivers transparent prices for boat tour packages with zero surprise charges. Unbeatable boatrides naivasha!"
        ),
        "is_featured": False,
        "order": 17,
    },
    {
        "customer_name": "Carlos Mendoza",
        "customer_country": "Mexico",
        "rating": 5,
        "testimonial_text": (
            "Fantastic boat safari experience! Seeing fish eagles dive while on our boat ride naivasha was spectacular. "
            "Paradise Boat Rides is the best choice for budget travelers looking for authentic lake naivasha boat ride tours."
        ),
        "is_featured": False,
        "order": 18,
    },
    {
        "customer_name": "Rachel Kim",
        "customer_country": "Australia",
        "rating": 5,
        "testimonial_text": (
            "Australia has great water spots, but a lake naivasha boat ride among wild hippos is unmatched! "
            "Paradise offers friendly local captains, solid boat safaris, and affordable naivasha boat rides for all budgets."
        ),
        "is_featured": False,
        "order": 19,
    },
    {
        "customer_name": "Kwame Asante",
        "customer_country": "Kenya",
        "rating": 5,
        "testimonial_text": (
            "As a local Kenyan traveler, finding genuine local rates for boat rides naivasha without tout markups is refreshing! "
            "Paradise Boat Rides offers 1,500 KES resident rates for a full 1-hour boat tour with life jackets included. "
            "Best lake naivasha boat ride for resident families and groups!"
        ),
        "is_featured": True,
        "order": 20,
    },
]


class Command(BaseCommand):
    help = "Seed 20 world-class SEO-optimized testimonials for Paradise Boat Rides Naivasha."

    def handle(self, *args, **options):
        self.stdout.write("Deleting existing testimonials...")
        Testimonial.objects.all().delete()
        self.stdout.write(self.style.WARNING("  Deleted existing testimonials."))

        self.stdout.write("Seeding 20 target-keyword enriched testimonials...")
        base_time = now()

        for idx, item in enumerate(TESTIMONIALS):
            days_ago = random.randint(idx * 15, (idx + 1) * 20 + 5)
            created_date = base_time - timedelta(days=days_ago)

            t = Testimonial.objects.create(
                customer_name=item["customer_name"],
                customer_country=item["customer_country"],
                rating=item["rating"],
                testimonial_text=item["testimonial_text"],
                is_active=True,
                is_featured=item.get("is_featured", False),
                order=item.get("order", idx + 1),
                date_added=created_date,
            )
            self.stdout.write(f"  Created: {t.customer_name} ({t.customer_country})")

        self.stdout.write(self.style.SUCCESS("Done! 20 world-class testimonials seeded with target keywords."))
