import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from utils import OptimizedImageMixin
from django.urls import reverse
from django.db.models import Avg, Count

class StaffMember(OptimizedImageMixin, models.Model):
    ROLE_CHOICES = [
        ('CAPTAIN', 'Captain'),
        ('GUIDE', 'Guide'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CAPTAIN')
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='staff_photos/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='staff_photos/webp/', blank=True, null=True, help_text="480px width optimized")
    bio = models.TextField(blank=True, help_text="Short bio for the staff profile page.")
    
    # QR Code for "Scan to Rate"
    qr_code = models.ImageField(upload_to='staff_qr_codes/', blank=True, null=True, editable=False)
    
    # Aggregated Stats (can be cached or calculated)
    total_reviews = models.PositiveIntegerField(default=0, editable=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, editable=False)

    class Meta:
        verbose_name = "Crew Member"
        verbose_name_plural = "Crew Members"
        ordering = ['-average_rating', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Optimize Photo
        if self.photo and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='photo')
        
        # Generate QR code if it doesn't exist
        if not self.qr_code:
            self.generate_qr_code()
            
        super().save(*args, **kwargs)

    def generate_qr_code(self):
        """Generates a QR code pointing to the staff member's rating page."""
        qr_data = f"https://paradiseboatrides.pythonanywhere.com/crew/{self.slug}/rate/"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        filename = f"qr-{self.slug}.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    def get_absolute_url(self):
        return reverse('reputation:staff_detail', kwargs={'slug': self.slug})

    def get_rate_url(self):
        return reverse('reputation:staff_rate', kwargs={'slug': self.slug})
