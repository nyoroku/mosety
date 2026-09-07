from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponse
from bookings.models import Booking
from dashboard.models import Expense
from dashboard.forms import ExpenseForm, SaleForm
from reputation.models import StaffMember


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    login_url = '/admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sales Logic
        confirmed_bookings = Booking.objects.filter(status='C')
        total_sales = confirmed_bookings.aggregate(total=Sum('total_price'))['total'] or 0
        referral_sales = confirmed_bookings.filter(referral_code__isnull=False).exclude(referral_code='').aggregate(total=Sum('total_price'))['total'] or 0
        direct_sales = total_sales - referral_sales
        
        # Expense & Profit logic
        total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        profit = total_sales - total_expenses
        
        # Loyalty Metrics
        from loyalty.models import LoyaltyMember, Referral, CrewWallet
        total_loyalty_members = LoyaltyMember.objects.count()
        pending_commissions = Referral.objects.filter(is_paid=False).aggregate(total=Sum('commission_earned'))['total'] or 0
        points_liability = CrewWallet.objects.aggregate(total=Sum('available_points'))['total'] or 0
        
        pending_bookings = Booking.objects.filter(status='P').count()
        
        context.update({
            'total_sales': total_sales,
            'referral_sales': referral_sales,
            'direct_sales': direct_sales,
            'total_expenses': total_expenses,
            'profit': profit,
            'pending_bookings': pending_bookings,
            'total_loyalty_members': total_loyalty_members,
            'pending_commissions': pending_commissions,
            'points_liability': points_liability,
            'recent_sales': Booking.objects.order_by('-booking_date')[:8],
            'recent_expenses': Expense.objects.order_by('-date_incurred')[:8],
            'top_staff': StaffMember.objects.all().order_by('-average_rating', '-total_reviews')[:3],
            'expense_form': ExpenseForm(),
            'sale_form': SaleForm(),
            'today': timezone.now() if hasattr(self, 'request') else None, # timezone import needed
        })
        return context


def add_expense_view(request):
    if request.method == 'POST' and request.htmx:
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            expenses = Expense.objects.order_by('-date_incurred')[:5]
            return render(request, 'dashboard/partials/expense_list.html', {'expenses': expenses})
    return render(request, 'dashboard/partials/expense_form.html', {'expense_form': form})


def add_sale_view(request):
    if request.method == 'POST' and request.htmx:
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            sales = Booking.objects.order_by('-booking_date')[:5]
            return render(request, 'dashboard/partials/sales_list.html', {'sales': sales})
    return render(request, 'dashboard/partials/add_sale_form.html', {'sale_form': form})


def update_booking_status_view(request, pk):
    if request.method == 'POST' and request.htmx:
        booking = get_object_or_404(Booking, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES).keys():
            booking.status = new_status
            booking.save()

            # Re-render KPIs and sales list
            total_sales = Booking.objects.filter(status='C').aggregate(total=Sum('total_price'))['total'] or 0
            profit = total_sales - Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
            pending_bookings = Booking.objects.filter(status='P').count()

            sales = Booking.objects.order_by('-booking_date')[:5]

            response = render(request, 'dashboard/partials/sales_list.html', {'sales': sales})

            kpi_html = render_to_string('dashboard/partials/kpi_cards.html', {
                'total_sales': total_sales, 'pending_bookings': pending_bookings, 'profit': profit,
                'total_expenses': Expense.objects.aggregate(total=Sum('amount'))['total'] or 0,
            })
            response['HX-Trigger-After-Swap'] = f"document.getElementById('kpi-container').outerHTML = `{kpi_html}`;"
            return response
    return HttpResponse(status=400)