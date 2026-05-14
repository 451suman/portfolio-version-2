from django.contrib import admin
from django.db.models import Count
from .models import Skill, Experience, Project, ProjectImage


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "level",
        "percentage",
        "is_featured",
        "order",
        "created_at",
    )
    list_filter = ("level", "is_featured", "created_at")
    search_fields = ("name",)
    list_editable = ("percentage", "is_featured", "order")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-is_featured", "order", "name")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "position",
        "company",
        "location",
        "is_current",
        "start_date",
        "end_date",
    )
    list_filter = ("is_current", "employment_type", "start_date")
    search_fields = ("position", "company", "location")
    readonly_fields = ("created_at",)
    list_editable = ("is_current",)
    ordering = ("-is_current", "-start_date")

    fieldsets = (
        ("Basic Info", {"fields": ("position", "company", "location")}),
        ("Duration", {"fields": ("start_date", "end_date", "is_current")}),
        ("Details", {"fields": ("description", "employment_type", "team_size")}),
        ("Technologies", {"fields": ("technologies",)}),
        ("Timestamps", {"fields": ("created_at",)}),
    )

    filter_horizontal = ("technologies",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("technologies")


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "title", "description", "order", "is_featured")
    ordering = ("order",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("project")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "status",
        "is_featured",
        "is_open_source",
        "show_github_button",
        "show_live_button",
        "show_demo_button",
        "start_date",
        "view_count",
        "created_at",
    )
    list_filter = (
        "status",
        "is_featured",
        "is_open_source",
        "show_github_button",
        "show_live_button",
        "show_demo_button",
        "start_date",
    )
    search_fields = ("title", "description", "short_description")
    list_editable = (
        "status",
        "is_featured",
        "is_open_source",
        "show_github_button",
        "show_live_button",
        "show_demo_button",
    )
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    inlines = [ProjectImageInline]
    readonly_fields = ("view_count", "like_count", "created_at", "updated_at")
    ordering = ("-is_featured", "-created_at")

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("title", "slug", "status", "is_featured", "is_open_source")},
        ),
        ("Description", {"fields": ("short_description", "description")}),
        ("Media", {"fields": ("featured_image",)}),
        ("Links", {"fields": ("github_url", "live_url", "demo_url")}),
        (
            "Display Controls",
            {"fields": ("show_github_button", "show_live_button", "show_demo_button")},
        ),
        (
            "Project Details",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "duration_weeks",
                    "team_size",
                    "client_name",
                    "budget",
                )
            },
        ),
        ("Technical", {"fields": ("technologies",)}),
        ("Documentation", {"fields": ("challenges", "architecture")}),
        (
            "Statistics",
            {"fields": ("view_count", "like_count", "created_at", "updated_at")},
        ),
    )


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "title", "order", "created_at")
    list_filter = ("created_at",)
    search_fields = ("project__title", "title", "description")
    readonly_fields = ("created_at",)
    list_editable = ("order",)
    ordering = ("project", "order")

    fieldsets = (
        ("Basic Info", {"fields": ("project", "title", "description")}),
        ("Display", {"fields": ("order",)}),
        ("Timestamps", {"fields": ("created_at",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("project")
