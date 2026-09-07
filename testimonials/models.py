from django.db import models
from django.utils.timezone import now

class Testimonial(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    customer_name = models.CharField(max_length=100)
    customer_country = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. USA, UK, Kenya")
    tour = models.ForeignKey(
        'bookings.Tour', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='testimonials'
    )
    staff_member = models.ForeignKey(
        'reputation.StaffMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonials',
        help_text="Attribute this review to a specific captain or guide."
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    testimonial_text = models.TextField()
    date_added = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-date_added']

    def __str__(self):
        return f"{self.customer_name} - {self.rating} Stars"

    def get_star_rating(self):
        return "★" * self.rating + "☆" * (5 - self.rating)