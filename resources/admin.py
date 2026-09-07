from django.contrib import admin
from .models import ResourceCategory, GuidePage, FAQItem, PricingTier, DownloadAsset

class FAQItemInline(admin.TabularInline):
    model = FAQItem
    extra = 1

class DownloadAssetInline(admin.TabularInline):
    model = DownloadAsset
    extra = 0

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'sort_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('sort_order',)

@admin.register(GuidePage)
class GuidePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_pillar', 'is_active', 'updated_at')
    list_filter = ('category', 'is_pillar', 'is_active')
    search_fields = ('title', 'intro_answer', 'body')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [FAQItemInline, DownloadAssetInline]

@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'guide_page', 'sort_order', 'is_active')
    list_filter = ('category', 'guide_page', 'is_active')
    search_fields = ('question', 'answer')
    list_editable = ('sort_order',)

@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    list_display = ('tour_type', 'group_size_label', 'price_kes', 'price_usd', 'sort_order', 'is_active')
    list_editable = ('price_kes', 'price_usd', 'sort_order')

@admin.register(DownloadAsset)
class DownloadAssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'guide_page', 'file_type', 'created_at')
