import json
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from core.models import SiteSettings
from tours.models import Tour
from .models import Captain, GuideArticle, QuestionAnswer, Testimonial
from seo.utils import build_faq_schema


class CrescentIslandView(TemplateView):
    template_name = 'content/crescent_island.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        tour = Tour.objects.filter(slug='crescent-island', is_active=True).first()
        
        wa_message = "Hi Mosety. I would like to book the Crescent Island boat ride & walking safari. Please share availability."
        context.update({
            'site': site,
            'tour': tour,
            'tour_whatsapp_url': site.build_whatsapp_url(wa_message),
            'faqs': QuestionAnswer.objects.filter(is_active=True, question__icontains='crescent')[:6],
            'meta_title': f"Crescent Island Boat Ride & Walking Safari Guide — {site.business_name}",
            'meta_description': (
                "Complete guide to visiting Crescent Island Sanctuary on Lake Naivasha. "
                "Boat charter rates, sanctuary gate walking fees, wildlife encounters (giraffes, zebras), and departure logistics."
            ),
        })
        return context


class SafetyStandardsView(TemplateView):
    template_name = 'content/safety.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Safety Standards & Hippo Buffer Protocols — {site.business_name}",
            'meta_description': (
                "Mosety safety standards on Lake Naivasha: Mandatory fitted life jackets for all ages, "
                "certified local captains, 30–50m ethical hippo buffers, and weather-first wind policies."
            ),
            'safety_faqs': QuestionAnswer.objects.filter(category='Safety', is_active=True),
        })
        return context


class CaptainsListView(ListView):
    model = Captain
    template_name = 'content/captains.html'
    context_object_name = 'captains'

    def get_queryset(self):
        return Captain.objects.filter(is_active=True).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Meet Our Licensed Local Captains — {site.business_name}",
            'meta_description': (
                "Meet the experienced local captains guiding Mosety boat rides on Lake Naivasha. "
                "Decades of navigation experience, certified marine safety, and birding specialists."
            ),
        })
        return context


class ReviewsListView(ListView):
    model = Testimonial
    template_name = 'content/reviews.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Testimonial.objects.filter(is_active=True).order_by('-review_date', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Guest Stories & Verified Reviews — {site.business_name}",
            'meta_description': (
                "Real reviews from guests who experienced Lake Naivasha boat rides with Mosety. "
                "Factual feedback, transparent pier rates, and verified wildlife safaris."
            ),
        })
        return context


class AboutView(TemplateView):
    template_name = 'content/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"About Mosety Boat Rides Naivasha — Our Lake Lineage",
            'meta_description': (
                "Learn about Mosety Boat Rides Naivasha: A collective of local captains operating from Karagita Beach "
                "committed to transparent pier rates, fitted safety vests, and ethical hippo observation."
            ),
        })
        return context


class ContactLocationView(TemplateView):
    template_name = 'content/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Location, Pier Directions & Contact — {site.business_name}",
            'meta_description': (
                "Find Mosety Boat Rides at Karagita Public Beach, South Lake Road, Lake Naivasha. "
                "GPS coordinates, driving directions from Nairobi and Nakuru, parking information, and contact numbers."
            ),
        })
        return context


class FAQHubView(TemplateView):
    template_name = 'content/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        all_faqs = QuestionAnswer.objects.filter(is_active=True).order_by('sort_order', 'id')
        
        categories = {}
        for faq in all_faqs:
            cat = faq.get_category_display() if hasattr(faq, 'get_category_display') else faq.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(faq)

        faq_pairs = [(faq.question, faq.answer) for faq in all_faqs]
        faq_schema = build_faq_schema(faq_pairs) if faq_pairs else ""

        context.update({
            'site': site,
            'categories': categories,
            'all_faqs': all_faqs,
            'faq_schema': json.dumps(faq_schema) if faq_schema else "",
            'meta_title': f"Lake Naivasha Boat Rides FAQ — Questions Answered — {site.business_name}",
            'meta_description': (
                "Answers to common questions about Lake Naivasha boat rides: Prices, hippo safety distances, "
                "Crescent Island tickets, departure times, and children safety."
            ),
        })
        return context


class PlanYourVisitHubView(TemplateView):
    template_name = 'content/plan_hub.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Plan Your Visit to Lake Naivasha — Complete Traveler Guide — {site.business_name}",
            'meta_description': (
                "Everything you need to plan a trip to Lake Naivasha: Getting here from Nairobi, "
                "best time of day for calm waters, packing checklist, children safety, and local pier tips."
            ),
        })
        return context


class PlanGettingHereView(TemplateView):
    template_name = 'content/plan_getting_here.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Getting to Lake Naivasha from Nairobi — Driving & Matatu Directions — {site.business_name}",
            'meta_description': (
                "Step-by-step travel guide from Nairobi to Karagita Beach, Lake Naivasha. "
                "Driving route via Mai Mahiu (A104/B3), Matatu options, travel times, and pier arrival tips."
            ),
        })
        return context


class PlanBestTimeToVisitView(TemplateView):
    template_name = 'content/plan_best_time.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Best Time of Day & Seasons for Lake Naivasha Boat Rides — {site.business_name}",
            'meta_description': (
                "When to take a boat ride on Lake Naivasha: Why morning (06:30–10:30 AM) offers mirror-calm waters, "
                "golden hour sunset conditions, and seasonal weather patterns."
            ),
        })
        return context


class PlanWhatToBringView(TemplateView):
    template_name = 'content/plan_what_to_bring.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"What to Bring on a Lake Naivasha Boat Safari — Packing Guide — {site.business_name}",
            'meta_description': (
                "Essential checklist for your Lake Naivasha boat ride: Sun protection, windbreaker layers, "
                "sturdy walking shoes for Crescent Island, camera gear, and dry bags."
            ),
        })
        return context


class PlanChildrenSafetyView(TemplateView):
    template_name = 'content/plan_children.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Visiting Lake Naivasha with Children — Family Boat Rides & Safety — {site.business_name}",
            'meta_description': (
                "A parent's guide to Lake Naivasha boat rides: Fitted infant and toddler life jackets, "
                "gentle wildlife observation, stroller advice for Crescent Island, and safe boarding."
            ),
        })
        return context


class NaivashaGuideHubView(TemplateView):
    template_name = 'content/guide_hub.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Lake Naivasha Destination Authority Guide — {site.business_name}",
            'meta_description': (
                "Comprehensive authority guide to Lake Naivasha: Freshwater Great Rift Valley ecology, "
                "resident hippo pods, 400+ bird species, Crescent Island walking safaris, and local boat docks."
            ),
        })
        return context


class NaivashaHipposView(TemplateView):
    template_name = 'content/guide_hippos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Lake Naivasha Hippos — Pod Locations & Ethical Viewing — {site.business_name}",
            'meta_description': (
                "Field guide to viewing hippopotamuses in Lake Naivasha: Pod behaviors, day-sleeping shallows, "
                "night grazing habits, and strict 30–50 meter boat safety buffers."
            ),
        })
        return context


class NaivashaBirdsView(TemplateView):
    template_name = 'content/guide_birds.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Lake Naivasha Birds & Fish Eagles — 400+ Species Guide — {site.business_name}",
            'meta_description': (
                "Bird watching on Lake Naivasha: African fish eagles, pelicans, cormorants, kingfishers, "
                "and goliath herons. Best morning photography angles and papyrus channel vantage points."
            ),
        })
        return context


class NaivashaWildlifeView(TemplateView):
    template_name = 'content/guide_wildlife.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Lake Naivasha Wildlife Guide — Animals of Crescent Island & Shoreline — {site.business_name}",
            'meta_description': (
                "Discover the animals of Lake Naivasha: Walking among Maasai giraffes, zebras, waterbucks, "
                "and impalas on Crescent Island, plus shoreline wildlife and colobus monkeys."
            ),
        })
        return context


class JournalListView(ListView):
    model = GuideArticle
    template_name = 'content/journal_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return GuideArticle.objects.filter(is_active=True, content_type='JOURNAL').order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'meta_title': f"Captains Journal & Field Notes — {site.business_name}",
            'meta_description': (
                "First-hand observations, navigation notes, and wildlife tracking from local boat captains on Lake Naivasha."
            ),
        })
        return context


class JournalDetailView(DetailView):
    model = GuideArticle
    template_name = 'content/journal_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return GuideArticle.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SiteSettings.get_solo()
        context.update({
            'site': site,
            'related_articles': GuideArticle.objects.filter(is_active=True).exclude(id=self.object.id)[:3],
        })
        return context
