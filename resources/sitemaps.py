from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import GuidePage

class ResourceGuideSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return GuidePage.objects.filter(is_active=True, allow_indexing=True)

    def lastmod(self, obj):
        return obj.updated_at

class ResourceStaticSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return ['resources:landing', 'resources:pricing', 'resources:faq']

    def location(self, item):
        return reverse(item)
