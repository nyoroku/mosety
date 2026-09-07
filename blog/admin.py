# blog/admin.py
from django.contrib import admin
from .models import Post
from tinymce.widgets import TinyMCE
from django import forms
from utils import auto_link  # make sure this exists

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Post
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Apply keyword auto-linking before saving
        instance.content = auto_link(instance.content)
        if commit:
            instance.save()
        return instance

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('status', '-created_at')

    class Media:
        js = ("js/tinymce-config.js",)  # optional, if you have extra JS


