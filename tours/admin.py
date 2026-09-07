from django.contrib import admin
from .models import Tour, PriceTier, AddOn


class PriceTierInline(admin.TabularInline):
    model = PriceTier
    extra = 1
    fields = ('label', 'min_guests', 'max_guests', 'pricing_mode', 'amount_kes', 'resident_type', 'is_active', 'sort_order')


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'starting_price_kes', 'intent_tag', 'is_featured', 'is_active', 'last_verified_at')
    list_filter = ('is_featured', 'is_active', 'intent_tag')
    search_fields = ('name', 'summary', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PriceTierInline]

    fieldsets = (
        ("Core Identity", {
            "fields": ("name", "slug", "short_name", "summary", "description", "hero_image")
        }),
        ("Operation & Logistics", {
            "fields": ("duration_minutes", "min_guests", "max_guests", "is_private", "is_shared", "departure_location", "best_for", "intent_tag")
        }),
        ("Experience Details", {
            "fields": ("highlights", "itinerary", "included", "excluded", "what_to_bring")
        }),
        ("Safety & Policies", {
            "fields": ("safety_notes", "child_policy", "weather_policy", "cancellation_policy")
        }),
        ("SEO & Social Metadata", {
            "fields": ("seo_title", "meta_description", "canonical_override", "og_title", "og_description", "og_image", "noindex", "nofollow")
        }),
        ("Publication & Verification", {
            "fields": ("sort_order", "is_featured", "is_active", "last_verified_at")
        }),
    )


@admin.register(PriceTier)
class PriceTierAdmin(admin.ModelAdmin):
    list_display = ('tour', 'label', 'pricing_mode', 'amount_kes', 'resident_type', 'min_guests', 'max_guests', 'is_active')
    list_filter = ('pricing_mode', 'resident_type', 'is_active', 'tour')
    search_fields = ('tour__name', 'label', 'notes')


@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_kes', 'pricing_mode', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
