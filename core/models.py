from django.db import models
from django.utils import timezone
from urllib.parse import quote


class SiteSettings(models.Model):
    """
    Singleton model managing all volatile business identity and public operational details.
    """
    business_name = models.CharField(max_length=150, default="Mosety Boat Rides Naivasha")
    legal_name = models.CharField(max_length=150, default="Mosety Boat Rides Naivasha")
    tagline = models.CharField(max_length=255, default="See Naivasha from the water.")
    
    phone = models.CharField(max_length=30, default="+254 114 182706")
    whatsapp_number = models.CharField(max_length=30, default="+254 114 182706")
    email = models.EmailField(default="info@mosety.co.ke")
    
    address_text = models.CharField(max_length=255, default="Karagita Public Beach, South Lake Road, Lake Naivasha, Kenya")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=-0.763400)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=36.425800)
    opening_hours = models.CharField(max_length=120, default="Daily 06:30 - 18:30")
    
    google_business_url = models.URLField(blank=True, default="")
    directions_url = models.URLField(blank=True, default="https://maps.google.com/?q=-0.763400,36.425800")
    base_url = models.URLField(default="https://mosety.co.ke")
    
    default_currency = models.CharField(max_length=5, default="KES")
    booking_notice = models.TextField(blank=True, default="Advance booking recommended for morning wildlife tours and weekend sunset cruises.")
    price_verified_at = models.DateField(default=timezone.now)
    
    # Media branding
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    favicon = models.ImageField(upload_to="branding/", blank=True, null=True)
    default_social_image = models.ImageField(upload_to="branding/", blank=True, null=True)
    
    # Analytics / Webmaster verification
    ga4_measurement_id = models.CharField(max_length=50, blank=True, default="", help_text="e.g. G-XXXXXXXXXX")
    gsc_verification_code = models.CharField(max_length=120, blank=True, default="")
    bing_verification_code = models.CharField(max_length=120, blank=True, default="")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.business_name

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    @property
    def phone_digits(self):
        return ''.join(c for c in self.phone if c.isdigit())

    @property
    def whatsapp_digits(self):
        digits = ''.join(c for c in self.whatsapp_number if c.isdigit())
        if digits.startswith('0') and len(digits) == 10:
            return f"254{digits[1:]}"
        return digits

    @property
    def phone_e164(self):
        digits = self.phone_digits
        if digits.startswith('0') and len(digits) == 10:
            return f"+254{digits[1:]}"
        return f"+{digits}" if digits else ""

    @property
    def tel_url(self):
        return f"tel:{self.phone_e164}" if self.phone_e164 else ""

    def build_whatsapp_url(self, message="Hi Mosety. I would like to inquire about a Lake Naivasha boat ride."):
        digits = self.whatsapp_digits
        if not digits:
            return ""
        encoded = quote(message)
        return f"https://wa.me/{digits}?text={encoded}"
