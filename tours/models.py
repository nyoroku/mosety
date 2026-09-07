from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from seo.models import SEOMixin
from utils import OptimizedImageMixin


class Tour(OptimizedImageMixin, SEOMixin, models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    short_name = models.CharField(max_length=80, blank=True, help_text="Concise name for chips and selectors")
    summary = models.CharField(max_length=255, help_text="One-sentence differentiator")
    description = models.TextField(help_text="Full editorial description")

    hero_image = models.ImageField(upload_to='tours/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='tours/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='tours/webp/', blank=True, null=True)

    duration_minutes = models.PositiveIntegerField(default=60, help_text="Standard duration in minutes")
    min_guests = models.PositiveIntegerField(default=1)
    max_guests = models.PositiveIntegerField(default=7)

    is_private = models.BooleanField(default=True, help_text="Available as private charter")
    is_shared = models.BooleanField(default=True, help_text="Available as shared ride")

    departure_location = models.CharField(max_length=150, default="Karagita Public Beach, South Lake Road")
    best_for = models.CharField(max_length=200, default="Wildlife enthusiasts, families, couples")

    highlights = models.TextField(blank=True, help_text="Newline-separated bullet points of what makes this ride special")
    itinerary = models.TextField(blank=True, help_text="Timeline overview of the experience")

    included = models.TextField(default="Full boat charter, licensed local captain, fuel, Coast Guard approved life vests")
    excluded = models.TextField(default="Sanctuary walking fees (if visiting Crescent Island), personal snacks, optional captain gratuities")
    what_to_bring = models.TextField(default="Sunscreen, sun hat, light windbreaker or fleece, camera or smartphone, binoculars")
    safety_notes = models.TextField(default="Mandatory fitted life jackets for all passengers. Captain strictly maintains 30-50m buffer from hippo pods.")
    child_policy = models.TextField(default="Children of all ages welcome. Certified infant and toddler safety vests provided.")
    weather_policy = models.TextField(default="Tours operate in calm conditions and light drizzle. In case of high afternoon winds, rides are rescheduled at zero fee.")
    cancellation_policy = models.TextField(default="Free cancellation or schedule adjustment via WhatsApp up to 2 hours before departure.")

    intent_tag = models.CharField(max_length=50, blank=True, help_text="e.g. wildlife, crescent_island, sunset, family, private, birding")

    sort_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_verified_at = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Mosety Tour"
        verbose_name_plural = "Mosety Tours"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.short_name:
            self.short_name = self.name
        super().save(*args, **kwargs)
        if self.hero_image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='hero_image')

    def get_absolute_url(self):
        return f"/boat-rides/{self.slug}/"

    @property
    def duration_display(self):
        if self.duration_minutes >= 60:
            hours = self.duration_minutes / 60.0
            if hours.is_integer():
                return f"{int(hours)} hr" if int(hours) == 1 else f"{int(hours)} hrs"
            return f"{hours:.1f} hrs"
        return f"{self.duration_minutes} mins"

    @property
    def highlights_list(self):
        return [line.strip() for line in self.highlights.splitlines() if line.strip()]

    @property
    def primary_price_tier(self):
        # Prioritize standard per-boat charter rate if present, else lowest tier
        boat_tier = self.price_tiers.filter(is_active=True, pricing_mode='PER_BOAT').order_by('amount_kes').first()
        if boat_tier:
            return boat_tier
        return self.price_tiers.filter(is_active=True).order_by('amount_kes').first()

    @property
    def starting_price_kes(self):
        tier = self.primary_price_tier
        return tier.amount_kes if tier else None

    @property
    def starting_price_usd(self):
        tier = self.primary_price_tier
        return tier.amount_usd if tier else None

    @property
    def pricing_mode_display(self):
        tier = self.primary_price_tier
        if tier and tier.pricing_mode == 'PER_PERSON':
            return "Per Person"
        return "Per Boat"

    @property
    def shared_tier(self):
        return self.price_tiers.filter(is_active=True, pricing_mode='PER_PERSON').order_by('amount_kes').first()

    @property
    def private_tier(self):
        return self.price_tiers.filter(is_active=True, pricing_mode='PER_BOAT').order_by('amount_kes').first()


class PriceTier(models.Model):
    PRICING_MODES = [
        ('PER_BOAT', 'Per Boat Charter'),
        ('PER_PERSON', 'Per Person'),
    ]
    RESIDENT_TYPES = [
        ('ALL', 'All Visitors'),
        ('RESIDENT', 'Kenyan Resident'),
        ('NON_RESIDENT', 'Non-Resident'),
    ]

    tour = models.ForeignKey(Tour, related_name='price_tiers', on_delete=models.CASCADE)
    label = models.CharField(max_length=100, default="Standard Boat Charter")
    min_guests = models.PositiveIntegerField(default=1)
    max_guests = models.PositiveIntegerField(default=7)
    pricing_mode = models.CharField(max_length=20, choices=PRICING_MODES, default='PER_BOAT')
    amount_kes = models.DecimalField(max_digits=10, decimal_places=2)
    resident_type = models.CharField(max_length=20, choices=RESIDENT_TYPES, default='ALL')

    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'amount_kes']
        verbose_name = "Price Tier"
        verbose_name_plural = "Price Tiers"

    @property
    def amount_usd(self):
        if self.amount_kes:
            return round(float(self.amount_kes) / 130.0)
        return None

    def __str__(self):
        return f"{self.tour.name} - {self.label} (KES {self.amount_kes:,.0f} {self.get_pricing_mode_display()})"


class AddOn(models.Model):
    PRICING_MODES = [
        ('PER_BOOKING', 'Per Booking'),
        ('PER_PERSON', 'Per Person'),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    price_kes = models.DecimalField(max_digits=10, decimal_places=2)
    pricing_mode = models.CharField(max_length=20, choices=PRICING_MODES, default='PER_BOOKING')
    description = models.TextField(blank=True)
    eligible_tours = models.ManyToManyField(Tour, blank=True, related_name='addons')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (+KES {self.price_kes:,.0f})"
