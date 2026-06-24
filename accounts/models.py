from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    github_username = models.CharField(max_length=50, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_username = models.CharField(max_length=50, blank=True)
    is_available = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"username": self.username})


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Backend Developer")
    profession_titles = models.JSONField(
        default=list,
        help_text="List of profession titles for rotation eg: ['Backend Developer', 'Full Stack Developer']",
    )
    phone = models.CharField(max_length=20, blank=True)
    resume_file = models.FileField(upload_to="resumes/", blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    preferred_work_type = models.CharField(
        max_length=20,
        choices=[
            ("full_time", "Full Time"),
            ("part_time", "Part Time"),
            ("freelance", "Freelance"),
            ("contract", "Contract"),
        ],
        default="full_time",
    )
    skills_summary = models.TextField(blank=True)
    about_short = models.CharField(max_length=200, blank=True)
    about_detailed = models.TextField(blank=True)
    cv_download_count = models.PositiveIntegerField(default=0)
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def increase_cv_download_count(self):
        self.cv_download_count += 1
        self.save()


class SocialLink(models.Model):
    PlatformChoices = [
        ("linkedin", "LinkedIn"),
        ("facebook", "Facebook"),
        ("github", "GitHub"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
        ("website", "Website"),
        ("youtube", "YouTube"),
    ]

    ICON_MAP = {
        "linkedin": "fab fa-linkedin",
        "facebook": "fab fa-facebook",
        "github": "fab fa-github",
        "twitter": "fab fa-twitter",
        "instagram": "fab fa-instagram",
        "website": "fas fa-globe",
        "youtube": "fab fa-youtube",
    }

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="social_links"
    )
    platform = models.CharField(max_length=50, choices=PlatformChoices)
    url = models.URLField()
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="icon is automatically set based on platform, but you can override it if needed from https://fontawesome.com/icons/",
    )

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        self.icon_class = self.ICON_MAP.get(self.platform, "")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.platform} - {self.profile.user.username}"
