from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from content.models import GuideArticle, QuestionAnswer
from tours.models import Tour
from seo.models import InternalLink

from .seo_geo_articles_part1 import ARTICLES_PART_1
from .seo_geo_articles_part2 import ARTICLES_PART_2
from .seo_geo_articles_part3 import ARTICLES_PART_3


VALID_CONTENT_TYPES = {'PLANNING', 'DESTINATION', 'WILDLIFE', 'JOURNAL', 'ITINERARY'}

PAA_FAQS = [
    (
        1,
        "Pricing",
        "How much is a boat ride at Lake Naivasha?",
        (
            "In 2026, direct Karagita Public Pier boat rides with Mosety start at KES 3,500 per private boat "
            "(up to 7 guests) for a 1-hour Hippo & Bird Safari, KES 4,000 for a Family Boat Ride, KES 4,500 for a "
            "Private Charter, KES 5,000 for a round-trip Crescent Island boat transfer with waiting time, KES 6,000 "
            "for a 1.5-hour Sunset Cruise, and KES 7,000 for an early-morning Photography & Birding Expedition. "
            "Organized group rides start from KES 1,000 per person. Every fare includes the boat, fuel, licensed "
            "local captain, and fitted adult and child life jackets."
        ),
        "hippo-bird-safari",
    ),
    (
        2,
        "General",
        "What are the typical times for the boat ride at Lake Naivasha?",
        (
            "Mosety boat rides depart daily on demand from 06:30 AM to 06:30 PM at Karagita Public Pier. "
            "Typical ride durations are 1 hour for a standard Hippo & Bird Safari, 1.5 hours for a Sunset Cruise "
            "(departing around 04:30 PM), and 2.5 to 3 hours total for a Crescent Island boat ride and walking safari. "
            "Morning departures (06:30 AM – 10:30 AM) offer the calmest water and most active birdlife."
        ),
        "hippo-bird-safari",
    ),
    (
        3,
        "Pricing",
        "Is there an entry fee for Lake Naivasha?",
        (
            "No. There is no general KWS park entry fee to access Lake Naivasha or take a boat ride from Karagita "
            "Public Beach Pier. You only pay your boat charter rate. Separate sanctuary gate fees apply only if you "
            "choose to disembark for a walking safari on Crescent Island Game Sanctuary (2026 rates: Kenya Citizens "
            "KES 800 adult / KES 400 child; Kenya Residents KES 1,100 adult / KES 550 child; Non-Residents $33 USD "
            "adult / $22 student / $16 child; under 5 free) or enter nearby Hell's Gate National Park."
        ),
        "crescent-island",
    ),
    (
        4,
        "Pricing",
        "How much does it cost to go to Naivasha?",
        (
            "A full day trip from Nairobi to Lake Naivasha typically costs KES 3,000 to KES 6,500 per Kenyan resident "
            "(covering public matatu KES 400–600 each way or shared fuel, a split private boat ride from KES 875–1,750 "
            "per person, optional Crescent Island gate ticket KES 800–1,100, and lakeside lunch). International visitors "
            "taking a private boat and Crescent Island walk typically budget $75 to $130 USD per person excluding private "
            "vehicle hire."
        ),
        "crescent-island",
    ),
    (
        5,
        "Pricing",
        "What is the Crescent Island boat ride price and walking safari entry fee?",
        (
            "Visiting Crescent Island by boat involves two separate transparent costs: (1) Mosety's round-trip private "
            "boat charter with 1.5–2 hours captain waiting time at KES 5,000 per boat (up to 7 guests), and (2) official "
            "2026 Crescent Island Game Sanctuary gate tickets paid directly to sanctuary rangers upon landing (Kenya "
            "Citizens KES 800 adult / KES 400 child; Kenya Residents KES 1,100 adult / KES 550 child; Non-Residents "
            "$33 USD adult / $22 student / $16 child; children under 5 enter free)."
        ),
        "crescent-island",
    ),
    (
        6,
        "Safety",
        "How do I choose the best boat ride operator on Lake Naivasha?",
        (
            "Look for published per-boat vs. per-person rates, transparent separation of Crescent Island sanctuary "
            "fees, named licensed local captains (at Mosety: Captain Moses Kamau and Captain Joseph Njuguna), "
            "fitted adult and child life jackets, strict 7-passenger boat capacity, calm 30–50m hippo safety buffers, "
            "and direct Karagita Public Pier boarding without roadside broker commissions."
        ),
        "private-boat",
    ),
]

CANONICAL_INTERNAL_LINKS = [
    ("Lake Naivasha boat ride prices", "/prices/"),
    ("boat rides Naivasha prices", "/prices/"),
    ("Lake Naivasha boat ride price", "/prices/"),
    ("Crescent Island boat ride price", "/journal/crescent-island-boat-ride-price-2026/"),
    ("day boat rides Naivasha", "/journal/day-boat-rides-naivasha-complete-schedule/"),
    ("day boat ride Naivasha", "/journal/day-boat-rides-naivasha-complete-schedule/"),
    ("best boat rides Naivasha", "/journal/best-boat-rides-naivasha-how-to-choose/"),
    ("Lake Naivasha boat ride reviews", "/reviews/"),
    ("Lake Naivasha boat ride review", "/journal/lake-naivasha-boat-ride-reviews-what-travelers-say/"),
    ("Lake Naivasha boat ride and Crescent Island", "/journal/lake-naivasha-boat-ride-and-crescent-island-complete-guide/"),
    ("Crescent Island Game Sanctuary", "/crescent-island/"),
    ("Crescent Island walking safari", "/crescent-island/"),
    ("Crescent Island boat ride", "/boat-rides/crescent-island/"),
    ("Crescent Island transfer", "/boat-rides/crescent-island/"),
    ("Crescent Island", "/crescent-island/"),
    ("Hippo & Bird Safari", "/boat-rides/hippo-bird-safari/"),
    ("hippo boat safari", "/boat-rides/hippo-bird-safari/"),
    ("Lake Naivasha hippos", "/naivasha-guide/hippos/"),
    ("hippo pods", "/naivasha-guide/hippos/"),
    ("African fish eagles", "/naivasha-guide/birds/"),
    ("African fish eagle", "/naivasha-guide/birds/"),
    ("bird watching on Lake Naivasha", "/naivasha-guide/birds/"),
    ("Lake Naivasha Sunset Cruise", "/boat-rides/sunset-cruise/"),
    ("sunset cruise", "/boat-rides/sunset-cruise/"),
    ("sunset boat ride", "/boat-rides/sunset-cruise/"),
    ("private boat charter", "/boat-rides/private-boat/"),
    ("Private Boat Ride Charter", "/boat-rides/private-boat/"),
    ("Family Lake Boat Ride", "/boat-rides/family-boat-ride/"),
    ("family boat rides", "/boat-rides/family-boat-ride/"),
    ("Photography & Birding Expedition", "/boat-rides/photography-birding/"),
    ("Group & Corporate Boat Rides", "/boat-rides/groups-corporate/"),
    ("Karagita Public Pier", "/contact/"),
    ("Karagita Public Beach", "/contact/"),
    ("Karagita Pier", "/contact/"),
    ("Captain Moses Kamau", "/captains/"),
    ("Captain Joseph Njuguna", "/captains/"),
    ("safety standards", "/safety/"),
    ("life jackets", "/safety/"),
    ("entry fee for Lake Naivasha", "/journal/is-there-an-entry-fee-for-lake-naivasha/"),
    ("best time of day", "/plan-your-visit/best-time-to-go/"),
    ("Nairobi to Lake Naivasha", "/plan-your-visit/getting-here/"),
    ("what to bring", "/plan-your-visit/what-to-bring/"),
    ("visiting with children", "/plan-your-visit/children/"),
    ("Lake Naivasha wildlife", "/naivasha-guide/wildlife/"),
    ("Lake Naivasha boat rides", "/boat-rides/"),
    ("Mosety Boat Rides Naivasha", "/"),
    ("Mosety Boat Rides", "/"),
]


def render_article_html(spec):
    parts = [
        '<div class="quick-answer">',
        '<p style="margin-bottom: 0;"><strong>Quick Answer:</strong> ' + spec["quick_answer"] + "</p>",
        "</div>",
    ]
    for heading, html_body in spec["sections"]:
        parts.append(f"<h2>{heading}</h2>")
        parts.append(html_body)

    if spec.get("captain_tip"):
        parts.append(
            '<div style="background: #ffffff; border: 1px solid var(--border-papyrus); border-left: 4px solid var(--ink-forest); border-radius: var(--radius-sm); padding: 1.25rem 1.4rem; margin-block: 1.75rem;">'
            f'<p style="margin: 0;"><strong>Local Captain Tip ({spec["reviewer"]}):</strong> {spec["captain_tip"]}</p>'
            "</div>"
        )

    if spec.get("faqs"):
        parts.append("<h2>Frequently Asked Questions</h2>")
        for q, a in spec["faqs"]:
            parts.append(f"<h3>{q}</h3>")
            parts.append(f"<p>{a}</p>")

    return "\n".join(parts)


class Command(BaseCommand):
    help = "Seed 50 SEO + GEO/AEO GuideArticles, PAA FAQs, and canonical InternalLinks for Mosety Boat Rides Naivasha."

    def handle(self, *args, **options):
        all_specs = ARTICLES_PART_1 + ARTICLES_PART_2 + ARTICLES_PART_3
        self.stdout.write(f"Seeding {len(all_specs)} SEO + GEO/AEO GuideArticles...")

        tour_map = {t.slug: t for t in Tour.objects.filter(is_active=True)}
        base_time = timezone.now()

        created_count = 0
        updated_count = 0

        for idx, spec in enumerate(all_specs):
            ctype = spec.get("content_type", "PLANNING")
            if ctype not in VALID_CONTENT_TYPES:
                ctype = "PLANNING"

            body_html = render_article_html(spec)
            pub_time = base_time - timedelta(hours=idx * 6)

            article, created = GuideArticle.objects.update_or_create(
                slug=spec["slug"],
                defaults={
                    "title": spec["title"],
                    "seo_title": spec["seo_title"][:70],
                    "meta_description": spec["meta_description"][:160],
                    "excerpt": spec["excerpt"][:255],
                    "body": body_html,
                    "author_name": "Mosety Editorial Team",
                    "reviewer_name": spec["reviewer"],
                    "content_type": ctype,
                    "published_at": pub_time,
                    "last_verified_at": timezone.now().date(),
                    "is_featured": spec.get("is_featured", False),
                    "is_active": True,
                },
            )
            linked_tours = [tour_map[s] for s in spec.get("tour_slugs", []) if s in tour_map]
            if linked_tours:
                article.related_tours.set(linked_tours)

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"GuideArticles processed: {created_count} created, {updated_count} updated "
                f"(Total active GuideArticles: {GuideArticle.objects.filter(is_active=True).count()})."
            )
        )

        # Fix legacy fee note on existing GuideArticle #6 if present
        existing_price_guide = GuideArticle.objects.filter(slug="boat-ride-prices-dock-guide-naivasha").first()
        if existing_price_guide:
            old_fee_text = "(KES 1,000 for Kenyan citizens, KES 1,500 residents, USD 30 non-residents)"
            new_fee_text = "(2026 official rates: Kenya Citizens KES 800 adult / KES 400 child; Kenya Residents KES 1,100 adult / KES 550 child; Non-Residents $33 USD adult / $22 student / $16 child; under 5 free)"
            if old_fee_text in existing_price_guide.body:
                existing_price_guide.body = existing_price_guide.body.replace(old_fee_text, new_fee_text)
            if not existing_price_guide.seo_title:
                existing_price_guide.seo_title = "Lake Naivasha Boat Ride Prices & Dock Guide (2026)"
            if not existing_price_guide.meta_description:
                existing_price_guide.meta_description = (
                    "2026 Karagita Pier boat ride prices on Lake Naivasha: private charters from KES 3,500/boat, "
                    "Crescent Island transfers KES 5,000, and official 2026 gate fees."
                )
            existing_price_guide.last_verified_at = timezone.now().date()
            existing_price_guide.save()
            self.stdout.write("Updated existing GuideArticle 'boat-ride-prices-dock-guide-naivasha' with verified 2026 fees & meta.")

        # Upsert exact PAA questions into QuestionAnswer
        qa_created = 0
        qa_updated = 0
        # Shift older un-ordered FAQs lower so our top PAA items lead the homepage & FAQ hub
        QuestionAnswer.objects.filter(sort_order__lte=6).update(sort_order=20)
        for sort_order, category, question, answer, tour_slug in PAA_FAQS:
            qa, created = QuestionAnswer.objects.update_or_create(
                question=question,
                defaults={
                    "category": category,
                    "answer": answer,
                    "related_tour": tour_map.get(tour_slug),
                    "sort_order": sort_order,
                    "last_verified_at": timezone.now().date(),
                    "is_active": True,
                },
            )
            if created:
                qa_created += 1
            else:
                qa_updated += 1
        self.stdout.write(f"PAA QuestionAnswers synced: {qa_created} created, {qa_updated} updated.")

        # Refresh & normalize InternalLink table to canonical Mosety URLs
        legacy_url_rewrites = [
            ("/tours/sunset-cruise/", "/boat-rides/sunset-cruise/"),
            ("/tours/crescent-island-family-transfer/", "/boat-rides/crescent-island/"),
            ("/tours/hippo-safari-and-bird-watching/", "/boat-rides/hippo-bird-safari/"),
            ("/tours/", "/boat-rides/"),
            ("/destinations/crescent-island-naivasha/", "/crescent-island/"),
            ("/crescent-island-tours/", "/crescent-island/"),
            ("/seo/crescent-island-walking-safari/", "/crescent-island/"),
            ("/seo/karagita-public-beach/", "/contact/"),
            ("/seo/hells-gate-lake-naivasha-boat-ride-combo/", "/journal/combining-hells-gate-and-crescent-island-boat-ride-in-one-day/"),
            ("/blog/crescent-island-tour-walking-safari-naivasha/", "/crescent-island/"),
            ("/blog/", "/journal/"),
        ]
        rewritten_links = 0
        for old_url, new_url in legacy_url_rewrites:
            cnt = InternalLink.objects.filter(url=old_url).update(url=new_url)
            rewritten_links += cnt

        # Deactivate obsolete competitor-named legacy InternalLink entries if any
        InternalLink.objects.filter(keyword__in=["Boffar Boat Safaris", "Gitoh B", "Marina Boat Safaris"]).update(is_active=False)

        il_created = 0
        il_updated = 0
        for keyword, url in CANONICAL_INTERNAL_LINKS:
            existing = InternalLink.objects.filter(keyword__iexact=keyword).first()
            if existing:
                if existing.url != url or not existing.is_active:
                    existing.url = url
                    existing.is_active = True
                    existing.save(update_fields=["url", "is_active"])
                    il_updated += 1
            else:
                InternalLink.objects.create(keyword=keyword, url=url, is_active=True)
                il_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"InternalLinks upgraded: {rewritten_links} legacy paths canonicalized, "
                f"{il_created} created, {il_updated} updated "
                f"(Total active: {InternalLink.objects.filter(is_active=True).count()})."
            )
        )
