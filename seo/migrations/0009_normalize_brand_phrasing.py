from django.db import migrations


def normalize_brand_phrasing(apps, schema_editor):
    content_models = [
        ('blog', 'Post'),
        ('seo', 'FAQ'),
        ('seo', 'LocalPage'),
        ('services', 'Service'),
        ('accommodation', 'PartnerHotel'),
        ('bookings', 'Tour'),
        ('testimonials', 'Testimonial'),
    ]
    duplicate = 'Paradise Boat Rides Naivasha Naivasha'
    brand = 'Paradise Boat Rides Naivasha'
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
                if isinstance(value, str) and duplicate in value:
                    setattr(obj, field.name, value.replace(duplicate, brand))
                    changed_fields.append(field.name)
            if changed_fields:
                obj.save(update_fields=changed_fields)


class Migration(migrations.Migration):
    dependencies = [
        ('seo', '0008_rename_blog_image_references'),
    ]

    operations = [
        migrations.RunPython(normalize_brand_phrasing, migrations.RunPython.noop),
    ]
