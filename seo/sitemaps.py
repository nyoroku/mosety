from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from tours.models import Tour as MosetyTour
from content.models import GuideArticle
from .models import LocalPage, FAQ

# ---------------- Static Pages ----------------
class StaticViewSitemap(Sitemap):
    protocol = 'https'
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'pages:home', 'content:contact', 'content:about', 'content:safety',
            'tours:tour_list', 'tours:prices', 'content:journal_list',
            'content:reviews', 'content:questions',
            'seo:faq', 'seo:list',
            'accommodation:hotel_list',
        ]

    def location(self, item):
        return reverse(item)


# ---------------- Tours ----------------
class TourSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return MosetyTour.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()


# ---------------- Guide Articles / Field Journal ----------------
class GuideArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return GuideArticle.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at


# ---------------- Blog Posts ----------------
class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


# ---------------- Local Pages ----------------
class LocalPageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return LocalPage.objects.filter(is_active=True, allow_indexing=True)

    def lastmod(self, obj):
        return obj.updated_at


# ---------------- FAQ ----------------
class FAQSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return FAQ.objects.filter(is_active=True, allow_indexing=True)

    def lastmod(self, obj):
        return obj.updated_at
