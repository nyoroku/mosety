from django.urls import path
from . import views

app_name = 'reputation'

urlpatterns = [
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('dashboard/', views.ReputationDashboardView.as_view(), name='management_dashboard'),
    path('success/', views.RatingSuccessView.as_view(), name='rating_success'),
    path('<slug:slug>/', views.StaffDetailView.as_view(), name='staff_detail'),
    path('<slug:slug>/rate/', views.StaffRateView.as_view(), name='staff_rate'),
]
