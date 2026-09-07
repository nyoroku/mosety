from django.urls import path
from . import views

app_name = 'loyalty'

urlpatterns = [
    path('signup/', views.LoyaltySignupView.as_view(), name='signup'),
    path('success/<str:code>/', views.LoyaltySuccessView.as_view(), name='signup_success'),
    path('api/manual-signup/', views.manual_signup, name='manual_signup'),
    path('api/redeem/<int:wallet_id>/', views.redeem_points, name='redeem_points'),
]
