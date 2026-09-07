from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from decimal import Decimal


from utils import OptimizedImageMixin

class Tour(OptimizedImageMixin, models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    description = models.TextField()

    # SEO
    seo_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Overrides default SEO title"
    )

    meta_description = models.CharField(
        max_length=160,
        blank=True
    )

    highlights = models.TextField(
        blank=True,
        help_text="Bullet-style highlights for snippets & schema"
    )

    location = models.CharField(
        max_length=100,
        default="Lake Naivasha"
    )

    duration_hours = models.DecimalField(max_digits=3, decimal_places=1)
    price_resident = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in KES for Kenyan Residents")
    price_international = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in USD for International Visitors")
    max_people = models.PositiveIntegerField()

    image = models.ImageField(upload_to='tour_images/', blank=True, null=True)
    
    # Optimized Images
    webp_image = models.ImageField(upload_to='tour_images/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='tour_images/webp/', blank=True, null=True, help_text="480px width optimized")

    is_active = models.BooleanField(default=True)
    allow_indexing = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        # 1. Save instance first to ensure file exists
        super().save(*args, **kwargs)
        
        # 2. Check if main image exists but optimized versions don't, or if image changed
        if self.image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='image')

    def get_absolute_url(self):
        return reverse('bookings:tour_detail', kwargs={'slug': self.slug})

    @property
    def effective_seo_title(self):
        return self.seo_title or f"{self.name} | Paradise Boat Rides Naivasha"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('X', 'Cancelled')
    ]
    
    VISITOR_TYPE_CHOICES = [
        ('RESIDENT', 'Kenyan Resident'),
        ('INTERNATIONAL', 'International Visitor'),
    ]

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)

    number_of_people = models.PositiveIntegerField()
    visitor_type = models.CharField(max_length=20, choices=VISITOR_TYPE_CHOICES, default='RESIDENT')
    currency = models.CharField(max_length=5, default='KES')

    booking_date = models.DateTimeField(auto_now_add=True)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P'
    )

    notes = models.TextField(blank=True, null=True)
    
    # Referral Tracking
    referral_code = models.CharField(max_length=20, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.customer_name} – {self.tour.name} ({self.visitor_type})"

    def save(self, *args, **kwargs):
        if not self.total_price:
            price = self.tour.price_resident if self.visitor_type == 'RESIDENT' else self.tour.price_international
            base_total = price * self.number_of_people
            
            # Apply referral discount (10%)
            if self.referral_code:
                from loyalty.models import LoyaltyMember
                if LoyaltyMember.objects.filter(referral_code=self.referral_code).exists():
                    self.discount_amount = base_total * Decimal('0.10')
            
            self.total_price = base_total - self.discount_amount
        super().save(*args, **kwargs)
        
        # Award commission if confirmed (simple logic for now)
        if self.status == 'C' and self.referral_code:
            from loyalty.models import LoyaltyMember, Referral
            referrer = LoyaltyMember.objects.filter(referral_code=self.referral_code).first()
            if referrer:
                # 5% commission for the referrer
                commission = self.total_price * Decimal('0.05')
                Referral.objects.get_or_create(
                    referrer=referrer,
                    booking=self,
                    defaults={
                        'referred_customer_name': self.customer_name,
                        'commission_earned': commission
                    }
                )
                # Update member balance (simplified, usually done on payment)
                referrer.total_commission += commission
                referrer.save()


# ---------------- MOSETY BOOKING LEAD ----------------
import uuid
from urllib.parse import quote

class BookingLead(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New Lead'),
        ('CONTACTED', 'Contacted / WhatsApp Sent'),
        ('CONFIRMED', 'Confirmed Booking'),
        ('CANCELLED', 'Cancelled'),
        ('LOST', 'Lost / No Response'),
    ]

    BOOKING_TYPE_CHOICES = [
        ('PRIVATE', 'Private Boat Charter'),
        ('SHARED', 'Shared Boat Ride'),
    ]

    reference = models.CharField(max_length=30, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)

    tour = models.ForeignKey(
        'tours.Tour',
        on_delete=models.SET_NULL,
        null=True,
        related_name='booking_leads'
    )

    trip_date = models.DateField()
    preferred_time = models.CharField(
        max_length=50,
        default="Early Morning (06:30 - 09:00)",
        help_text="e.g. Early Morning, Mid-Morning, Afternoon, Sunset"
    )

    adults = models.PositiveIntegerField(default=2)
    children = models.PositiveIntegerField(default=0)
    party_size = models.PositiveIntegerField(default=2)
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES, default='PRIVATE')

    notes = models.TextField(blank=True, help_text="Special requests, photography focus, hotel pickup query")
    estimated_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=5, default="KES")

    # Attribution / Marketing
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)
    utm_term = models.CharField(max_length=100, blank=True)
    utm_content = models.CharField(max_length=100, blank=True)
    landing_page = models.CharField(max_length=255, blank=True)
    referrer = models.CharField(max_length=255, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    consent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Mosety Booking Lead"
        verbose_name_plural = "Mosety Booking Leads"

    def __str__(self):
        tour_name = self.tour.name if self.tour else "General Inquiry"
        return f"{self.reference} - {self.name} ({tour_name}, {self.party_size} guests)"

    def save(self, *args, **kwargs):
        if not self.reference:
            prefix = "MOS"
            date_str = timezone.now().strftime("%y%m")
            random_suffix = uuid.uuid4().hex[:4].upper()
            self.reference = f"{prefix}-{date_str}-{random_suffix}"
        self.party_size = (self.adults or 1) + (self.children or 0)
        super().save(*args, **kwargs)

    def build_whatsapp_continuation_url(self, site):
        tour_name = self.tour.name if self.tour else "Lake Naivasha Boat Ride"
        date_str = self.trip_date.strftime("%d %b %Y") if self.trip_date else "upcoming date"
        price_str = f"{self.currency} {self.estimated_total:,.0f}" if self.estimated_total else "pending confirmation"

        message = (
            f"Hi Mosety. I’d like to book {tour_name} on {date_str} for {self.party_size} guests. "
            f"Preferred time: {self.preferred_time}. Ref: {self.reference}. "
            f"Estimated website quote: {price_str}."
        )
        return site.build_whatsapp_url(message)

