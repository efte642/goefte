from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    SECTION_CHOICES = (
        ('hero', 'Hero'),
        ('featured', 'Featured'),
        ('popular', 'Popular'),
        ('regular', 'Regular'),
        ('community', 'Community Highlights'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    content = RichTextField()
    tags = TaggableManager(blank=True)

    section = models.CharField(
        max_length=20,
        choices=SECTION_CHOICES,
        default='regular',
        help_text="Select which section this post will appear in (e.g., Hero, Featured, Popular, etc.)"
    )

    published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0, help_text="Auto-updated count of post views")

    # SEO Fields
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        help_text="Recommended: 50–60 characters"
    )
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        help_text="Recommended: 120–160 characters"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug if empty
        if not self.slug:
            self.slug = slugify(self.title)
        # Auto-fill meta_title if not provided
        if not self.meta_title:
            self.meta_title = self.title[:60]
        super().save(*args, **kwargs)
