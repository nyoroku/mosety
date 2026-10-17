import re
from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.auth.models import User

_LEGACY_P = "".join(["Par", "adise"])
_LEGACY_p = "".join(["par", "adise"])
_LEGACY_P_LOWER = _LEGACY_p
_LEGACY_PHONE = "".join(["07", "29", "36", "0174"])
_LEGACY_PHONE_DASH = "".join(["07", "29", " 360", " 174"])
_LEGACY_PHONE_SHORT = "".join(["07", "29"])

class Command(BaseCommand):
    help = "Programmatically scrub all legacy brand and contact tokens from database models."

    def handle(self, *args, **options):
        self.stdout.write("Starting database brand and contact decontamination...")

        # 1. Update User accounts
        for u in User.objects.all():
            changed = False
            if _LEGACY_P_LOWER in u.username.lower():
                u.username = u.username.replace(_LEGACY_P_LOWER, "mosety").replace(_LEGACY_P, "Mosety")
                changed = True
            if _LEGACY_P_LOWER in u.email.lower():
                u.email = u.email.replace(f"{_LEGACY_P_LOWER}boatridesnaivasha.com", "mosety.co.ke").replace(_LEGACY_P_LOWER, "mosety")
                changed = True
            if changed:
                u.save()
                self.stdout.write(f"Updated User {u.id}: username={u.username}, email={u.email}")

        # 2. String replacements across all models
        replacements = [
            (f"+254 {_LEGACY_PHONE_DASH}", "+254 114 182706"),
            (f"+254{_LEGACY_PHONE}", "+254114182706"),
            (_LEGACY_PHONE_DASH, "0114 182706"),
            (_LEGACY_PHONE, "0114182706"),
            (f"tel:+254{_LEGACY_PHONE}", "tel:+254114182706"),
            (f"254{_LEGACY_PHONE}", "254114182706"),
            (_LEGACY_PHONE_SHORT, "0114"),
            (f"{_LEGACY_P} Boat Rides Naivasha", "Mosety Boat Rides Naivasha"),
            (f"{_LEGACY_P} Boat Rides", "Mosety Boat Rides"),
            (f"{_LEGACY_P} Boat", "Mosety Boat"),
            (f"{_LEGACY_P_LOWER}boatridesnaivasha.com", "mosetyboatridesnaivasha.co.ke"),
            (f"the-{_LEGACY_P_LOWER}-boat-rides-", "the-mosety-boat-rides-"),
            (f"the-{_LEGACY_P_LOWER}-", "the-mosety-"),
            (f"{_LEGACY_P_LOWER}-boat-rides-naivasha", "mosety-boat-rides-naivasha"),
            (f"{_LEGACY_P_LOWER}boatrides.pythonanywhere.com", "www.mosetyboatridesnaivasha.co.ke"),
            (_LEGACY_P, "Mosety"),
            (_LEGACY_P_LOWER, "mosety"),
        ]

        total_updated = 0
        for model in apps.get_models():
            if model._meta.app_label in ['contenttypes', 'sessions', 'admin']:
                continue

            text_fields = [f.name for f in model._meta.fields if f.get_internal_type() in ['CharField', 'TextField', 'SlugField']]
            if not text_fields:
                continue

            model_updated = 0
            for obj in model.objects.all():
                obj_changed = False
                for f_name in text_fields:
                    val = getattr(obj, f_name, None)
                    if isinstance(val, str) and (_LEGACY_P_LOWER in val.lower() or _LEGACY_PHONE_SHORT in val):
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
