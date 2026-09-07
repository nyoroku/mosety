from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import StaffMember

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'average_rating', 'total_reviews', 'review_link_display', 'qr_code_preview')
    list_filter = ('role',)
    search_fields = ('name',)
    readonly_fields = ('qr_code_preview', 'review_link_display', 'average_rating', 'total_reviews', 'qr_code')
    prepopulated_fields = {'slug': ('name',)}

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['dashboard_url'] = reverse('reputation:management_dashboard')
        return super().changelist_view(request, extra_context=extra_context)

    def review_link_display(self, obj):
        url = f"https://paradiseboatrides.pythonanywhere.com/crew/{obj.slug}/rate/"
        return format_html('<a href="{0}" target="_blank">{0}</a>', url)
    
    review_link_display.short_description = "Review Link"

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="100" height="100" />', obj.qr_code.url)
        return "Not generated"
    
    qr_code_preview.short_description = "QR Code Preview"
