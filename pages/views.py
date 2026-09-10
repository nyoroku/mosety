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
        faqs = list(QuestionAnswer.objects.filter(is_active=True).order_by('sort_order')[:8])
        journal_articles = list(GuideArticle.objects.filter(is_active=True).order_by('-published_at')[:3])

        context.update({
            'site': site,
            'all_tours': all_tours,
            'featured_tours': featured_tours,
            'pricing_tours': pricing_tours,
            'journal_articles': journal_articles,
            'default_tour': default_tour,
            'captains': captains,
            'testimonials': testimonials,
            'faqs': faqs,
            'local_business_schema': render_json_ld(build_local_business_schema(site)),
            'faq_schema': render_json_ld(build_faq_schema(faqs)),
        })
        return context



def robots_txt(request):
    site = SiteSettings.get_solo()
    base_url = (site.base_url or "https://mosety.co.ke").rstrip('/')
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
    base_url = (site.base_url or "https://mosety.co.ke").rstrip('/')
    lines = [
        f'# {site.business_name}', '',
        f'> {site.tagline}',
        '> Local lake experiences, clearly priced and expertly guided on Lake Naivasha.', '',
        '## Boat Rides',
    ]
    lines.extend(f'- {tour.name}: {base_url}{tour.get_absolute_url()}' for tour in Tour.objects.filter(is_active=True, allow_indexing=True))
    lines.extend(['', '## Key Links', f'- Homepage: {base_url}/', f'- Boat Rides: {base_url}/boat-rides/', f'- Prices: {base_url}/prices/', f'- Plan Your Visit: {base_url}/plan-your-visit/', f'- Naivasha Guide: {base_url}/naivasha-guide/', '', '## Contact', f'WhatsApp: {site.whatsapp_number}', f'Phone: {site.phone}', f'Location: {site.address_text}'])
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
            contact_form.save() # If you want to save it to a model
            # For now, we'll just show a success message
            messages.success(request, f"Thank you, {contact_form.cleaned_data['name']}. Your message has been received. We'll get back to you soon!")
            # In a real project, you would send an email here using Django's email backend.
            # from django.core.mail import send_mail
            # send_mail(
            #     contact_form.cleaned_data['subject'],
            #     contact_form.cleaned_data['message'],
            #     contact_form.cleaned_data['email'],
            #     ['your-email@paradiseboatridesnaivasha.com'],
            #     fail_silently=False,
            # )
        else:
            messages.error(request, "There was an error with your submission. Please check the fields and try again.")

        # For HTMX, we re-render the form with the message
        return render(request, 'pages/partials/contact_form.html', {'contact_form': contact_form})
