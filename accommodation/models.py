from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from utils import OptimizedImageMixin

class PartnerHotel(OptimizedImageMixin, models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = HTMLField(help_text="Detailed description of the hotel.")
    main_image = models.ImageField(upload_to='hotel_images/', blank=True, null=True, help_text="Main thumbnail image.")
    webp_image = models.ImageField(upload_to='hotel_images/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='hotel_images/webp/', blank=True, null=True, help_text="480px width optimized")
    website_url = models.URLField(blank=True, null=True, help_text="Link to the hotel's official website.")
    location = models.CharField(max_length=200, help_text="General location, e.g., 'North Lake Naivasha'.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Partner Hotel"
        verbose_name_plural = "Partner Hotels"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('accommodation:hotel_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.main_image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='main_image')

class HotelImage(OptimizedImageMixin, models.Model):
    hotel = models.ForeignKey(PartnerHotel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_gallery/')
    webp_image = models.ImageField(upload_to='hotel_gallery/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='hotel_gallery/webp/', blank=True, null=True, help_text="480px width optimized")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='image')

    class Meta:
        ordering = ['order']
        verbose_name = "Hotel Image"
        verbose_name_plural = "Hotel Images"

    def __str__(self):
        return f"Image for {self.hotel.name}"
