from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
import re
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    queryset = Post.objects.filter(status='published')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(status='published')

    def get(self, request, *args, **kwargs):
        legacy_slug = kwargs.get('slug', '')
        if 'katrue' in legacy_slug.lower():
            current_slug = re.sub(
                r'katrue',
                'paradise-boat-rides-naivasha',
                legacy_slug,
                flags=re.IGNORECASE,
            )
            if Post.objects.filter(slug=current_slug, status='published').exists():
                return redirect('blog:post_detail', slug=current_slug, permanent=True)
        return super().get(request, *args, **kwargs)
