import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from django.core.management import call_command
from django.core.files import File
from core.models import SiteSettings
from tours.models import Tour, PriceTier
from content.models import Captain, GuideArticle, QuestionAnswer, Testimonial

def run_seed():
    print("1. Running database migrations...")
    call_command('migrate', interactive=False)

    print("2. Configuring SiteSettings...")
    site = SiteSettings.get_solo()
    site.business_name = "Mosety Boat Rides Naivasha"
    site.tagline = "See Naivasha from the water."
    site.phone = "+254 114 182706"
    site.whatsapp_number = "+254 114 182706"
    site.base_url = "https://mosety.pythonanywhere.com"
    site.address_text = "Karagita Public Beach, South Lake Road, Lake Naivasha, Kenya"
    site.save()

    print("3. Seeding Tours & Price Tiers...")
    tours_data = [
        {
            'name': 'Hippo & Bird Safari',
            'slug': 'hippo-bird-safari',
            'short_name': 'Hippo Safari',
            'summary': 'Standard 1-hour safari across hippo bays with raptor viewing.',
            'description': 'Our signature 1-hour cruise departs from Karagita Beach into calm morning bays where wild hippo pods rest in the shallows.',
            'duration_minutes': 60,
            'max_guests': 7,
            'intent_tag': 'wildlife',
            'is_featured': True,
            'image': 'static/images/gallery/naivasha-hippo.jpeg',
            'tiers': [
                ('Standard Private Boat (1 Hour)', 3500, 'PER_BOAT'),
                ('Shared Boat Ride (Per Person)', 1200, 'PER_PERSON'),
                ('Extended Private Boat (2 Hours)', 6000, 'PER_BOAT'),
            ]
        },
        {
            'name': 'Crescent Island Boat Ride & Walk',
            'slug': 'crescent-island',
            'short_name': 'Crescent Island Trip',
            'summary': 'Boat cruise combined with unhurried walking safari among giraffes and zebras.',
            'description': 'A 2.5-hour package combining a scenic lake crossing, hippo viewing, and a 2-hour waiting period while you explore Crescent Island on foot.',
            'duration_minutes': 150,
            'max_guests': 7,
            'intent_tag': 'crescent_island',
            'is_featured': True,
            'image': 'static/images/gallery/naivasha-giraffes-boat.jpeg',
            'tiers': [
                ('Boat Charter (Transfer + 2hr Waiting)', 5000, 'PER_BOAT'),
                ('Shared Return Boat Transfer', 1500, 'PER_PERSON'),
            ]
        },
        {
            'name': 'Lake Naivasha Sunset Cruise',
            'slug': 'sunset-cruise',
            'short_name': 'Sunset Cruise',
            'summary': 'Private evening charter during golden hour with dramatic Mau Escarpment colors.',
            'description': 'Depart at 5:00 PM for mirror-calm waters and dramatic amber skies as wild hippos begin their evening routine.',
            'duration_minutes': 90,
            'max_guests': 7,
            'intent_tag': 'sunset',
            'is_featured': True,
            'image': 'static/images/gallery/naivasha-sunset-guests.jpeg',
            'tiers': [
                ('Private Sunset Charter (1.5 Hours)', 6000, 'PER_BOAT'),
            ]
        },
        {
            'name': 'Private Boat Ride Charter',
            'slug': 'private-boat',
            'short_name': 'Private Boat Charter',
            'summary': 'Exclusive boat hire with custom routing, dedicated captain, and total privacy.',
            'description': 'Enjoy an entire boat reserved exclusively for your party with tailored departure times and flexible stops.',
            'duration_minutes': 60,
            'max_guests': 7,
            'intent_tag': 'private',
            'is_featured': True,
            'image': 'static/images/gallery/naivasha-boat-passenger.jpeg',
            'tiers': [
                ('Private Charter (1 Hour)', 4500, 'PER_BOAT'),
                ('Private Charter (2 Hours)', 8000, 'PER_BOAT'),
            ]
        },
        {
            'name': 'Family Lake Boat Ride',
            'slug': 'family-boat-ride',
            'short_name': 'Family Boat Ride',
            'summary': 'Family-friendly cruise with infant/child safety life jackets and gentle guiding.',
            'description': 'Tailored for traveling families with certified children life vests and educational captain commentary.',
            'duration_minutes': 60,
            'max_guests': 7,
            'intent_tag': 'family',
            'is_featured': False,
            'image': 'static/images/gallery/naivasha-cruise-guests.jpeg',
            'tiers': [
                ('Private Family Boat (Up to 7 Guests)', 4000, 'PER_BOAT'),
            ]
        },
        {
            'name': 'Photography & Birding Expedition',
            'slug': 'photography-birding',
            'short_name': 'Birding Charter',
            'summary': 'Early morning charter for enthusiasts tracking 400+ species with silent drift positioning.',
            'description': 'Dawn 6:30 AM departure designed for long-lens photographers with low-wake maneuvering and bird species guidance.',
            'duration_minutes': 120,
            'max_guests': 6,
            'intent_tag': 'birding',
            'is_featured': False,
            'image': 'static/images/gallery/naivasha-boat-wildlife.jpeg',
            'tiers': [
                ('Dedicated Birding Charter (2 Hours)', 7000, 'PER_BOAT'),
            ]
        },
        {
            'name': 'Group & Corporate Boat Rides',
            'slug': 'groups-corporate',
            'short_name': 'Group Boat Rides',
            'summary': 'Multi-boat packages for corporate retreats, churches, and large tour groups.',
            'description': 'Coordinated multi-boat lake excursions accommodating 15 to 150 guests with coordinated schedules.',
            'duration_minutes': 60,
            'max_guests': 100,
            'intent_tag': 'group',
            'is_featured': False,
            'image': 'static/images/gallery/naivasha-group-boat.jpeg',
            'tiers': [
                ('Group Rate (Per Person, Min 8 Guests)', 1000, 'PER_PERSON'),
            ]
        },
    ]

    for td in tours_data:
        tour, _ = Tour.objects.get_or_create(
            slug=td['slug'],
            defaults={
                'name': td['name'],
                'short_name': td['short_name'],
                'summary': td['summary'],
                'description': td['description'],
                'duration_minutes': td['duration_minutes'],
                'max_guests': td['max_guests'],
                'intent_tag': td['intent_tag'],
                'is_featured': td['is_featured'],
                'is_active': True,
            }
        )
        if os.path.exists(td['image']) and (not tour.hero_image or not os.path.exists(tour.hero_image.path)):
            with open(td['image'], 'rb') as f:
                tour.hero_image.save(os.path.basename(td['image']), File(f), save=True)

        for label, amt, mode in td['tiers']:
            PriceTier.objects.get_or_create(
                tour=tour,
                label=label,
                defaults={'amount_kes': amt, 'pricing_mode': mode, 'is_active': True}
            )
        print(f"  - Tour: {tour.name}")

    print("4. Seeding Captains...")
    captains_data = [
        ('Moses Kamau', 'moses-kamau', 'Born and raised in Naivasha, Captain Moses Kamau has over 15 years of professional boat safari experience piloting from Karagita Beach across Crescent Island channels and Oloidien Bay. Licensed by the Kenya Maritime Authority, Moses is renowned for his deep understanding of resident hippo families, water currents, and calm, reassuring navigation.', 15, 'Hippo pod behavior, Crescent Island navigation, golden hour photography, sunrise boat rides', 'static/images/captains/captain-moses-kamau.jpeg'),
        ('Joseph Njuguna', 'joseph-njuguna', 'Captain Joseph Njuguna is an experienced Lake Naivasha boat captain and certified birding specialist with 12 years piloting safari craft from Karagita Pier. Renowned for his sharp wildlife spotting, encyclopedic bird knowledge, and gentle handling of family groups, Joseph guarantees every guest enjoys the best boat ride on Lake Naivasha with complete safety.', 12, 'African fish eagle feeding spots, water bird identification, family & group boat rides, eco-tours', 'static/images/captains/captain-joseph-njuguna.jpeg'),
    ]
    for name, slug, bio, years, spec, img in captains_data:
        capt, _ = Captain.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'short_bio': bio,
                'years_on_lake': years,
                'specialties': spec,
                'is_active': True
            }
        )
        if os.path.exists(img) and (not capt.photo or not os.path.exists(capt.photo.path)):
            with open(img, 'rb') as f:
                capt.photo.save(os.path.basename(img), File(f), save=True)
        print(f"  - Captain: {capt.name}")

    print("5. Seeding Field Articles & Journal...")
    articles_data = [
        ('Where & How Lake Naivasha Hippos Are Viewed Safely', 'hippo-viewing-guide-naivasha', 'Why maintaining 30-50m distances protects both guests and nursing mothers in the shallows.', 'static/images/gallery/naivasha-hippo-shore.jpeg'),
        ('Complete Crescent Island Sanctuary Walking Safari Guide', 'crescent-island-sanctuary-guide', 'How to combine a boat ride with Kenya\'s most famous walking safari: entry fees, animal checklist, and walking loops.', 'static/images/gallery/naivasha-giraffe.jpeg'),
        ('The Complete One-Day Lake Naivasha Day Trip from Nairobi', 'nairobi-to-naivasha-day-trip-itinerary', 'A realistic timeline for traveling from Nairobi, enjoying morning boat safaris, walking Crescent Island, and returning comfortably.', 'static/images/gallery/naivasha-boats-lake.jpeg'),
        ('Birdwatching & Raptor Photography on Lake Naivasha: A Captain\'s Field Manual', 'birdwatching-photography-guide-naivasha', 'Field notes on spotting 400+ bird species, tracking African fish eagles, and boat positioning for reflections.', 'static/images/gallery/naivasha-boat-wildlife.jpeg'),
        ('Lake Naivasha Sunset Boat Rides: Timing, Golden Hour Light & What to Expect', 'sunset-boat-rides-lake-naivasha', 'Why the 5:00 PM to 6:30 PM departure window delivers mirror-calm waters, dramatic Mau Escarpment silhouettes, and evening hippo activity.', 'static/images/gallery/naivasha-sunset-guests.jpeg'),
        ('Lake Naivasha Boat Ride Prices & Dock Etiquette: 2026 Direct Guide', 'boat-ride-prices-dock-guide-naivasha', 'A transparent breakdown of standard pier rates, private charters vs shared rides, Crescent Island fees, and tipping norms at Karagita Beach.', 'static/images/gallery/naivasha-captain.jpeg'),
    ]
    for title, slug, excerpt, img in articles_data:
        art, _ = GuideArticle.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title,
                'excerpt': excerpt,
                'body': f"<p>{excerpt}</p>",
                'content_type': 'JOURNAL',
                'author_name': 'Mosety Senior Captains',
                'is_active': True,
                'is_featured': True
            }
        )
        if os.path.exists(img) and (not art.hero_image or not os.path.exists(art.hero_image.path)):
            with open(img, 'rb') as f:
                art.hero_image.save(os.path.basename(img), File(f), save=True)
        print(f"  - Article: {art.title}")

    print("6. Collecting static files...")
    call_command('collectstatic', interactive=False)
    print("\n[OK] Mosety seed completed successfully!")

if __name__ == '__main__':
    run_seed()
