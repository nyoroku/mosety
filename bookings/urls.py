from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # List all tours
    path('', views.TourListView.as_view(), name='tour_list'),

    # Tour detail variants
    path('<slug:slug>/', views.TourDetailRedirectView.as_view(), name='tour_detail'),
    path('<slug:slug>/resident/', views.TourDetailView.as_view(), {'visitor_type': 'RESIDENT'}, name='tour_detail_resident'),
    path('<slug:slug>/international/', views.TourDetailView.as_view(), {'visitor_type': 'INTERNATIONAL'}, name='tour_detail_international'),

    # Create booking for a specific tour (slug required)
    path('<slug:slug>/book/', views.CreateBookingView.as_view(), name='create_booking'),

    # Booking success page
    path('booking-success/', views.booking_success_view, name='booking_success'),
]
