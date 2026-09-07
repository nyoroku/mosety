from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # Core Authority & Trust Pillars
    path('crescent-island/', views.CrescentIslandView.as_view(), name='crescent_island'),
    path('safety/', views.SafetyStandardsView.as_view(), name='safety'),
    path('captains/', views.CaptainsListView.as_view(), name='captains'),
    path('reviews/', views.ReviewsListView.as_view(), name='reviews'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactLocationView.as_view(), name='contact'),
    path('questions/', views.FAQHubView.as_view(), name='questions'),

    # Plan Your Visit Authority Hub
    path('plan-your-visit/', views.PlanYourVisitHubView.as_view(), name='plan_hub'),
    path('plan-your-visit/getting-here/', views.PlanGettingHereView.as_view(), name='plan_getting_here'),
    path('plan-your-visit/best-time-to-go/', views.PlanBestTimeToVisitView.as_view(), name='plan_best_time'),
    path('plan-your-visit/what-to-bring/', views.PlanWhatToBringView.as_view(), name='plan_what_to_bring'),
    path('plan-your-visit/children/', views.PlanChildrenSafetyView.as_view(), name='plan_children'),

    # Naivasha Destination Hub
    path('naivasha-guide/', views.NaivashaGuideHubView.as_view(), name='guide_hub'),
    path('naivasha-guide/hippos/', views.NaivashaHipposView.as_view(), name='guide_hippos'),
    path('naivasha-guide/birds/', views.NaivashaBirdsView.as_view(), name='guide_birds'),
    path('naivasha-guide/wildlife/', views.NaivashaWildlifeView.as_view(), name='guide_wildlife'),

    # Journal / Captains Log
    path('journal/', views.JournalListView.as_view(), name='journal_list'),
    path('journal/<slug:slug>/', views.JournalDetailView.as_view(), name='journal_detail'),
]
