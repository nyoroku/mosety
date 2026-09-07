import json
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from django.utils.safestring import mark_safe
from core.models import SiteSettings


TRACKING_PARAMS = {
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'gclid', 'fbclid', 'msclkid', 'ref', 'source', 'mc_cid', 'mc_eid'
}


def clean_canonical_url(request, override_url=None):
    """
    Builds a pristine canonical URL by stripping all marketing and click tracking query parameters.
    Only explicit pagination (?page=N where N > 1) is preserved.
    """
    site = SiteSettings.get_solo()
    base_url = (site.base_url or "https://mosety.co.ke").rstrip('/')

    if override_url:
        if override_url.startswith('http'):
            parsed = urlparse(override_url)
            return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
        return f"{base_url}{override_url}"

    parsed_path = request.path
    query_params = request.GET.copy()

    # Strip all tracking parameters
    for param in TRACKING_PARAMS:
        query_params.pop(param, None)

    # Clean query string
    page = query_params.get('page')
    clean_query = {}
    if page and page.isdigit() and int(page) > 1:
        clean_query['page'] = page

    query_str = urlencode(clean_query)
    if query_str:
        return f"{base_url}{parsed_path}?{query_str}"
    return f"{base_url}{parsed_path}"


def render_json_ld(data):
    """
    Safely serializes a Python dictionary to JSON for embedding in <script type="application/ld+json">.
    """
    return mark_safe(json.dumps(data, indent=2, ensure_ascii=False))


def build_local_business_schema(site):
    """
    Generates structured data for Mosety Boat Rides Naivasha LocalBusiness entity.
    """
    base_url = (site.base_url or "https://mosety.co.ke").rstrip('/')
    schema = {
        "@context": "https://schema.org",
        "@type": ["TouristAttraction", "LocalBusiness"],
        "@id": f"{base_url}/#business",
        "name": site.business_name,
        "legalName": site.legal_name,
        "description": site.tagline,
        "url": f"{base_url}/",
        "telephone": site.phone_e164,
        "email": site.email,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": site.address_text,
            "addressLocality": "Naivasha",
            "addressRegion": "Nakuru County",
            "addressCountry": "KE"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": float(site.latitude),
            "longitude": float(site.longitude)
        },
        "openingHours": "Mo-Su 06:30-18:30",
        "priceRange": site.default_currency,
        "currenciesAccepted": "KES, USD",
        "paymentAccepted": "Cash, M-PESA, Credit Card",
        "areaServed": {
            "@type": "Place",
            "name": "Lake Naivasha, Nakuru County, Kenya"
        }
    }
    if site.logo:
        schema["logo"] = f"{base_url}{site.logo.url}"
    return schema


def build_faq_schema(faq_list):
    """
    Builds FAQPage JSON-LD schema from question/answer tuples or objects.
    """
    items = []
    for item in faq_list:
        if isinstance(item, dict):
            q, a = item.get('question'), item.get('answer')
        elif hasattr(item, 'question') and hasattr(item, 'answer'):
            q, a = item.question, getattr(item, 'plain_answer', None) or item.answer
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            q, a = item[0], item[1]
        else:
            continue
        if q and a:
            items.append({
                "@type": "Question",
                "name": str(q),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": str(a)
                }
            })
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items
    }


def build_breadcrumb_schema(breadcrumb_list, site):
    """
    Builds BreadcrumbList schema from a list of {'name': ..., 'url': ...}.
    """
    base_url = (site.base_url or "https://mosety.co.ke").rstrip('/')
    elements = []
    for i, item in enumerate(breadcrumb_list, 1):
        url = item.get('url') or ""
        if url and not url.startswith('http'):
            url = f"{base_url}{url}"
        element = {
            "@type": "ListItem",
            "position": i,
            "name": item.get('name', '')
        }
        if url:
            element["item"] = url
        elements.append(element)

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements
    }
