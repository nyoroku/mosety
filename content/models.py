from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from seo.models import SEOMixin
from utils import OptimizedImageMixin


class Captain(OptimizedImageMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    photo = models.ImageField(upload_to='captains/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='captains/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='captains/webp/', blank=True, null=True)

    short_bio = models.TextField(help_text="Factual background, local upbringing, navigation credentials")
    years_on_lake = models.PositiveIntegerField(null=True, blank=True, help_text="Verified years operating on Lake Naivasha")
    specialties = models.CharField(max_length=200, help_text="e.g. Hippo behavior, raptor identification, sunrise photography")
    languages = models.CharField(max_length=100, default="English, Swahili")
    quote = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Mosety Captain"
        verbose_name_plural = "Mosety Captains"

    def __str__(self):
        return f"Captain {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.photo and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='photo')


class GuideArticle(OptimizedImageMixin, SEOMixin, models.Model):
    CONTENT_TYPES = [
        ('PLANNING', 'Trip Planning'),
        ('DESTINATION', 'Destination Guide'),
        ('WILDLIFE', 'Wildlife Entity'),
        ('JOURNAL', 'Captains Log / Journal'),
        ('ITINERARY', 'Itinerary'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.CharField(max_length=255, help_text="1-2 sentences summarizing the core takeaway")
    body = models.TextField(help_text="Detailed editorial content")

    hero_image = models.ImageField(upload_to='articles/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='articles/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='articles/webp/', blank=True, null=True)

    author_name = models.CharField(max_length=100, default="Mosety Editorial Team")
    reviewer_name = models.CharField(max_length=100, blank=True, help_text="Verified local captain or wildlife specialist")
    published_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_verified_at = models.DateField(default=timezone.now)

    content_type = models.CharField(max_length=30, choices=CONTENT_TYPES, default='PLANNING')
    related_tours = models.ManyToManyField('tours.Tour', blank=True, related_name='guide_articles')

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Guide Article"
        verbose_name_plural = "Guide Articles"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if self.hero_image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='hero_image')

    def get_absolute_url(self):
        if self.content_type == 'JOURNAL':
            return f"/journal/{self.slug}/"
        return f"/naivasha-guide/{self.slug}/"


class QuestionAnswer(models.Model):
    CATEGORIES = [
        ('General', 'General Questions'),
        ('Pricing', 'Pricing & Payments'),
        ('Safety', 'Safety & Standards'),
        ('Children', 'Children & Families'),
        ('Logistics', 'Logistics & Arrival'),
        ('Wildlife', 'Wildlife & Ethics'),
    ]

    question = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    answer = models.TextField(help_text="Concise, factual answer")
    category = models.CharField(max_length=50, choices=CATEGORIES, default='General')
    related_tour = models.ForeignKey('tours.Tour', null=True, blank=True, on_delete=models.SET_NULL, related_name='faqs')
    sort_order = models.PositiveIntegerField(default=0)
    last_verified_at = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "Question & Answer"
        verbose_name_plural = "Questions & Answers"

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)[:250]
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    display_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    review_text = models.TextField()
    source = models.CharField(max_length=50, default="Google Review")
    source_url = models.URLField(blank=True)
    review_date = models.DateField(default=timezone.now)
    verified_import = models.BooleanField(default=True)
    permission_status = models.CharField(max_length=50, default="Public Review")
    related_tour = models.ForeignKey('tours.Tour', null=True, blank=True, on_delete=models.SET_NULL, related_name='testimonials')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-review_date', '-id']
        verbose_name = "Guest Testimonial"
        verbose_name_plural = "Guest Testimonials"

    def __str__(self):
        return f"{self.display_name} ({self.rating}★) - {self.source}"
