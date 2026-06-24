from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Profile, SocialLink


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_available",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_active", "is_available", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined", "last_login")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "experience_years",
        "preferred_work_type",
        "hourly_rate",
        "created_at",
    )
    list_filter = ("preferred_work_type", "experience_years", "created_at")
    search_fields = ("user__username", "user__email", "title", "profession_titles")
    readonly_fields = ("cv_download_count", "last_active", "created_at", "updated_at")
    list_editable = ("preferred_work_type",)
    ordering = ("-created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("profile", "platform", "url", "is_active", "order")
    list_filter = ("is_active", "platform")
    search_fields = ("profile__user__username", "platform", "url")
    list_editable = ("is_active", "order")
    ordering = ("profile", "order")

    

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("profile")
