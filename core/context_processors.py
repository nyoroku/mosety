from .models import SiteSettings
from seo.utils import clean_canonical_url


def mosety_site_context(request):
    """
    Global context processor injecting Mosety SiteSettings, clean canonical URLs,
    and verified business details.
    """
    site = SiteSettings.get_solo()
    canonical = clean_canonical_url(request)

    primary_nav = [
        {'title': 'Boat Rides & Services', 'url': '/boat-rides/'},
        {'title': 'Crescent Island', 'url': '/crescent-island/'},
        {'title': 'Prices', 'url': '/prices/'},
        {'title': 'Plan Your Visit', 'url': '/plan-your-visit/'},
        {'title': 'Naivasha Guide', 'url': '/naivasha-guide/'},
        {'title': 'Journal & Blog', 'url': '/journal/'},
        {'title': 'About', 'url': '/about/'},
    ]

    whatsapp_book_url = site.build_whatsapp_url(
        "Hi Mosety. I would like to book a Lake Naivasha boat ride. Please share availability."
    )

    return {
        'site': site,
        'canonical_url': canonical,
        'primary_nav': primary_nav,
        'whatsapp_book_url': whatsapp_book_url,
        'analytics': {
            'ga4_id': site.ga4_measurement_id,
            'gsc_code': site.gsc_verification_code,
            'bing_code': site.bing_verification_code,
        }
    }
