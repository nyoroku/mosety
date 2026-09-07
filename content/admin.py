from django.contrib import admin
from .models import Captain, GuideArticle, QuestionAnswer, Testimonial


@admin.register(Captain)
class CaptainAdmin(admin.ModelAdmin):
    list_display = ('name', 'years_on_lake', 'specialties', 'languages', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)


@admin.register(GuideArticle)
class GuideArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'author_name', 'published_at', 'is_featured', 'is_active')
    list_filter = ('content_type', 'is_featured', 'is_active')
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('related_tours',)


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'related_tour', 'sort_order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'rating', 'source', 'review_date', 'is_featured', 'is_active')
    list_filter = ('rating', 'source', 'is_featured', 'is_active')
    search_fields = ('display_name', 'review_text')
