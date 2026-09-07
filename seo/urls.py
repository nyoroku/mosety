from django.urls import path
from . import views

app_name = 'seo'
urlpatterns = [
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('destinations/', views.LocalPageListView.as_view(), name='list'),
    path('<slug:slug>/', views.LocalPageDetailView.as_view(), name='detail'),
]