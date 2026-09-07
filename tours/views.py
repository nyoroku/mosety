from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Tour, PriceTier
from core.models import SiteSettings
from seo.utils import build_faq_schema, render_json_ld


class TourListView(ListView):
    model = Tour
    template_name = 'tours/tour_list.html'
    context_object_name = 'tours'

    def get_queryset(self):
        return Tour.objects.filter(is_active=True).order_by('sort_order', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'meta_title': f"Lake Naivasha Boat Rides & Safaris — {site.business_name}",
            'meta_description': (
                "Explore all 7 guided boat ride experiences on Lake Naivasha. "
                "Hippo safaris, Crescent Island transfers, sunset cruises and private charters with clear dock pricing."
            ),
        })
        return context


class TourDetailView(DetailView):
    model = Tour
    template_name = 'tours/tour_detail.html'
    context_object_name = 'tour'

    def get_queryset(self):
        return Tour.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.object
        site = SiteSettings.get_solo()
        
        # Prefilled WhatsApp message for this specific tour
        starting_price = tour.starting_price_kes
        price_str = f"KES {starting_price:,.0f}" if starting_price else "standard dock rate"
        wa_message = f"Hi Mosety. I'm interested in booking the {tour.name} ({tour.duration_display}). Starting rate: {price_str}. Please let me know availability."
        context['tour_whatsapp_url'] = site.build_whatsapp_url(wa_message)

        context['related_tours'] = Tour.objects.filter(is_active=True).exclude(id=tour.id).order_by('sort_order')[:3]
        context['faqs'] = tour.faqs.filter(is_active=True)

        return context


class FindYourRideView(View):
    """
    HTMX-driven intent recommendation engine.
    Maps visitor intent chips to curated Lake Naivasha boat rides.
    """
    INTENT_MAP = {
        'wildlife': {
            'slug': 'hippo-bird-safari',
            'reason': 'Best for close observation of wild hippo pods and watching African fish eagles hunt in the shallows.'
        },
        'crescent_island': {
            'slug': 'crescent-island',
            'reason': 'Combines a scenic lake cruise with an unhurried walking safari among giraffes and zebras.'
        },
        'sunset': {
            'slug': 'sunset-cruise',
            'reason': 'Depart during golden hour for mirror-calm waters and dramatic amber skies over the Mau Escarpment.'
        },
        'private': {
            'slug': 'private-boat',
            'reason': 'Exclusive boat charter with dedicated captain, customized itinerary, and complete privacy.'
        },
        'family': {
            'slug': 'family-boat-ride',
            'reason': 'Designed for all ages with fitted infant/child life jackets and gentle, educational wildlife guiding.'
        },
        'birding': {
            'slug': 'photography-birding',
            'reason': 'Dawn departure at 6:30 AM with drift positioning for serious raptor and waterbird photography.'
        }
    }

    def get(self, request, *args, **kwargs):
        intent = request.GET.get('intent', 'wildlife')
        return self.render_recommendation(request, intent)

    def post(self, request, *args, **kwargs):
        intent = request.POST.get('intent', 'wildlife')
        return self.render_recommendation(request, intent)

    def render_recommendation(self, request, intent):
        site = SiteSettings.get_solo()
        mapping = self.INTENT_MAP.get(intent, self.INTENT_MAP['wildlife'])
        tour = Tour.objects.filter(slug=mapping['slug'], is_active=True).first()
        
        if not tour:
            tour = Tour.objects.filter(is_active=True).first()

        context = {
            'tour': tour,
            'reason': mapping['reason'],
            'intent': intent,
            'site': site,
        }

        if request.headers.get('HX-Request'):
            return render(request, 'tours/partials/ride_recommendation.html', context)
        return render(request, 'tours/partials/ride_recommendation.html', context)


class PriceEstimateView(View):
    """
    HTMX Price Calculator endpoint.
    Computes accurate price estimates based on tour, party size, and private/shared mode.
    """
    def get(self, request, *args, **kwargs):
        return self.calculate(request, request.GET)

    def post(self, request, *args, **kwargs):
        return self.calculate(request, request.POST)

    def calculate(self, request, params):
        site = SiteSettings.get_solo()
        tour_id = params.get('tour_id')
        adults = int(params.get('adults', 2) or 2)
        children = int(params.get('children', 0) or 0)
        party_size = max(1, adults + children)
        booking_type = params.get('booking_type', 'PRIVATE')

        tour = None
        if tour_id:
            tour = Tour.objects.filter(id=tour_id, is_active=True).first()
        if not tour:
            tour = Tour.objects.filter(is_active=True).order_by('sort_order').first()

        # Find applicable tier
        tiers = tour.price_tiers.filter(is_active=True)
        chosen_tier = None

        if booking_type == 'SHARED':
            chosen_tier = tiers.filter(pricing_mode='PER_PERSON').first()

        if not chosen_tier:
            # Fall back to per-boat charter
            chosen_tier = tiers.filter(pricing_mode='PER_BOAT').first()

        if not chosen_tier:
            chosen_tier = tiers.first()

        if chosen_tier:
            if chosen_tier.pricing_mode == 'PER_PERSON':
                total_kes = chosen_tier.amount_kes * party_size
                per_person_kes = chosen_tier.amount_kes
            else:
                total_kes = chosen_tier.amount_kes
                per_person_kes = round(total_kes / Decimal(party_size), 0)
        else:
            total_kes = Decimal(3500)
            per_person_kes = round(total_kes / Decimal(party_size), 0)

        # Build contextual WhatsApp booking URL
        wa_message = (
            f"Hi Mosety. I calculated a website quote for {tour.name} for {party_size} guests "
            f"({booking_type.lower()}). Estimated quote: KES {total_kes:,.0f}. "
            f"Please confirm availability for my date."
        )
        whatsapp_url = site.build_whatsapp_url(wa_message)

        context = {
            'tour': tour,
            'tier': chosen_tier,
            'party_size': party_size,
            'adults': adults,
            'children': children,
            'booking_type': booking_type,
            'total_kes': total_kes,
            'per_person_kes': per_person_kes,
            'whatsapp_url': whatsapp_url,
            'site': site,
        }

        if request.headers.get('HX-Request'):
            return render(request, 'tours/partials/quote_result.html', context)
        return render(request, 'tours/partials/quote_result.html', context)


class PricesPageView(TemplateView):
    template_name = 'tours/prices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        tours = Tour.objects.filter(is_active=True).prefetch_related('price_tiers').order_by('sort_order')
        
        context.update({
            'site': site,
            'tours': tours,
            'meta_title': f"Lake Naivasha Boat Ride Prices & Calculator — {site.business_name}",
            'meta_description': (
                "Transparent, dock-direct Lake Naivasha boat ride prices. "
                "Calculate your exact cost for hippo safaris, Crescent Island transfers, and private charters with zero hidden fees."
            ),
        })
        return context
