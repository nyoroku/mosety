from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('add-expense/', views.add_expense_view, name='add_expense'),
    path('add-sale/', views.add_sale_view, name='add_sale'),
    path('update-status/<int:pk>/', views.update_booking_status_view, name='update_booking_status'),
]