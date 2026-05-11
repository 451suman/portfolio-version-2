from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import BlogPost, Comment
from portfolio.models import Category, Tag


class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        queryset = (
            BlogPost.objects.filter(status="published")
            .select_related("author")
            .prefetch_related("categories", "tags", "comments")
            .order_by("-published_at", "-created_at")
        )

        # Search functionality
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(content__icontains=search_query)
                | Q(excerpt__icontains=search_query)
                | Q(categories__name__icontains=search_query)
                | Q(tags__name__icontains=search_query)
            ).distinct()

        # Category filter
        category_slug = self.request.GET.get("category", "")
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)

        # Tag filter
        tag_slug = self.request.GET.get("tag", "")
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filters for sidebar
        context["categories"] = (
            Category.objects.filter(is_active=True, blog_posts__status="published")
            .distinct()
            .order_by("order")
        )

        context["tags"] = (
            Tag.objects.filter(blog_posts__status="published")
            .distinct()
            .order_by("name")
        )

        # Get current filters
        context["current_category"] = self.request.GET.get("category", "")
        context["current_tag"] = self.request.GET.get("tag", "")
        context["search_query"] = self.request.GET.get("search", "")

        # Featured posts
        context["featured_posts"] = (
            BlogPost.objects.filter(status="published", is_featured=True)
            .select_related("author")
            .prefetch_related("categories", "tags")[:3]
        )

        # Recent posts
        context["recent_posts"] = (
            BlogPost.objects.filter(status="published")
            .select_related("author")
            .prefetch_related("categories", "tags")[:5]
        )

        # Blog statistics
        context["blog_stats"] = {
            "total_posts": BlogPost.objects.filter(status="published").count(),
            "total_categories": Category.objects.filter(
                is_active=True, blog_posts__status="published"
            )
            .distinct()
            .count(),
            "total_tags": Tag.objects.filter(blog_posts__status="published")
            .distinct()
            .count(),
        }

        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return (
            BlogPost.objects.filter(status="published")
            .select_related("author")
            .prefetch_related("categories", "tags", "comments")
        )

    def get_object(self):
        slug = self.kwargs.get("slug")
        post = get_object_or_404(BlogPost, slug=slug, status="published")

        # Increase view count
        post.increase_view_count()

        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Add comment form
        from .forms import CommentForm

        context["comment_form"] = CommentForm()

        # Get approved comments (top-level only)
        context["comments"] = (
            post.comments.filter(is_approved=True, parent=None)
            .select_related("post")
            .prefetch_related("replies")
            .order_by("created_at")
        )

        # Get related posts
        context["related_posts"] = post.related_posts

        # Get all posts for navigation
        context["all_posts"] = BlogPost.objects.filter(status="published").order_by(
            "-published_at", "-created_at"
        )

        # Get categories and tags for sidebar
        from portfolio.models import Category, Tag

        context["categories"] = Category.objects.filter(is_active=True).order_by("name")
        context["tags"] = Tag.objects.all().order_by("name")

        # Get post index for navigation
        post_list = list(context["all_posts"])
        try:
            current_index = post_list.index(post)
            context["previous_post"] = (
                post_list[current_index - 1] if current_index > 0 else None
            )
            context["next_post"] = (
                post_list[current_index + 1]
                if current_index < len(post_list) - 1
                else None
            )
        except (ValueError, IndexError):
            context["previous_post"] = None
            context["next_post"] = None

        # Table of contents (simple implementation)
        context["table_of_contents"] = self.generate_table_of_contents(post.content)

        return context

    def generate_table_of_contents(self, content):
        """Generate a simple table of contents from headings in content"""
        import re

        headings = re.findall(r"<h([1-6])>(.*?)</h[1-6]>", content)
        toc = []
        for level, title in headings:
            toc.append(
                {
                    "level": int(level),
                    "title": title.strip(),
                    "anchor": title.strip()
                    .lower()
                    .replace(" ", "-")
                    .replace("?", "")
                    .replace("!", ""),
                }
            )
        return toc


class CategoryBlogListView(ListView):
    model = BlogPost
    template_name = "blog/category_posts.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        category_slug = self.kwargs.get("slug")
        self.category = get_object_or_404(Category, slug=category_slug, is_active=True)

        return (
            BlogPost.objects.filter(categories=self.category, status="published")
            .select_related("author")
            .prefetch_related("categories", "tags")
            .order_by("-published_at", "-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["category_posts_count"] = self.get_queryset().count()
        return context


class TagBlogListView(ListView):
    model = BlogPost
    template_name = "blog/tag_posts.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        tag_slug = self.kwargs.get("slug")
        self.tag = get_object_or_404(Tag, slug=tag_slug)

        return (
            BlogPost.objects.filter(tags=self.tag, status="published")
            .select_related("author")
            .prefetch_related("categories", "tags")
            .order_by("-published_at", "-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        context["tag_posts_count"] = self.get_queryset().count()
        return context


class CommentCreateView(CreateView):
    model = Comment
    fields = ["name", "email", "website", "content"]
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.post = get_object_or_404(
            BlogPost, slug=self.kwargs["slug"], status="published"
        )
        form.instance.ip_address = self.get_client_ip()
        form.instance.user_agent = self.request.META.get("HTTP_USER_AGENT", "")

        # Auto-approve comments (in production, you might want to moderate)
        form.instance.is_approved = True

        response = super().form_valid(form)

        # Update comment count on post
        form.instance.post.update_comment_count()

        messages.success(self.request, "Your comment has been submitted successfully!")
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip

    def get_success_url(self):
        return (
            reverse_lazy("blog:post_detail", kwargs={"slug": self.kwargs["slug"]})
            + "#comments"
        )
