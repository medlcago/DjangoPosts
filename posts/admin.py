from django.contrib import admin

from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("author__username",)
    list_display = ("title", "author", "is_published")
    list_filter = ("is_published",)
