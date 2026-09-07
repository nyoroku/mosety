from django.db import migrations


def clean_legacy_brand_links(apps, schema_editor):
    internal_link = apps.get_model('seo', 'InternalLink')
    internal_link.objects.filter(url__icontains='katrue').update(url='/tours/')


class Migration(migrations.Migration):
    dependencies = [
        ('seo', '0006_replace_katrue_brand_references'),
    ]

    operations = [
        migrations.RunPython(clean_legacy_brand_links, migrations.RunPython.noop),
    ]
