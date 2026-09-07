from django.core.management.base import BaseCommand
from bookings.models import Tour
from accommodation.models import PartnerHotel, HotelImage
from blog.models import Post
from seo.models import LocalPage, LocalPageImage
from reputation.models import StaffMember
from services.models import Service

class Command(BaseCommand):
    help = 'Converts existing images to WebP format for all models'

    def handle(self, *args, **options):
        self.stdout.write("Starting image conversion...")

        # Tours
        self.stdout.write("Processing Tours...")
        for tour in Tour.objects.all():
            if tour.image:
                self.stdout.write(f"  Optimizing {tour.name}")
                tour.save()

        # Hotels
        self.stdout.write("Processing Hotels...")
        for hotel in PartnerHotel.objects.all():
            if hotel.main_image:
                self.stdout.write(f"  Optimizing {hotel.name}")
                hotel.save()
        
        self.stdout.write("Processing Hotel Images...")
        for img in HotelImage.objects.all():
            if img.image:
                self.stdout.write(f"  Optimizing Hotel Image {img.id}")
                img.save()

        # Blog Posts
        self.stdout.write("Processing Blog Posts...")
        for post in Post.objects.all():
            if post.image:
                self.stdout.write(f"  Optimizing {post.title}")
                post.save()

        # Local Pages
        self.stdout.write("Processing Local Pages...")
        for page in LocalPage.objects.all():
            if page.image:
                self.stdout.write(f"  Optimizing {page.title}")
                page.save()

        self.stdout.write("Processing Local Page Images...")
        for img in LocalPageImage.objects.all():
            if img.image:
                self.stdout.write(f"  Optimizing Local Page Image {img.id}")
                img.save()

        # Staff
        self.stdout.write("Processing Staff...")
        for staff in StaffMember.objects.all():
            if staff.photo:
                self.stdout.write(f"  Optimizing {staff.name}")
                staff.save()

        # Services
        self.stdout.write("Processing Services...")
        for service in Service.objects.all():
            if service.image:
                self.stdout.write(f"  Optimizing {service.title}")
                service.save()

        self.stdout.write(self.style.SUCCESS('Successfully converted all images to WebP!'))
