import re

from django.db import migrations


def normalize_tour_slugs(apps, schema_editor):
    tour = apps.get_model('bookings', 'Tour')
    for item in tour.objects.filter(slug__icontains='katrue').iterator():
        item.slug = re.sub(
            r'katrue',
            'paradise-boat-rides-naivasha',
            item.slug,
            flags=re.IGNORECASE,
        )
        item.save(update_fields=['slug'])


class Migration(migrations.Migration):
    dependencies = [
        ('seo', '0010_normalize_blog_slugs'),
    ]

    operations = [
        migrations.RunPython(normalize_tour_slugs, migrations.RunPython.noop),
    ]
