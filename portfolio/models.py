from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(
        max_length=50, blank=True, help_text="Font Awesome icon class"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    color = models.CharField(
        max_length=7, default="#007bff", help_text="Hex color code"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Skill(models.Model):
    SKILL_LEVELS = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    level = models.CharField(
        max_length=20, choices=SKILL_LEVELS, default="intermediate"
    )
    percentage = models.PositiveIntegerField(
        default=50, help_text="Skill percentage for progress bars"
    )
    icon_class = models.CharField(
        max_length=100, blank=True, help_text="Font Awesome icon class"
    )
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "order", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Experience(models.Model):
    EMPLOYMENT_TYPES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("freelance", "Freelance"),
        ("internship", "Internship"),
        ("contract", "Contract"),
    ]

    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_TYPES, default="full_time"
    )
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(
        null=True, blank=True, help_text="Leave empty if current job"
    )
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    achievements = models.JSONField(default=list, help_text="List of achievements")
    technologies = models.ManyToManyField(Skill, related_name="experiences", blank=True)
    company_logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    company_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_current", "-start_date", "order"]

    def __str__(self):
        return f"{self.position} at {self.company}"

    @property
    def duration(self):
        if self.end_date:
            return self.end_date.year - self.start_date.year
        return "Present"


class Project(models.Model):
    PROJECT_STATUS = [
        ("planning", "Planning"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("on_hold", "On Hold"),
        ("cancelled", "Cancelled"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    status = models.CharField(
        max_length=20, choices=PROJECT_STATUS, default="completed"
    )
    featured_image = models.ImageField(
        upload_to="projects/featured/", blank=True, null=True
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_open_source = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    duration_weeks = models.PositiveIntegerField(null=True, blank=True)
    team_size = models.PositiveIntegerField(default=1)
    client_name = models.CharField(max_length=200, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    challenges = models.TextField(
        blank=True, help_text="Challenges faced and solutions"
    )
    architecture = models.TextField(
        blank=True, help_text="Technical architecture details"
    )
    technologies = models.ManyToManyField(Skill, related_name="projects", blank=True)
    categories = models.ManyToManyField(Category, related_name="projects", blank=True)
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=["view_count"])


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="projects/gallery/")
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} - Image {self.order}"
