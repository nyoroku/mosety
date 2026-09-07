from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView
from django.urls import reverse
from .models import LoyaltyMember, CrewWallet, PointTransaction
from .forms import LoyaltySignupForm
from reputation.models import StaffMember

def award_crew_points(staff_member, points, source, description=""):
    wallet, created = CrewWallet.objects.get_or_create(staff_member=staff_member)
    wallet.available_points += points
    wallet.total_earned_points += points
    wallet.save()
    
    PointTransaction.objects.create(
        wallet=wallet,
        points=points,
        source=source,
        description=description
    )

class LoyaltySignupView(CreateView):
    model = LoyaltyMember
    form_class = LoyaltySignupForm
    template_name = 'loyalty/signup.html'

    def form_valid(self, form):
        crew_slug = self.request.GET.get('crew')
        if crew_slug:
            staff = StaffMember.objects.filter(slug=crew_slug).first()
            if staff:
                form.instance.facilitated_by = staff
                # Award points for signup facilitation
                award_crew_points(staff, 50, 'SIGNUP', f"Facilitated signup for {form.instance.customer_name}")
        
        self.object = form.save()
        return redirect('loyalty:signup_success', code=self.object.referral_code)

class LoyaltySuccessView(TemplateView):
    template_name = 'loyalty/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referral_code'] = self.kwargs.get('code')
        context['referral_url'] = f"http://127.0.0.1:8000/?ref={context['referral_code']}"
        return context

from django.http import JsonResponse
from decimal import Decimal

def manual_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        crew_slug = request.POST.get('crew_slug')
        
        staff = get_object_or_404(StaffMember, slug=crew_slug)
        member, created = LoyaltyMember.objects.get_or_create(
            email=email,
            defaults={'customer_name': name, 'facilitated_by': staff}
        )
        
        if created:
            award_crew_points(staff, 50, 'SIGNUP', f"Manual signup: {name}")
            return JsonResponse({'status': 'success', 'message': f'Signed up {name}!'})
        return JsonResponse({'status': 'error', 'message': 'Email already registered.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

def redeem_points(request, wallet_id):
    wallet = get_object_or_404(CrewWallet, id=wallet_id)
    points = wallet.available_points
    if points > 0:
        cash_value = Decimal(points) * Decimal('0.5') # 1 point = 0.5 KES
        
        # Create transaction
        PointTransaction.objects.create(
            wallet=wallet,
            points=-points,
            source='REDEMPTION',
            description=f"Redeemed {points} points for KES {cash_value}"
        )
        
        # Update wallet
        wallet.available_points = 0
        wallet.total_cash_redeemed += cash_value
        wallet.save()
        
        return JsonResponse({'status': 'success', 'cash': str(cash_value)})
    return JsonResponse({'status': 'error', 'message': 'No points to redeem.'})
