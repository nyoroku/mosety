import re
from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Programmatically scrub all legacy brand tokens (Paradise) from database models."

    def handle(self, *args, **options):
        self.stdout.write("Starting database brand decontamination...")

        # 1. Update User accounts
        for u in User.objects.all():
            changed = False
            if "paradise" in u.username.lower():
                u.username = u.username.replace("paradise", "mosety").replace("Paradise", "Mosety")
                changed = True
            if "paradise" in u.email.lower():
                u.email = u.email.replace("paradiseboatridesnaivasha.com", "mosety.co.ke").replace("paradise", "mosety")
                changed = True
            if changed:
                u.save()
                self.stdout.write(f"Updated User {u.id}: username={u.username}, email={u.email}")

        # 2. String replacements across all models
        replacements = [
            ("Paradise Boat Rides Naivasha", "Mosety Boat Rides Naivasha"),
            ("Paradise Boat Rides", "Mosety Boat Rides"),
            ("Paradise Boat", "Mosety Boat"),
            ("paradiseboatridesnaivasha.com", "mosetyboatridesnaivasha.co.ke"),
            ("paradise-boat-rides-naivasha", "mosety-boat-rides-naivasha"),
            ("paradiseboatrides.pythonanywhere.com", "www.mosetyboatridesnaivasha.co.ke"),
            ("0729360174", "+254 114 182706"),
            ("Paradise", "Mosety"),
            ("paradise", "mosety"),
        ]

        total_updated = 0
        for model in apps.get_models():
            # Skip django internal models that don't need text scrubbing
            if model._meta.app_label in ['contenttypes', 'sessions', 'admin']:
                continue

            text_fields = [f.name for f in model._meta.fields if f.get_internal_type() in ['CharField', 'TextField']]
            if not text_fields:
                continue

            model_updated = 0
            for obj in model.objects.all():
                obj_changed = False
                for f_name in text_fields:
                    val = getattr(obj, f_name, None)
                    if isinstance(val, str) and ("paradise" in val.lower() or "0729360174" in val):
                        new_val = val
                        for old, new in replacements:
                            new_val = re.sub(re.escape(old), new, new_val, flags=re.IGNORECASE)
                        if new_val != val:
                            setattr(obj, f_name, new_val)
                            obj_changed = True
                
                if obj_changed:
                    obj.save()
                    model_updated += 1
            
            if model_updated > 0:
                self.stdout.write(f"Model {model.__name__}: updated {model_updated} records.")
                total_updated += model_updated

        self.stdout.write(self.style.SUCCESS(f"Decontamination complete! Total records updated: {total_updated}"))
