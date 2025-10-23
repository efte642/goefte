# blog/urls.py
from django.urls import path
from .views import HomeView, PostDetailView, CategoryPostView, TagPostView

app_name = 'blog'  # <- ADD THIS

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'), 
    path('category/<slug:slug>/', CategoryPostView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/', TagPostView.as_view(), name='tag_posts'),
]
