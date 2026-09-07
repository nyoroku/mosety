from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db import models
from django.db.models import Avg, Count
from .models import StaffMember
from testimonials.models import Testimonial

class LeaderboardView(ListView):
    model = StaffMember
    template_name = 'reputation/leaderboard.html'
    context_object_name = 'crew'

    def get_queryset(self):
        # Refresh stats on view load for simplicity
        for staff in StaffMember.objects.all():
            stats = staff.testimonials.filter(is_active=True).aggregate(avg=Avg('rating'), count=Count('id'))
            staff.average_rating = stats['avg'] or 0.00
            staff.total_reviews = stats['count'] or 0
            staff.save()
            
        return StaffMember.objects.all().order_by('-average_rating', '-total_reviews')

class ReputationDashboardView(LoginRequiredMixin, ListView):
    model = Testimonial
    template_name = 'reputation/dashboard.html'
    context_object_name = 'reviews'
    login_url = '/admin/login/'

    def get_queryset(self):
        # Only show reviews attributed to staff
        queryset = Testimonial.objects.filter(staff_member__isnull=False).order_by('-date_added')
        crew_slug = self.request.GET.get('staff_member')
        if crew_slug:
            queryset = queryset.filter(staff_member__slug=crew_slug)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_staff_reviews = Testimonial.objects.filter(staff_member__isnull=False)
        
        # Stats
        context['total_reviews'] = all_staff_reviews.count()
        context['average_crew_rating'] = all_staff_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        context['gated_count'] = all_staff_reviews.filter(rating__lt=4).count()
        context['promoted_count'] = all_staff_reviews.filter(rating__gte=4).count()
        
        # Staff performance breakdown
        context['staff_stats'] = StaffMember.objects.all().order_by('-average_rating')
        
        # Loyalty/Point Stats
        from loyalty.models import CrewWallet, LoyaltyMember
        context['total_points_awarded'] = CrewWallet.objects.aggregate(models.Sum('total_earned_points'))['total_earned_points__sum'] or 0
        context['total_loyalty_members'] = LoyaltyMember.objects.count()
        
        # Filtering context
        context['selected_staff'] = self.request.GET.get('staff_member')
        from django.utils import timezone
        context['today'] = timezone.now()
        
        return context

class StaffDetailView(DetailView):
    model = StaffMember
    template_name = 'reputation/profile.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_reviews'] = self.object.testimonials.filter(is_active=True).order_by('-date_added')[:5]
        return context

class StaffRateView(CreateView):
    model = Testimonial
    fields = ['customer_name', 'customer_country', 'rating', 'testimonial_text']
    template_name = 'reputation/rate.html'
    
    def form_valid(self, form):
        staff = get_object_or_404(StaffMember, slug=self.kwargs['slug'])
        form.instance.staff_member = staff
        form.instance.is_active = True
        self.object = form.save()
        
        # Award points to crew member for receiving a review
        from loyalty.views import award_crew_points
        award_crew_points(staff, 10, 'REVIEW', f"Review received from {form.instance.customer_name}")
        
        return redirect(f"{reverse('reputation:rating_success')}?rating={self.object.rating}&text={self.object.testimonial_text}&crew={staff.slug}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member'] = get_object_or_404(StaffMember, slug=self.kwargs['slug'])
        return context

class RatingSuccessView(TemplateView):
    template_name = 'reputation/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating = int(self.request.GET.get('rating', 5))
        text = self.request.GET.get('text', '')
        crew_slug = self.request.GET.get('crew', '')
        
        context['rating'] = rating
        context['text'] = text
        context['crew_slug'] = crew_slug
        
        # The actual Paradise Boat Rides Google Review Link
        context['google_review_url'] = "https://g.page/paradise-boat-rides/review" 
        return context
