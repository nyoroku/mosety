import html
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from tinymce.models import HTMLField
from django.utils.text import slugify
from utils import auto_link, OptimizedImageMixin
from django.utils.safestring import mark_safe


class Post(OptimizedImageMixin, models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_description = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='blog_images/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='blog_images/webp/', blank=True, null=True, help_text="480px width optimized")

    # This is the magic for tagging
    tags = TaggableManager()

    class Meta:
        ordering = ['-created_at']

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
        """Return content with auto-links applied and unescaped."""

        # 1. Run the auto_link function
        result_with_escaped_tags = auto_link(self.content)

        # 2. Unescape the HTML entities (&lt; back to <, etc.)
        # This reverses the escaping done by BeautifulSoup's str() output
        final_content = html.unescape(result_with_escaped_tags)

        # 3. Mark the final, corrected string safe for rendering
        return mark_safe(final_content)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

