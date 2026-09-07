from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Business Identity", {
            "fields": ("business_name", "legal_name", "tagline", "base_url", "default_currency")
        }),
        ("Contact & Direct Conversion", {
            "fields": ("phone", "whatsapp_number", "email", "booking_notice", "price_verified_at")
        }),
        ("Location & Arrival", {
            "fields": ("address_text", "latitude", "longitude", "opening_hours", "google_business_url", "directions_url")
        }),
        ("Branding Assets", {
            "fields": ("logo", "favicon", "default_social_image")
        }),
        ("Analytics & Verification", {
            "fields": ("ga4_measurement_id", "gsc_verification_code", "bing_verification_code")
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
