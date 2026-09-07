from bs4 import BeautifulSoup
import re
from html import escape
from django.core.files.base import ContentFile
from PIL import Image
import io
import os

KEYWORDS = {
    "Lake Naivasha": "/lake-naivasha/",
    "boat rides": "/tours/",
    "sunset cruise": "/tours/sunset-cruise/",
    "hippos": "/wildlife/",
    "Crescent Island": "/destinations/crescent-island-naivasha/",
    "bird watching": "/activities/bird-watching/",
    "Naivasha": "/lake-naivasha/",
    "private boat": "/tours/",
    "family tour": "/tours/",
    "wildlife safari": "/tours/hippo-safari-and-bird-watching/",
}


def auto_link(html):
    """
    Automatically wraps keywords in <a> tags using the InternalLink model.
    """
    if not html:
        return html

    from seo.models import InternalLink
    
    # Get active keywords from DB
    internal_links = InternalLink.objects.filter(is_active=True)
    if not internal_links.exists():
        return html

    soup = BeautifulSoup(html, "html.parser")

    # Match the longest phrases first in one pass.  This prevents a broad
    # phrase such as "Paradise Boat Rides" from being inserted inside a
    # longer link such as "Paradise Boat Rides Naivasha".
    links = list(internal_links.values_list('keyword', 'url'))
    links.sort(key=lambda item: len(item[0]), reverse=True)
    keyword_urls = {keyword.casefold(): url for keyword, url in links}
    pattern = re.compile(
        r"(?<![\w-])(?:" + "|".join(re.escape(keyword) for keyword, _ in links) + r")(?![\w-])",
        flags=re.IGNORECASE,
    )

    for text_node in soup.find_all(string=True):
        parent = text_node.parent

        # Never touch existing links or scripts/styles
        if parent.name in ["a", "script", "style"]:
            continue

        original_text = str(text_node)
        matches = list(pattern.finditer(original_text))
        if not matches:
            continue

        fragments = []
        cursor = 0
        for match in matches:
            if match.start() > cursor:
                fragments.append(escape(original_text[cursor:match.start()]))
            keyword = match.group(0)
            url = keyword_urls[keyword.casefold()]
            fragments.append(
                f'<a href="{escape(url, quote=True)}">{escape(keyword)}</a>'
            )
            cursor = match.end()
        if cursor < len(original_text):
            fragments.append(escape(original_text[cursor:]))

        text_node.replace_with(BeautifulSoup(''.join(fragments), 'html.parser'))

    return str(soup)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_resident_ip(ip):
    """
    Very basic check for Kenyan IP ranges or local dev.
    In production, this should use GeoIP2 or a proper service.
    """
    if not ip or ip in ['127.0.0.1', 'localhost', '::1']:
        return True
    return True  # Defaulting to resident for now as per plan


class OptimizedImageMixin:
    """
    Mixin to automatically generate WebP and mobile-optimized images.
    Requires the model to have:
    - An ImageField named 'image' (or specify source_field_name)
    - ImageFields named 'webp_image' and 'webp_mobile'
    """
    
    def convert_to_webp(self, source_field_name='image'):
        source_field = getattr(self, source_field_name, None)
        
        if not source_field:
            return

        try:
            img = Image.open(source_field.path)
            
            # Convert RGBA -> RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            # Use the source filename as base
            filename = os.path.splitext(os.path.basename(source_field.name))[0]
            
            # 1. Full Size WebP
            if hasattr(self, 'webp_image') and (not self.webp_image or not os.path.exists(self.webp_image.path if self.webp_image else '')): 
                webp_io = io.BytesIO()
                img.save(webp_io, format='WEBP', quality=85)
                self.webp_image.save(f'{filename}.webp', ContentFile(webp_io.getvalue()), save=False)
            
            # 2. Mobile Size (480w)
            if hasattr(self, 'webp_mobile') and (not self.webp_mobile or not os.path.exists(self.webp_mobile.path if self.webp_mobile else '')):
                img_mobile = img.copy()
                if img_mobile.width > 480:
                    aspect = img_mobile.height / img_mobile.width
                    img_mobile = img_mobile.resize((480, int(480 * aspect)), Image.Resampling.LANCZOS)
                
                mobile_io = io.BytesIO()
                img_mobile.save(mobile_io, format='WEBP', quality=85)
                self.webp_mobile.save(f'{filename}_mobile.webp', ContentFile(mobile_io.getvalue()), save=False)
            
            # Save ONLY the new fields to prevent recursion
            update_fields = []
            if hasattr(self, 'webp_image'):
                update_fields.append('webp_image')
            if hasattr(self, 'webp_mobile'):
                update_fields.append('webp_mobile')
                
            # Filter fields that actually exist on the model
            update_fields = [f for f in update_fields if hasattr(self, f)]
                
            if update_fields:
               # We use the class of 'self' to call the save method, trying to be generic
                super(self.__class__, self).save(update_fields=update_fields)
            
        except Exception as e:
            print(f"Error optimizing image for {source_field_name} in {self.__class__.__name__}: {e}")
