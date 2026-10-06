from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class ContactMessage(models.Model):
    INQUIRY_TYPES = [
        ("general", "General Inquiry"),
        ("project", "Project Collaboration"),
        ("job", "Job Opportunity"),
        ("freelance", "Freelance Work"),
        ("consultation", "Consultation"),
        ("support", "Technical Support"),
        ("feedback", "Feedback"),
    ]

    STATUS_CHOICES = [
        ("new", "New"),
        ("read", "Read"),
        ("replied", "Replied"),
        ("archived", "Archived"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    inquiry_type = models.CharField(
        max_length=20, choices=INQUIRY_TYPES, default="general"
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Project budget if applicable",
    )
    timeline = models.CharField(
        max_length=100, blank=True, help_text="Project timeline if applicable"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    is_urgent = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referral_source = models.CharField(
        max_length=100, blank=True, help_text="How did you find us?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def mark_as_read(self):
        self.status = "read"
        self.save(update_fields=["status"])

    def mark_as_replied(self):
        self.status = "replied"
        self.save(update_fields=["status"])


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    subscription_date = models.DateTimeField(auto_now_add=True)
    unsubscribe_date = models.DateTimeField(null=True, blank=True)
    unsubscribe_reason = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    referral_source = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["-subscription_date"]

    def __str__(self):
        return self.email

    def unsubscribe(self, reason=""):
        self.is_active = False
        self.unsubscribe_date = timezone.now()
        self.unsubscribe_reason = reason
        self.save()


class EmailTemplate(models.Model):
    TEMPLATE_TYPES = [
        ("contact_reply", "Contact Reply"),
        ("newsletter_welcome", "Newsletter Welcome"),
        ("newsletter_unsubscribe", "Newsletter Unsubscribe"),
        ("project_inquiry", "Project Inquiry"),
        ("auto_reply", "Auto Reply"),
    ]

    name = models.CharField(max_length=100, unique=True)
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=200)
    html_content = models.TextField()
    text_content = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
