from django.contrib import admin
from .models import Category, Post
from taggit.admin import TagAdmin
from taggit.models import Tag

# Unregister the default Tag model if it's already registered
try:
    admin.site.unregister(Tag)
except admin.sites.NotRegistered:
    pass

# Register Tag model with TagAdmin for autocomplete support
@admin.register(Tag)
class CustomTagAdmin(TagAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'section', 'published', 'views', 'created_at')
    list_filter = ('category', 'section', 'published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('tags',)
    readonly_fields = ('views', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'image', 'content', 'tags', 'section', 'published')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Timestamps', {
            'fields': ('views', 'created_at', 'updated_at')
        }),
    )
