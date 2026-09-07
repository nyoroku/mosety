from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Expense, ExpenseCategory



@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'view_dashboard_link')
    
    def view_dashboard_link(self, obj):
        url = reverse('dashboard:dashboard')
        return format_html('<a class="button" href="{}">Go to Business Dashboard</a>', url)
    view_dashboard_link.short_description = "Action"

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'amount', 'date_incurred', 'view_dashboard_link')
    list_filter = ('category', 'date_incurred')
    
    def view_dashboard_link(self, obj):
        url = reverse('dashboard:dashboard')
        return format_html('<a class="button" href="{}">View Dashboard</a>', url)
    view_dashboard_link.short_description = "Dashboard"