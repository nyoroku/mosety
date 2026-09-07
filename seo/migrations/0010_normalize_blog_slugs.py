import re

from django.db import migrations


def normalize_blog_slugs(apps, schema_editor):
    post = apps.get_model('blog', 'Post')
    for item in post.objects.filter(slug__icontains='katrue').iterator():
        item.slug = re.sub(
            r'katrue',
            'paradise-boat-rides-naivasha',
            item.slug,
            flags=re.IGNORECASE,
        )
        item.save(update_fields=['slug'])


class Migration(migrations.Migration):
    dependencies = [
        ('seo', '0009_normalize_brand_phrasing'),
    ]

    operations = [
        migrations.RunPython(normalize_blog_slugs, migrations.RunPython.noop),
    ]
