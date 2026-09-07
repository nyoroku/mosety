from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tinymce.models import HTMLField

class ResourceCategory(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text='Lucide or FontAwesome icon name e.g. fas fa-book')
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class GuidePage(models.Model):
    category = models.ForeignKey(ResourceCategory, related_name='guide_pages', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    h1 = models.CharField(max_length=200, blank=True, help_text='Override for the H1 tag. Defaults to title.')
    intro_answer = models.TextField(max_length=500, help_text='Plain text, 40-60 words. First visible paragraph. Used for AEO/featured snippets.')
    body = HTMLField()
    target_keyword = models.CharField(max_length=100, blank=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_pillar = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    allow_indexing = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__sort_order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('resources:guide_detail', kwargs={'slug': self.slug})

    @property
    def effective_h1(self):
        return self.h1 or self.title

    @property
    def effective_meta_title(self):
        return self.meta_title or self.title

class FAQItem(models.Model):
    category = models.ForeignKey(ResourceCategory, related_name='faq_items', on_delete=models.SET_NULL, null=True, blank=True)
    guide_page = models.ForeignKey(GuidePage, related_name='faq_items', on_delete=models.SET_NULL, null=True, blank=True)
    question = models.CharField(max_length=255)
    answer = models.TextField(help_text='Plain text answer, 40-60 words. Used for both display and FAQPage schema.')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.question

class PricingTier(models.Model):
    tour_type = models.CharField(max_length=100)
    group_size_label = models.CharField(max_length=50, help_text='e.g. 1-4 people, 5-10 people')
    price_kes = models.DecimalField(max_digits=10, decimal_places=2)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    includes = models.TextField(help_text='What is included in this tier')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.tour_type} - {self.group_size_label}'

class DownloadAsset(models.Model):
    guide_page = models.ForeignKey(GuidePage, related_name='downloads', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resources/downloads/')
    file_type = models.CharField(max_length=20, help_text='e.g. PDF, JPEG, etc.')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
