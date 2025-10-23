from django.contrib import admin
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'section', 'published', 'created_at')
    list_filter = ('category', 'section', 'published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('published', 'section')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    autocomplete_fields = ('category',)
    autocomplete_fields = ('tags',)
