import json

from django.conf import settings
from django.db.models import Avg, Count, Q
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import strip_tags
from bookings.models import Tour
from seo.models import FAQ, LocalPage
from services.models import Service
from blog.models import Post
from testimonials.models import Testimonial
from accommodation.models import PartnerHotel
from .forms import ContactForm
from core.models import SiteSettings
from seo.utils import build_local_business_schema, build_faq_schema, render_json_ld
from utils import get_client_ip, is_resident_ip


from tours.models import Tour as MosetyTour
from content.models import Captain, Testimonial as ContentTestimonial, QuestionAnswer, GuideArticle


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()

        # Mosety database-backed data
        all_tours = list(MosetyTour.objects.filter(is_active=True).prefetch_related('price_tiers').order_by('sort_order'))
        featured_tours = [t for t in all_tours if t.is_featured]
        if not featured_tours:
            featured_tours = all_tours[:4]
            
        # 3 highlight experiences for the dynamic Pricing Snapshot
        pricing_tours = [t for t in all_tours if t.slug in ['hippo-bird-safari', 'crescent-island', 'sunset-cruise']]
        if len(pricing_tours) < 3:
            pricing_tours = all_tours[:3]

        default_tour = MosetyTour.objects.filter(slug='hippo-bird-safari', is_active=True).first() or (all_tours[0] if all_tours else None)
        captains = Captain.objects.filter(is_active=True).order_by('-years_on_lake')[:2]
        testimonials = list(ContentTestimonial.objects.filter(is_active=True).order_by('-is_featured', '-review_date')[:6])
        faqs = list(QuestionAnswer.objects.filter(is_active=True).order_by('sort_order', 'id')[:10])
        journal_articles = list(GuideArticle.objects.filter(is_active=True).order_by('-is_featured', '-published_at')[:6])
        popular_guides = list(GuideArticle.objects.filter(is_active=True).order_by('-is_featured', '-published_at')[6:18])

        context.update({
            'site': site,
            'all_tours': all_tours,
            'featured_tours': featured_tours,
            'pricing_tours': pricing_tours,
            'journal_articles': journal_articles,
            'popular_guides': popular_guides,
            'default_tour': default_tour,
            'captains': captains,
            'testimonials': testimonials,
            'faqs': faqs,
            'local_business_schema': render_json_ld(build_local_business_schema(site)),
            'faq_schema': render_json_ld(build_faq_schema(faqs)),
        })
        return context



def _get_public_base_url(request, site):
    host = request.get_host().split(':')[0]
    if 'mosetyboatridesnaivasha.co.ke' in host:
        return "https://www.mosetyboatridesnaivasha.co.ke"
    if site.base_url and 'pythonanywhere.com' not in site.base_url:
        return site.base_url.rstrip('/')
    return "https://www.mosetyboatridesnaivasha.co.ke"


def robots_txt(request):
    site = SiteSettings.get_solo()
    base_url = _get_public_base_url(request, site)
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /dashboard/',
        'Disallow: /tinymce/',
        '',
        f'Sitemap: {base_url}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')


def llms_txt(request):
    site = SiteSettings.get_solo()
    base_url = _get_public_base_url(request, site)
    lines = [
        f'# {site.business_name}', '',
        f'> {site.tagline}',
        '> Direct Lake Naivasha boat rides, Crescent Island transfers, hippo safaris, and sunset cruises departing Karagita Public Pier.', '',
        '## Verified 2026 Quick Facts (GEO / Answer Engine Reference)',
        '- Departure Pier: Karagita Public Beach Pier, South Lake Road, Lake Naivasha (GPS: -0.763400, 36.425800)',
        '- Operating Hours: Daily 06:30 AM – 06:30 PM (morning 06:30–10:30 AM offers the calmest water)',
        '- Lake Naivasha Entry Fee: None. There is no KWS park fee to access Lake Naivasha or take a boat ride from Karagita Pier.',
        '- Typical Boat Ride Prices (2026 Direct Pier Rates): Hippo & Bird Safari from KES 3,500/boat (1 hr, up to 7 guests); Family Boat Ride KES 4,000/boat; Private Boat Charter KES 4,500/boat; Crescent Island Boat Transfer + Waiting KES 5,000/boat (2.5–3 hrs total); Sunset Cruise KES 6,000/boat (1.5 hrs); Photography & Birding KES 7,000/boat; Group/Shared Rides from KES 1,000/person.',
        '- Crescent Island Sanctuary Gate Fees (2026, paid separately at island gate): Kenya Citizens KES 800 adult / KES 400 child; Kenya Residents KES 1,100 adult / KES 550 child; Non-Residents USD 33 adult / USD 22 student / USD 16 child; Under 5 free.',
        '- Licensed Local Captains: Captain Moses Kamau and Captain Joseph Njuguna.',
        '- Cancellation Policy: Free cancellation or rescheduling up to 2 hours before departure.',
        '',
        '## Boat Rides & Experiences',
    ]
    for tour in MosetyTour.objects.filter(is_active=True).order_by('sort_order'):
        lines.append(f'- {tour.name} (From KES {int(tour.starting_price_kes):,}, {tour.duration_display}): {base_url}{tour.get_absolute_url()}')
    for tour in Tour.objects.filter(is_active=True, allow_indexing=True):
        lines.append(f'- {tour.name}: {base_url}{tour.get_absolute_url()}')
    lines.extend([
        '',
        '## Key Authority Pages',
        f'- Homepage: {base_url}/',
        f'- All Boat Rides: {base_url}/boat-rides/',
        f'- Transparent Prices & Quote Calculator: {base_url}/prices/',
        f'- Crescent Island Boat & Walking Safari Guide: {base_url}/crescent-island/',
        f'- Guest Reviews: {base_url}/reviews/',
        f'- Safety Standards: {base_url}/safety/',
        f'- Meet Our Captains: {base_url}/captains/',
        f'- Frequently Asked Questions: {base_url}/questions/',
        f'- Plan Your Visit: {base_url}/plan-your-visit/',
        f'- Getting Here from Nairobi: {base_url}/plan-your-visit/getting-here/',
        f'- Best Time to Go: {base_url}/plan-your-visit/best-time-to-go/',
        f'- Naivasha Guide: {base_url}/naivasha-guide/',
        f'- Field Journal & Answer Hub: {base_url}/journal/',
        f'- Directions & Contact: {base_url}/contact/',
        '',
        '## Field Guides & Q&A Articles',
    ])
    for article in GuideArticle.objects.filter(is_active=True).order_by('-is_featured', '-published_at')[:60]:
        lines.append(f'- {article.title}: {base_url}{article.get_absolute_url()}')
    lines.extend([
        '',
        '## Contact',
        f'WhatsApp: {site.whatsapp_number}',
        f'Phone: {site.phone}',
        f'Email: {site.email}',
        f'Location: {site.address_text}',
    ])
    return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')



class ContactView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, f"Thank you, {contact_form.cleaned_data['name']}. Your message has been received. We'll get back to you soon!")
        else:
            messages.error(request, "There was an error with your submission. Please check the fields and try again.")
        return render(request, 'pages/partials/contact_form.html', {'contact_form': contact_form})


class SitemapView(TemplateView):
    template_name = 'pages/sitemap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        all_tours = list(MosetyTour.objects.filter(is_active=True).order_by('sort_order'))
        articles = list(GuideArticle.objects.filter(is_active=True).order_by('-is_featured', '-published_at'))
        faqs = list(QuestionAnswer.objects.filter(is_active=True).order_by('sort_order', 'id')[:12])
        context.update({
            'site': site,
            'all_tours': all_tours,
            'articles': articles,
            'faqs': faqs,
        })
        return context


class PrivacyPolicyView(TemplateView):
    template_name = 'pages/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = SiteSettings.get_solo()
        return context


class TermsOfServiceView(TemplateView):
    template_name = 'pages/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = SiteSettings.get_solo()
        return context
