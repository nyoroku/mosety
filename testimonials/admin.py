from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'staff_member', 'is_active', 'date_added')
    list_filter = ('is_active', 'rating', 'staff_member')
    search_fields = ('customer_name', 'testimonial_text')
    list_editable = ('is_active',)