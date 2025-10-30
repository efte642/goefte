from django.views.generic import ListView, DetailView
from .models import Post, Category
from taggit.models import Tag


class HomeView(ListView):
    model = Post
    template_name = 'index.html'  # root templates folder
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_posts'] = Post.objects.filter(section='hero', published=True).order_by('-created_at')[:4]
        context['featured_posts'] = Post.objects.filter(section='featured', published=True).order_by('-created_at')[:4]
        context['popular_posts'] = Post.objects.filter(section='popular', published=True).order_by('-created_at')[:6]
        context['community_posts'] = Post.objects.filter(section='community', published=True).order_by('-created_at')[:4]
        context['recent_posts'] = Post.objects.filter(published=True).order_by('-created_at')[:6]
        context['categories'] = Category.objects.all()
        context['meta_title'] = "Goefte Magazine – Lifestyle, Travel, Tech & Culture for USA and Canada"
        context['meta_description'] = "Goefte Magazine delivers trending stories on lifestyle, travel, tech, wellness, and culture for readers in the USA and Canada."
        context['meta_keywords'] = "Goefte, USA magazine, Canada magazine, online magazine, lifestyle trends, tech news, travel blog, wellness tips"
        context['meta_image'] = None
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'  # root templates folder
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['hero_posts'] = Post.objects.filter(section='hero', published=True)
        context['featured_posts'] = Post.objects.filter(section='featured', published=True)
        context['recent_posts'] = Post.objects.filter(published=True).exclude(id=post.id).order_by('-created_at')[:5]
        context['related_posts'] = Post.objects.filter(category=post.category, published=True).exclude(id=post.id).order_by('-created_at')[:3]
        context['categories'] = Category.objects.all()
        return context


class CategoryPostView(ListView):
    model = Post
    template_name = 'category_posts.html'  # root templates folder
    context_object_name = 'posts'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Post.objects.filter(category__slug=slug, published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        category = Category.objects.filter(slug=slug).first()
        context['category'] = category

        if category:
            context['meta_title'] = f"{category.name} – Goefte Magazine"
            context['meta_description'] = f"Read all articles and posts about {category.name} on Goefte Magazine."
            context['meta_keywords'] = f"{category.name}, Goefte Magazine, USA, Canada"
            context['meta_image'] = category.image
        else:
            context['meta_title'] = "Category – Goefte Magazine"
            context['meta_description'] = "Posts in this category."
            context['meta_keywords'] = "Goefte Magazine"
            context['meta_image'] = None

        context['recent_posts'] = Post.objects.filter(published=True).order_by('-created_at')[:5]
        return context


class TagPostView(ListView):
    template_name = 'tag_posts.html'  # root templates folder
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'], published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['slug']
        tag = Tag.objects.filter(slug=tag_slug).first()
        context['tag'] = tag or tag_slug
        context['meta_title'] = f"Posts tagged '{tag_slug}' – Goefte Magazine"
        context['meta_description'] = f"Explore all posts tagged with '{tag_slug}' on Goefte Magazine."
        context['meta_keywords'] = f"{tag_slug}, Goefte Magazine, USA, Canada"
        context['meta_image'] = None
        context['recent_posts'] = Post.objects.filter(published=True).order_by('-created_at')[:5]
        return context
