from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "publisher",
        "approved",
        "created_at",
    )
    list_filter = (
        "approved",
        "publisher",
    )
    search_fields = (
        "title",
        "content",
        "author__username",
    )
    ordering = ("-created_at",)
