from django.contrib import admin
from .models import FAQ, LocalPage, InternalLink, LocalPageImage, Redirect

class LocalPageImageInline(admin.TabularInline):
    model = LocalPageImage
    extra = 1

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order')

@admin.register(InternalLink)
class InternalLinkAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'url', 'is_active')

@admin.register(LocalPage)
class LocalPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'is_active', 'updated_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LocalPageImageInline]
    
    # Hide the legacy single 'image' field if needed, or keep it as the primary thumbnail
    fields = (
        'title', 
        'image', 
        'slug', 
        'is_active', 
        'allow_indexing',
        'seo_title', 
        'meta_description', 
        'primary_keyword', 
        'location', 
        'modifiers', 
        'content'
    )


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'status_code', 'is_active', 'created_at')
    list_filter = ('status_code', 'is_active')
    search_fields = ('old_path', 'new_path')