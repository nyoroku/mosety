from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.ResourcesLandingView.as_view(), name='landing'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('faq/', views.ResourceFAQView.as_view(), name='faq'),
    path('<slug:slug>/', views.GuidePageDetailView.as_view(), name='guide_detail'),
]
