from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('boat-rides/', views.TourListView.as_view(), name='tour_list'),
    path('boat-rides/<slug:slug>/', views.TourDetailView.as_view(), name='tour_detail'),
    path('find-your-ride/', views.FindYourRideView.as_view(), name='find_your_ride'),
    path('prices/', views.PricesPageView.as_view(), name='prices'),
    path('prices/estimate/', views.PriceEstimateView.as_view(), name='prices_estimate'),
]
