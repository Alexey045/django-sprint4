from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("title", "slug")
    list_filter = ("is_published",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("name",)
    list_filter = ("is_published",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "pub_date", "author", "category", "is_published")
    list_editable = ("is_published",)
    search_fields = ("title", "text")
    list_filter = ("is_published", "category", "location")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")
    search_fields = ("text", "author__username", "post__title")
