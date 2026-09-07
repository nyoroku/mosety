from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.db.models import Avg, Count, Q
from utils import get_client_ip, is_resident_ip

from .models import Tour, Booking
from .forms import BookingForm


class TourListView(ListView):
    model = Tour
    template_name = 'bookings/tour_list.html'
    context_object_name = 'tours'
    paginate_by = 6

    def get_queryset(self):
        return Tour.objects.filter(is_active=True, allow_indexing=True).annotate(
            average_rating=Avg('testimonials__rating', filter=Q(testimonials__is_active=True)),
            review_count=Count('testimonials', filter=Q(testimonials__is_active=True)),
        ).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        ip = get_client_ip(self.request)
        is_resident = is_resident_ip(ip)
        currency_symbol = "KES" if is_resident else "$"
        
        tours = list(context['tours'])
        for tour in tours:
            tour.display_price = tour.price_resident if is_resident else tour.price_international
            
        context.update({
            'tours': tours,
            'currency_symbol': currency_symbol,
            "seo_title": "Boat Rides in Naivasha | Paradise Boat Rides",
            "meta_description": (
                "Explore the best boat rides on Lake Naivasha. "
                "Sunset cruises, birthday boat rides, group tours and private experiences."
            ),
            "h1": "Boat Rides in Naivasha",
            "intro_text": (
                "Choose from curated boat ride experiences on Lake Naivasha — "
                "perfect for couples, families, birthdays and group outings."
            ),
        })

        return context


class TourDetailRedirectView(View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        ip = get_client_ip(request)

        if 'katrue' in slug.lower():
            current_slug = slug.lower().replace('katrue', 'paradise-boat-rides-naivasha')
            if Tour.objects.filter(slug=current_slug, is_active=True).exists():
                view_name = 'bookings:tour_detail_resident' if is_resident_ip(ip) else 'bookings:tour_detail_international'
                return redirect(view_name, slug=current_slug, permanent=True)
        
        if is_resident_ip(ip):
            return redirect('bookings:tour_detail_resident', slug=slug)
        else:
            return redirect('bookings:tour_detail_international', slug=slug)


class TourDetailView(DetailView):
    model = Tour
    template_name = 'bookings/tour_detail.html'
    context_object_name = 'tour'

    def get_object(self):
        tour = get_object_or_404(
            Tour,
            slug=self.kwargs['slug'],
            is_active=True,
        )

        if not tour.allow_indexing:
            raise Http404()

        return tour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.object
        visitor_type = self.kwargs.get('visitor_type', 'RESIDENT')
        
        # Currency and Price Logic
        if visitor_type == 'INTERNATIONAL':
            price = tour.price_international
            currency_symbol = "$"
            currency_code = "USD"
        else:
            price = tour.price_resident
            currency_symbol = "KES"
            currency_code = "KES"

        context.update({
            "booking_form": BookingForm(initial={
                'visitor_type': visitor_type,
                'currency': currency_code
            }),
            "visitor_type": visitor_type,
            "display_price": price,
            "currency_symbol": currency_symbol,
            "currency_code": currency_code,

            # SEO
            "seo_title": tour.effective_seo_title,
            "meta_description": tour.meta_description or (
                f"{tour.name} on Lake Naivasha. "
                f"Duration: {tour.duration_hours} hrs. "
                f"Price from {currency_symbol} {price} per person."
            ),

            # Internal linking (critical for SEO)
            "related_tours": Tour.objects.filter(
                is_active=True,
                allow_indexing=True
            ).exclude(id=tour.id)[:4],

            # Conversion cues
            "cta_text": "Book this boat ride",
        })
        review_summary = tour.testimonials.filter(is_active=True).aggregate(
            average=Avg('rating'),
            count=Count('id'),
        )
        context['average_rating'] = review_summary['average']
        context['review_count'] = review_summary['count']

        return context


class CreateBookingView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/partials/booking_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tour'] = get_object_or_404(Tour, slug=self.kwargs['slug'], is_active=True)
        return kwargs


    def get_initial(self):
        initial = super().get_initial()
        from .utils import get_client_ip, is_resident_ip
        ip = get_client_ip(self.request)
        is_resident = is_resident_ip(ip)
        
        # Priority: POST > GET > GeoIP
        visitor_type = self.request.POST.get('visitor_type') or \
                       self.request.GET.get('visitor_type') or \
                       ('RESIDENT' if is_resident else 'INTERNATIONAL')
        
        initial['visitor_type'] = visitor_type
        initial['currency'] = 'KES' if visitor_type == 'RESIDENT' else 'USD'
        initial['referral_code'] = self.request.POST.get('referral_code') or self.request.GET.get('ref')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = get_object_or_404(Tour, slug=self.kwargs['slug'], is_active=True)
        
        # Determine visitor type from form initial or POST
        visitor_type = self.request.POST.get('visitor_type') or self.request.GET.get('visitor_type', 'RESIDENT')
        if visitor_type == 'INTERNATIONAL':
            price = tour.price_international
            currency_symbol = "$"
            currency_code = "USD"
        else:
            price = tour.price_resident
            currency_symbol = "KES"
            currency_code = "KES"

        context.update({
            'tour': tour,
            'display_price': price,
            'currency_symbol': currency_symbol,
            'currency_code': currency_code,
        })
        return context

    def form_valid(self, form):
        tour = get_object_or_404(
            Tour,
            slug=self.kwargs['slug'],
            is_active=True
        )

        form.instance.tour = tour


class CreateBookingView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/partials/booking_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tour'] = get_object_or_404(Tour, slug=self.kwargs['slug'], is_active=True)
        return kwargs


    def get_initial(self):
        initial = super().get_initial()
        from .utils import get_client_ip, is_resident_ip
        ip = get_client_ip(self.request)
        is_resident = is_resident_ip(ip)
        
        # Priority: POST > GET > GeoIP
        visitor_type = self.request.POST.get('visitor_type') or \
                       self.request.GET.get('visitor_type') or \
                       ('RESIDENT' if is_resident else 'INTERNATIONAL')
        
        initial['visitor_type'] = visitor_type
        initial['currency'] = 'KES' if visitor_type == 'RESIDENT' else 'USD'
        initial['referral_code'] = self.request.POST.get('referral_code') or self.request.GET.get('ref')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = get_object_or_404(Tour, slug=self.kwargs['slug'], is_active=True)
        
        # Determine visitor type from form initial or POST
        visitor_type = self.request.POST.get('visitor_type') or self.request.GET.get('visitor_type', 'RESIDENT')
        if visitor_type == 'INTERNATIONAL':
            price = tour.price_international
            currency_symbol = "$"
            currency_code = "USD"
        else:
            price = tour.price_resident
            currency_symbol = "KES"
            currency_code = "KES"

        context.update({
            'tour': tour,
            'display_price': price,
            'currency_symbol': currency_symbol,
            'currency_code': currency_code,
        })
        return context

    def form_valid(self, form):
        tour = get_object_or_404(
            Tour,
            slug=self.kwargs['slug'],
            is_active=True
        )

        form.instance.tour = tour
        
        # Calculate total price based on visitor type
        visitor_type = form.cleaned_data.get('visitor_type', 'RESIDENT')
        form.instance.referral_code = form.cleaned_data.get('referral_code')
        price = tour.price_resident if visitor_type == 'RESIDENT' else tour.price_international
        form.instance.total_price = (price * form.cleaned_data['number_of_people'])

        messages.success(
            self.request,
            "Booking request received. Our team will contact you shortly."
        )

        if self.request.headers.get('HX-Request'):
            return render(self.request, 'bookings/partials/booking_success_msg.html', {
                'tour': tour,
                'total_price': form.instance.total_price,
                'currency': form.instance.currency
            })

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the appropriate variant
        visitor_type = self.request.POST.get('visitor_type', 'RESIDENT')
        view_name = 'bookings:tour_detail_resident' if visitor_type == 'RESIDENT' else 'bookings:tour_detail_international'
        return reverse(view_name, kwargs={'slug': self.kwargs['slug']})


def booking_success_view(request):
    return render(request, 'bookings/booking_success.html', {
        "seo_title": "Booking Received | Paradise Boat Rides",
        "meta_description": "Your booking request has been received. We will contact you shortly."
    })


# ---------------- MOSETY BOOKING LEAD FLOW ----------------
from .forms import BookingLeadForm
from .models import BookingLead
from core.models import SiteSettings
from tours.models import Tour as MosetyTour


class BookLeadView(View):
    def get(self, request, *args, **kwargs):
        tour_slug = kwargs.get('slug') or request.GET.get('tour')
        initial = {}
        selected_tour = None
        if tour_slug:
            selected_tour = MosetyTour.objects.filter(slug=tour_slug, is_active=True).first()
            if selected_tour:
                initial['tour'] = selected_tour

        form = BookingLeadForm(initial=initial)
        site = SiteSettings.get_solo()
        return render(request, 'bookings/book.html', {
            'form': form,
            'selected_tour': selected_tour,
            'site': site,
            'meta_title': f"Book a Lake Naivasha Boat Ride — {site.business_name}",
            'meta_description': "Reserve your Lake Naivasha boat ride directly with Mosety. Transparent pricing, fitted life jackets, and experienced local captains.",
        })

    def post(self, request, *args, **kwargs):
        form = BookingLeadForm(request.POST)
        site = SiteSettings.get_solo()
        if form.is_valid():
            lead = form.save(commit=False)
            
            # Apply UTM attribution
            utm = request.session.get('utm_data', {})
            lead.utm_source = utm.get('utm_source', '')
            lead.utm_medium = utm.get('utm_medium', '')
            lead.utm_campaign = utm.get('utm_campaign', '')
            lead.utm_term = utm.get('utm_term', '')
            lead.utm_content = utm.get('utm_content', '')
            lead.landing_page = utm.get('landing_page', '')
            lead.referrer = utm.get('referrer', '')

            # Compute estimate total
            if lead.tour:
                tiers = lead.tour.price_tiers.filter(is_active=True)
                tier = tiers.filter(pricing_mode='PER_PERSON').first() if lead.booking_type == 'SHARED' else tiers.filter(pricing_mode='PER_BOAT').first()
                if not tier:
                    tier = tiers.first()
                if tier:
                    lead.estimated_total = tier.amount_kes * (lead.party_size if tier.pricing_mode == 'PER_PERSON' else 1)

            lead.save()
            wa_url = lead.build_whatsapp_continuation_url(site)

            context = {
                'lead': lead,
                'whatsapp_url': wa_url,
                'site': site,
            }
            if request.headers.get('HX-Request'):
                return render(request, 'bookings/partials/booking_success.html', context)
            return render(request, 'bookings/booking_success.html', context)

        return render(request, 'bookings/book.html', {'form': form, 'site': site})
