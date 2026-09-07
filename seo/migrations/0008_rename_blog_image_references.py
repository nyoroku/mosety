from pathlib import Path
import shutil

from django.conf import settings
from django.db import migrations


def rename_blog_images(apps, schema_editor):
    post = apps.get_model('blog', 'Post')
    for old_name, new_name in [
        ('blog_images/katrue_wildlife_0.jpg', 'blog_images/paradise_wildlife_0.jpg'),
        ('blog_images/katrue_wildlife_1.jpg', 'blog_images/paradise_wildlife_1.jpg'),
    ]:
        source = Path(settings.MEDIA_ROOT) / old_name
        target = Path(settings.MEDIA_ROOT) / new_name
        if source.exists() and not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        post.objects.filter(image=old_name).update(image=new_name)


class Migration(migrations.Migration):
    dependencies = [
        ('seo', '0007_clean_legacy_brand_links'),
        ('blog', '0002_post_webp_image_post_webp_mobile'),
    ]

    operations = [
        migrations.RunPython(rename_blog_images, migrations.RunPython.noop),
    ]
