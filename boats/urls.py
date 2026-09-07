# boats/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap
from seo.sitemaps import StaticViewSitemap, BlogSitemap, LocalPageSitemap, FAQSitemap, TourSitemap
from resources.sitemaps import ResourceGuideSitemap, ResourceStaticSitemap
sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'local': LocalPageSitemap,
    'faq': FAQSitemap,
    'tours': TourSitemap,
    'resources': ResourceGuideSitemap,
    'resources_static': ResourceStaticSitemap,
}

from bookings.views import BookLeadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('', include('tours.urls')),
    path('', include('content.urls')),
    path('book/', BookLeadView.as_view(), name='book_lead'),
    path('book/<slug:slug>/', BookLeadView.as_view(), name='book_tour_lead'),
    path('tours/', RedirectView.as_view(url='/boat-rides/', permanent=True)),
    path('services/', RedirectView.as_view(url='/boat-rides/', permanent=True)),
    path('blog/', RedirectView.as_view(url='/journal/', permanent=True)),
    path('dashboard/', include('dashboard.urls')),
    path('careers/', include('jobs.urls')),
    path('reviews/', include('testimonials.urls')),
    path("tinymce/", include("tinymce.urls")),
    path('loyalty/', include('loyalty.urls')),
    path('accommodation/', include('accommodation.urls')),
    path('crew/', include('reputation.urls')),
    path('resources/', include('resources.urls')),
    path('', include('seo.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin Site Customization
admin.site.site_header = "Mosety Boat Rides Naivasha"
admin.site.site_title = "Mosety Boat Rides Naivasha Admin"
admin.site.index_title = "Mosety Operations & Content Management"

