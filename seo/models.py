from django.db import models
from tinymce.models import HTMLField
from utils import auto_link, OptimizedImageMixin
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.urls import reverse
import html


# ---------------- FAQ ----------------
class FAQ(models.Model):
    question = models.CharField(max_length=255)

    # SEO & accessibility
    plain_answer = models.TextField(
        blank=True,
        help_text="Plain text answer for meta description, schema & screen readers"
    )

    answer = HTMLField()

    seo_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Overrides default SEO title if provided"
    )

    meta_description = models.CharField(max_length=160, blank=True)

    # pSEO platforms
    search_intent = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. pricing, safety, booking, location"
    )

    is_active = models.BooleanField(default=True)
    allow_indexing = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question

    @property
    def linked_answer(self):
        result = auto_link(self.answer)
        return mark_safe(html.unescape(result))

    @property
    def effective_seo_title(self):
        return self.seo_title or self.question

    def get_absolute_url(self):
        return reverse('seo:faq')

class LocalPage(OptimizedImageMixin, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    # SEO core
    seo_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Used for the browser title tag. Defaults to title."
    )

    meta_description = models.CharField(max_length=160, blank=True)

    # pSEO expansion fields
    primary_keyword = models.CharField(
        max_length=100,
        help_text="Main keyword e.g. 'Boat rides in Naivasha'"
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Naivasha, Lake Naivasha, Crescent Island"
    )

    modifiers = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated: price, safety, sunset, group, birthday"
    )

    content = HTMLField()
    image = models.ImageField(upload_to='location_images/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='location_images/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='location_images/webp/', blank=True, null=True, help_text="480px width optimized")

    is_active = models.BooleanField(default=True)
    allow_indexing = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = "SEO Local Page"
        verbose_name_plural = "SEO Local Pages"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if self.image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='image')

    @property
    def linked_content(self):
        result = auto_link(self.content)
        return mark_safe(html.unescape(result))

    @property
    def effective_seo_title(self):
        return self.seo_title or self.title

    def get_absolute_url(self):
        return reverse('seo:detail', kwargs={'slug': self.slug})

class LocalPageImage(OptimizedImageMixin, models.Model):
    local_page = models.ForeignKey(LocalPage, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='location_gallery/')
    webp_image = models.ImageField(upload_to='location_gallery/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='location_gallery/webp/', blank=True, null=True, help_text="480px width optimized")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='image')

    class Meta:
        ordering = ['order']
        verbose_name = "Location Image"
        verbose_name_plural = "Location Images"

    def __str__(self):
        return f"Image for {self.local_page.title}"


# ---------------- INTERNAL LINKING ----------------
class InternalLink(models.Model):
    keyword = models.CharField(
        max_length=100, 
        unique=True,
        help_text="The exact phrase to turn into a link (case-insensitive)"
    )
    url = models.CharField(
        max_length=255,
        help_text="Relative (e.g. /tours/) or absolute URL"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['keyword']

    def __str__(self):
        return f"{self.keyword} -> {self.url}"


# ---------------- REUSABLE SEO MIXIN & REDIRECTS ----------------
class SEOMixin(models.Model):
    seo_title = models.CharField(max_length=70, blank=True, help_text="Overrides page title for SEO (50-60 chars)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="Search engine snippet (140-160 chars)")
    canonical_override = models.CharField(max_length=255, blank=True, help_text="Override canonical URL")
    og_title = models.CharField(max_length=100, blank=True, help_text="OpenGraph social title")
    og_description = models.CharField(max_length=200, blank=True, help_text="OpenGraph social description")
    og_image = models.ImageField(upload_to='seo/og/', blank=True, null=True, help_text="1200x630 social share preview")
    noindex = models.BooleanField(default=False, help_text="Instruct robots not to index this page")
    nofollow = models.BooleanField(default=False, help_text="Instruct robots not to follow links on this page")

    class Meta:
        abstract = True


class Redirect(models.Model):
    old_path = models.CharField(max_length=255, unique=True, db_index=True)
    new_path = models.CharField(max_length=255)
    status_code = models.PositiveSmallIntegerField(
        default=301,
        choices=[(301, '301 Permanent Redirect'), (302, '302 Temporary Redirect')]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['old_path']
        verbose_name = "SEO Redirect"
        verbose_name_plural = "SEO Redirects"

    def __str__(self):
        return f"{self.old_path} -> {self.new_path} ({self.status_code})"