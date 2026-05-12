from django.contrib import admin
from .models import ContactMessage, NewsletterSubscription, EmailTemplate


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "inquiry_type",
        "is_urgent",
        "status",
        "created_at",
    )
    list_filter = ("status", "inquiry_type", "is_urgent", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("ip_address", "user_agent", "created_at", "updated_at")
    list_editable = ("status",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Contact Info", {"fields": ("name", "email", "phone", "company")}),
        ("Message", {"fields": ("subject", "inquiry_type", "message")}),
        ("Project Details", {"fields": ("budget", "timeline", "is_urgent")}),
        ("Status", {"fields": ("status",)}),
        ("Metadata", {"fields": ("ip_address", "user_agent", "referral_source")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    actions = ["mark_as_read", "mark_as_unread", "mark_as_responded"]

    def mark_as_read(self, request, queryset):
        queryset.update(status="read")

    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(status="unread")

    mark_as_unread.short_description = "Mark selected messages as unread"

    def mark_as_responded(self, request, queryset):
        queryset.update(status="responded")

    mark_as_responded.short_description = "Mark selected messages as responded"


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "subscription_date",
        "unsubscribe_date",
    )
    list_filter = ("is_active", "subscription_date", "unsubscribe_date")
    search_fields = ("email", "first_name", "last_name")
    list_editable = ("is_active",)
    readonly_fields = ("subscription_date", "unsubscribe_date", "ip_address")
    ordering = ("-subscription_date",)

    fieldsets = (
        ("Subscriber Info", {"fields": ("email", "first_name", "last_name")}),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "subscription_date",
                    "unsubscribe_date",
                    "unsubscribe_reason",
                )
            },
        ),
        ("Technical", {"fields": ("ip_address", "referral_source")}),
    )

    actions = ["unsubscribe_selected", "resubscribe_selected"]

    def unsubscribe_selected(self, request, queryset):
        queryset.update(is_active=False)

    unsubscribe_selected.short_description = "Unsubscribe selected subscribers"

    def resubscribe_selected(self, request, queryset):
        queryset.update(is_active=True, unsubscribe_date=None, unsubscribe_reason="")

    resubscribe_selected.short_description = "Resubscribe selected subscribers"


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "subject", "description")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("is_active",)
    ordering = ("name",)

    fieldsets = (
        ("Basic Info", {"fields": ("name", "description")}),
        ("Email Content", {"fields": ("subject", "html_content", "text_content")}),
        ("Status", {"fields": ("is_active",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")
