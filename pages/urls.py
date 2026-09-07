from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('robots.txt', views.robots_txt, name='robots'),
    path('llms.txt', views.llms_txt, name='llms'),
]
