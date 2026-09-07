from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from bookings.models import Tour
from .models import LocalPage, FAQ

# ---------------- Static Pages ----------------
class StaticViewSitemap(Sitemap):
    protocol = 'https'
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            'pages:home', 'pages:contact', 'seo:faq',
            'seo:list', 'bookings:tour_list', 'blog:post_list',
            'services:service_list', 'accommodation:hotel_list',
        ]

    def location(self, item):
        return reverse(item)


# ---------------- Tours ----------------
class TourSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0  # Tours are our main product

    def items(self):
        return Tour.objects.filter(is_active=True, allow_indexing=True)


# ---------------- Blog Posts ----------------
class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


# ---------------- Local Pages ----------------
class LocalPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return LocalPage.objects.filter(is_active=True, allow_indexing=True)

    def lastmod(self, obj):
        return obj.updated_at


# ---------------- FAQ ----------------
class FAQSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return FAQ.objects.filter(is_active=True, allow_indexing=True)

    def lastmod(self, obj):
        return obj.updated_at
