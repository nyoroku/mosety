from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse
from django.shortcuts import redirect
from .models import ResourceCategory, GuidePage, FAQItem, PricingTier


def featured_guide(category_slug='ultimate-guides'):
    """Return a stable internal target for legacy resource links."""
    guide = GuidePage.objects.filter(
        is_active=True,
        allow_indexing=True,
        category__slug=category_slug,
    ).order_by('is_pillar', 'id').first()
    return guide or GuidePage.objects.filter(
        is_active=True,
        allow_indexing=True,
    ).order_by('is_pillar', 'id').first()

class ResourcesLandingView(ListView):
    model = ResourceCategory
    template_name = 'resources/landing.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return ResourceCategory.objects.filter(is_active=True).order_by('sort_order').prefetch_related('guide_pages')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_title'] = 'Resources & Travel Guides | Paradise Boat Rides'
        context['meta_description'] = 'Your complete guide to affordable Lake Naivasha boat rides. Transparent pricing, trip planning, safety information, wildlife guides, and local attractions.'
        context['canonical_url'] = self.request.build_absolute_uri()
        context['featured_guide'] = featured_guide()
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse('pages:home')},
            {'name': 'Resources'}
        ]
        return context

class PricingView(TemplateView):
    template_name = 'resources/pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        guide_page = GuidePage.objects.filter(slug='pricing', is_active=True).first()
        context['pricing_tiers'] = PricingTier.objects.filter(is_active=True).order_by('sort_order')
        context['faq_items'] = FAQItem.objects.filter(is_active=True, category__slug='pricing')[:10]
        context['guide_page'] = guide_page
        context['featured_guide'] = featured_guide()
        context['meta_title'] = guide_page.meta_title if guide_page and guide_page.meta_title else 'Naivasha Boat Ride Prices — No Hidden Fees | Paradise'
        context['meta_description'] = guide_page.meta_description if guide_page and guide_page.meta_description else ''
        context['canonical_url'] = self.request.build_absolute_uri()
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse('pages:home')},
            {'name': 'Resources', 'url': reverse('resources:landing')},
            {'name': 'Pricing'}
        ]
        return context

class ResourceFAQView(ListView):
    model = FAQItem
    template_name = 'resources/faq.html'
    context_object_name = 'faq_items'
    paginate_by = 20

    def get_queryset(self):
        return FAQItem.objects.filter(is_active=True).order_by('sort_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        guide_page = GuidePage.objects.filter(slug='faq', is_active=True).first()
        context['guide_page'] = guide_page
        context['featured_guide'] = featured_guide()
        context['meta_title'] = guide_page.meta_title if guide_page and guide_page.meta_title else 'Lake Naivasha Boat Ride FAQ | Paradise Boat Rides'
        context['meta_description'] = guide_page.meta_description if guide_page and guide_page.meta_description else ''
        context['canonical_url'] = self.request.build_absolute_uri()
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse('pages:home')},
            {'name': 'Resources', 'url': reverse('resources:landing')},
            {'name': 'FAQ'}
        ]
        return context

class GuidePageDetailView(DetailView):
    model = GuidePage
    template_name = 'resources/guide_detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        return GuidePage.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        # These slugs were previously published in resource content and may
        # still be present in search indexes or external links. Redirect them
        # to the current database-backed guide instead of returning a 404.
        legacy_categories = {
            'ultimate-guide-naivasha-boat-rides': 'ultimate-guides',
            'trip-planning': 'trip-planning',
        }
        slug = kwargs.get('slug', '')
        category_slug = legacy_categories.get(slug)
        if category_slug and not GuidePage.objects.filter(
            slug=slug, is_active=True, allow_indexing=True
        ).exists():
            target = featured_guide(category_slug)
            if target:
                return redirect('resources:guide_detail', slug=target.slug, permanent=True)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.object
        context['meta_title'] = page.effective_meta_title
        context['meta_description'] = page.meta_description
        context['canonical_url'] = self.request.build_absolute_uri()
        context['related_guides'] = GuidePage.objects.filter(is_active=True, allow_indexing=True).exclude(id=page.id)[:6]
        context['faq_items'] = page.faq_items.filter(is_active=True)
        context['pricing_tiers'] = PricingTier.objects.filter(is_active=True)[:3]
        context['featured_guide'] = featured_guide()
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse('pages:home')},
            {'name': 'Resources', 'url': reverse('resources:landing')},
            {'name': page.category.name, 'url': None},
            {'name': page.title}
        ]
        return context
