from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


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


class BlogPost(models.Model):
    POST_STATUS = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    excerpt = models.CharField(
        max_length=300, help_text="Short description for previews"
    )
    featured_image = models.ImageField(
        upload_to="blog/featured/", blank=True, null=True
    )
    status = models.CharField(max_length=20, choices=POST_STATUS, default="draft")
    is_featured = models.BooleanField(default=False)
    reading_time = models.PositiveIntegerField(
        default=5, help_text="Estimated reading time in minutes"
    )
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO meta title")
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="SEO meta description"
    )
    categories = models.ManyToManyField(
        "Category", related_name="blog_posts", blank=True
    )
    tags = models.ManyToManyField("Tag", related_name="blog_posts", blank=True)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=["view_count"])

    def update_comment_count(self):
        self.comment_count = self.comments.filter(is_approved=True).count()
        self.save(update_fields=["comment_count"])

    @property
    def related_posts(self):
        return (
            BlogPost.objects.filter(categories__in=self.categories.all())
            .exclude(id=self.id)
            .distinct()[:3]
        )


class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="comments"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"

    @property
    def is_reply(self):
        return self.parent is not None

    @property
    def replies(self):
        return Comment.objects.filter(parent=self, is_approved=True).order_by(
            "created_at"
        )
