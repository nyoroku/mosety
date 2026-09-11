# boats/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap
from seo.sitemaps import StaticViewSitemap, BlogSitemap, LocalPageSitemap, FAQSitemap, TourSitemap, GuideArticleSitemap
from resources.sitemaps import ResourceGuideSitemap, ResourceStaticSitemap
sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'local': LocalPageSitemap,
    'faq': FAQSitemap,
    'tours': TourSitemap,
    'journal': GuideArticleSitemap,
    'resources': ResourceGuideSitemap,
    'resources_static': ResourceStaticSitemap,
}

from bookings.views import BookLeadView

def sitemap_clean_view(request, *args, **kwargs):
    response = sitemap(request, *args, **kwargs)
    if response.has_header('X-Robots-Tag'):
        del response['X-Robots-Tag']
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    path('', include('pages.urls')),
    path('', include('tours.urls')),
    path('', include('content.urls')),
    path('bookings/', include('bookings.urls')),
    path('book/', BookLeadView.as_view(), name='book_lead'),
    path('book/<slug:slug>/', BookLeadView.as_view(), name='book_tour_lead'),
    path('tours/', RedirectView.as_view(url='/boat-rides/', permanent=True)),
    path('services/', RedirectView.as_view(url='/boat-rides/', permanent=True)),
    path('blog/', include('blog.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('careers/', include('jobs.urls')),
    path('reviews/', include('testimonials.urls')),
    path("tinymce/", include("tinymce.urls")),
    path('loyalty/', include('loyalty.urls')),
    path('accommodation/', include('accommodation.urls')),
    path('crew/', include('reputation.urls')),
    path('resources/', include('resources.urls')),
    path('', include('seo.urls')),
    path('sitemap.xml', sitemap_clean_view, {'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin Site Customization
admin.site.site_header = "Mosety Boat Rides Naivasha"
admin.site.site_title = "Mosety Boat Rides Naivasha Admin"
admin.site.index_title = "Mosety Operations & Content Management"

