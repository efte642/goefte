from django.views.generic import ListView, DetailView
from .models import Post, Category
from taggit.models import Tag


class HomeView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Default queryset for homepage (optional if not directly used)
        return Post.objects.filter(published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sections for homepage
        context['hero_posts'] = Post.objects.filter(section='hero', published=True).order_by('-created_at')[:4]
        context['featured_posts'] = Post.objects.filter(section='featured', published=True).order_by('-created_at')[:4]
        context['popular_posts'] = Post.objects.filter(section='popular', published=True).order_by('-created_at')[:6]
        context['community_posts'] = Post.objects.filter(section='community', published=True).order_by('-created_at')[:4]
        context['recent_posts'] = Post.objects.filter(published=True).order_by('-created_at')[:6]
        context['categories'] = Category.objects.all()

        # SEO metadata for homepage
        context['meta_title'] = "Goefte Magazine – Lifestyle, Travel, Tech & Culture for USA and Canada"
        context['meta_description'] = "Goefte Magazine delivers trending stories on lifestyle, travel, tech, wellness, and culture for readers in the USA and Canada."
        context['meta_keywords'] = "Goefte, USA magazine, Canada magazine, online magazine, lifestyle trends, tech news, travel blog, wellness tips"
        context['meta_image'] = None  # Optional: homepage OG image

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # SEO
        context['hero_posts'] = Post.objects.filter(section='hero', published=True)
        context['featured_posts'] = Post.objects.filter(section='featured', published=True)
        context['recent_posts'] = Post.objects.filter(section='regular', published=True)[:6]  # latest 6 posts

        # Recent posts (excluding current post)
        context['recent_posts'] = Post.objects.filter(published=True).exclude(id=post.id).order_by('-created_at')[:5]

        # Related posts by same category (excluding current)
        context['related_posts'] = Post.objects.filter(
            category=post.category,
            published=True
        ).exclude(id=post.id).order_by('-created_at')[:5]

        # All categories (for sidebar/menu)
        context['categories'] = Category.objects.all()

        return context


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Get category slug from URL
        slug = self.kwargs.get('slug')
        # Filter posts by category slug and published=True
        return Post.objects.filter(category__slug=slug, published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        # Get category object
        category = Category.objects.filter(slug=slug).first()
        context['category'] = category

        # SEO metadata
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

        # Recent posts for sidebar
        context['recent_posts'] = Post.objects.filter(published=True).order_by('-created_at')[:5]
        

        return context


class TagPostView(ListView):
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            tags__slug=self.kwargs['slug'],
            published=True
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['slug']
        tag = Tag.objects.filter(slug=tag_slug).first()
        context['tag'] = tag or tag_slug

        # SEO for tag page
        context['meta_title'] = f"Posts tagged '{tag_slug}' – Goefte Magazine"
        context['meta_description'] = f"Explore all posts tagged with '{tag_slug}' on Goefte Magazine."
        context['meta_keywords'] = f"{tag_slug}, Goefte Magazine, USA, Canada"
        context['meta_image'] = None

        # Recent posts for sidebar
        context['recent_posts'] = Post.objects.filter(published=True).order_by('-created_at')[:5]

        return context
