from django.contrib import admin
from .models import PartnerHotel, HotelImage

class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1

@admin.register(PartnerHotel)
class PartnerHotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'location')
    search_fields = ('name', 'description', 'location')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [HotelImageInline]

@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'caption', 'order')
    list_filter = ('hotel',)
