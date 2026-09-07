from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils.text import slugify
from utils import OptimizedImageMixin


class Service(OptimizedImageMixin, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = HTMLField(help_text="Provide a detailed description of the service.")
    icon_class = models.CharField(
        max_length=50,
        help_text="Enter a Font Awesome icon class, e.g., 'fas fa-fish'"
    )
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='service_images/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='service_images/webp/', blank=True, null=True, help_text="480px width optimized")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Services will be ordered by this number (lower first).")

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if self.image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='image')

    def get_absolute_url(self):
        return reverse('services:service_detail', kwargs={'slug': self.slug})