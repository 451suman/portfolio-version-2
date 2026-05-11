from re import T
from django.contrib import admin
from .models import BlogPost, Comment, Category, Tag

admin.site.register(Category)
admin.site.register(Tag)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "author",
        "status",
        "is_featured",
        "published_at",
        "view_count",
        "comment_count",
        "created_at",
    )
    list_filter = ("status", "is_featured", "published_at", "created_at")
    search_fields = ("title", "content", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = (
        "view_count",
        "comment_count",
        "reading_time",
        "created_at",
        "updated_at",
    )
    list_editable = ("is_featured", "status")
    ordering = ("-is_featured", "-published_at", "-created_at")
    filter_horizontal = ("categories", "tags")

    fieldsets = (
        ("Basic Info", {"fields": ("title", "slug", "excerpt")}),
        ("Content", {"fields": ("content",)}),
        ("Status", {"fields": ("status", "is_featured")}),
        ("Publishing", {"fields": ("author", "published_at")}),
        ("Media", {"fields": ("featured_image",)}),
        ("Relationships", {"fields": ("categories", "tags")}),
        ("Statistics", {"fields": ("view_count", "comment_count", "reading_time")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("author")
            .prefetch_related("categories", "tags")
        )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "post",
        "email",
        "is_approved",
        "parent",
        "created_at",
    )
    list_filter = ("is_approved", "created_at")
    search_fields = ("name", "email", "content", "post__title")
    readonly_fields = ("ip_address", "user_agent", "created_at", "updated_at")
    list_editable = ("is_approved",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Comment Info", {"fields": ("post", "parent", "name", "email", "website")}),
        ("Content", {"fields": ("content",)}),
        ("Status", {"fields": ("is_approved",)}),
        ("Metadata", {"fields": ("ip_address", "user_agent")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("post", "parent")
