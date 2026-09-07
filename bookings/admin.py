from django.contrib import admin
from .models import Tour, Booking

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_hours', 'price_resident', 'price_international', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'tour', 'booking_date', 'number_of_people', 'total_price', 'status')
    list_filter = ('status', 'tour', 'booking_date')
    search_fields = ('customer_name', 'customer_email')
    readonly_fields = ('booking_date',)