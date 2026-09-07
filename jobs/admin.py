from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'is_active', 'posted_at')
    list_filter = ('is_active', 'posted_at')
    search_fields = ('title', 'location')