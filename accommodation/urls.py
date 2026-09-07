from django.urls import path
from . import views

app_name = 'accommodation'

urlpatterns = [
    path('', views.HotelListView.as_view(), name='hotel_list'),
    path('<slug:slug>/', views.HotelDetailView.as_view(), name='hotel_detail'),
]
