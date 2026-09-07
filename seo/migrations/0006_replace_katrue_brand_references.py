import re

from django.db import migrations


BRAND_RE = re.compile(r"katrue(?:\s+boat\s+rides?)?", re.IGNORECASE)
BRAND_NAME = "Paradise Boat Rides Naivasha"


def replace_brand_references(apps, schema_editor):
    content_models = [
        ('blog', 'Post'),
        ('seo', 'FAQ'),
        ('seo', 'LocalPage'),
        ('services', 'Service'),
        ('accommodation', 'PartnerHotel'),
        ('bookings', 'Tour'),
        ('testimonials', 'Testimonial'),
    ]

    for app_label, model_name in content_models:
        model = apps.get_model(app_label, model_name)
        text_fields = [
            field for field in model._meta.fields
            if field.name != 'slug' and field.get_internal_type() in {'CharField', 'TextField'}
        ]
        for obj in model.objects.all().iterator():
            changed_fields = []
            for field in text_fields:
                value = getattr(obj, field.name, None)
                if not isinstance(value, str) or not BRAND_RE.search(value):
                    continue
                updated = BRAND_RE.sub(BRAND_NAME, value)
                if updated != value:
                    setattr(obj, field.name, updated)
                    changed_fields.append(field.name)
            if changed_fields:
                obj.save(update_fields=changed_fields)

    internal_link = apps.get_model('seo', 'InternalLink')
    keyword_map = {
        'Katrue Boat Rides': 'Paradise Boat Rides',
        'Katrue': 'Paradise Boat Rides Naivasha',
    }
    for old_keyword, new_keyword in keyword_map.items():
        old_link = internal_link.objects.filter(keyword__iexact=old_keyword).first()
        if not old_link:
            continue
        target_link = internal_link.objects.filter(keyword=new_keyword).exclude(pk=old_link.pk).first()
        if target_link:
            old_link.delete()
        else:
            old_link.keyword = new_keyword
            old_link.url = '/' if new_keyword.endswith('Naivasha') else '/tours/'
            old_link.save(update_fields=['keyword', 'url'])

    for keyword, url in [
        ('Paradise Boat Rides', '/'),
        ('Paradise Boat Rides Naivasha', '/'),
        ('call Paradise Boat Rides', 'tel:+254729360174'),
        ('book Paradise Boat Rides', '/tours/'),
    ]:
        internal_link.objects.get_or_create(keyword=keyword, defaults={'url': url, 'is_active': True})


class Migration(migrations.Migration):
    dependencies = [
        ('seo', '0005_localpage_webp_image_localpage_webp_mobile_and_more'),
        ('blog', '0002_post_webp_image_post_webp_mobile'),
        ('services', '0003_service_webp_image_service_webp_mobile'),
        ('accommodation', '0003_hotelimage_webp_image_hotelimage_webp_mobile_and_more'),
        ('bookings', '0005_tour_webp_image_tour_webp_mobile'),
        ('testimonials', '0003_testimonial_is_featured'),
    ]

    operations = [
        migrations.RunPython(replace_brand_references, migrations.RunPython.noop),
    ]
