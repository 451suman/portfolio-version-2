from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q, Count, Sum
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.paginator import Paginator

from accounts.models import Profile, SocialLink
from portfolio.models import Project, Skill, Experience
from blog.models import BlogPost, Category, Tag
from contact.models import ContactMessage, NewsletterSubscription


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get profile data
        try:
            profile = Profile.objects.select_related("user").first()
            breakpoint()
            if profile:
                context["profile"] = profile
                context["social_links"] = profile.social_links.filter(
                    is_active=True
                ).order_by("order")
        except:
            pass

        # Featured projects with optimized queries
        context["featured_projects"] = Project.objects.filter(
            is_featured=True, status="completed"
        ).prefetch_related("technologies", "images")[:6]

        # Latest projects
        context["latest_projects"] = Project.objects.filter(
            status="completed"
        ).prefetch_related("technologies")[:3]

        # Featured skills
        context["featured_skills"] = Skill.objects.filter(is_featured=True).order_by(
            "order", "name"
        )[:8]

        # All skills for tech stack section
        context["all_skills"] = Skill.objects.all().order_by(
            "-is_featured", "order", "name"
        )

        # Experience timeline
        context["experiences"] = Experience.objects.prefetch_related(
            "technologies"
        ).order_by("-is_current", "-start_date")

        # Featured blog posts
        context["featured_posts"] = (
            BlogPost.objects.filter(status="published", is_featured=True)
            .select_related("author")
            .prefetch_related("categories", "tags")[:3]
        )

        # Recent blog posts
        context["recent_posts"] = (
            BlogPost.objects.filter(status="published")
            .select_related("author")
            .prefetch_related("categories", "tags")[:6]
        )

        # Project statistics
        context["project_stats"] = {
            "total_projects": Project.objects.filter(status="completed").count(),
            "featured_projects": Project.objects.filter(
                is_featured=True, status="completed"
            ).count(),
            "total_skills": Skill.objects.count(),
        }

        # Blog statistics
        context["blog_stats"] = {
            "total_posts": BlogPost.objects.filter(status="published").count(),
            "total_comments": BlogPost.objects.filter(status="published").aggregate(
                total=Count("comments", filter=Q(comments__is_approved=True))
            )["total"]
            or 0,
            "total_views": BlogPost.objects.filter(status="published").aggregate(
                total=Sum("view_count")
            )["total"]
            or 0,
        }

        return context


class AboutView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get profile data
        try:
            profile = Profile.objects.select_related("user").first()
            if profile:
                context["profile"] = profile
                context["social_links"] = profile.social_links.filter(
                    is_active=True
                ).order_by("order")
        except:
            pass

        # All skills with progress bars
        context["skills"] = Skill.objects.all().order_by(
            "-is_featured", "order", "name"
        )

        # Experience timeline
        context["experiences"] = Experience.objects.prefetch_related(
            "technologies"
        ).order_by("-is_current", "-start_date")

        # Skills by level
        context["expert_skills"] = Skill.objects.all().order_by(
            "order", "name"
        )
        context["advanced_skills"] = Skill.objects.filter(level="advanced").order_by(
            "order", "name"
        )
        context["intermediate_skills"] = Skill.objects.filter(
            level="intermediate"
        ).order_by("order", "name")
        context["beginner_skills"] = Skill.objects.filter(level="beginner").order_by(
            "order", "name"
        )

        return context


class SearchView(TemplateView):
    template_name = "core/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "")

        if query:
            # Search projects
            projects = (
                Project.objects.filter(
                    Q(title__icontains=query)
                    | Q(description__icontains=query)
                    | Q(short_description__icontains=query)
                    | Q(technologies__name__icontains=query)
                )
                .distinct()
                .prefetch_related("technologies")
            )

            # Search blog posts
            blog_posts = (
                BlogPost.objects.filter(
                    Q(title__icontains=query)
                    | Q(content__icontains=query)
                    | Q(excerpt__icontains=query)
                )
                .distinct()
                .filter(status="published")
                .select_related("author")
                .prefetch_related("categories", "tags")
            )

            context.update(
                {
                    "query": query,
                    "projects": projects,
                    "blog_posts": blog_posts,
                    "projects_count": projects.count(),
                    "blog_posts_count": blog_posts.count(),
                    "total_results": projects.count() + blog_posts.count(),
                }
            )
        else:
            context.update(
                {
                    "query": "",
                    "projects": Project.objects.none(),
                    "blog_posts": BlogPost.objects.none(),
                    "projects_count": 0,
                    "blog_posts_count": 0,
                    "total_results": 0,
                }
            )

        return context


class Error404View(TemplateView):
    template_name = "core/404.html"

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("status", 404)
        return super().render_to_response(context, **response_kwargs)


class Error500View(TemplateView):
    template_name = "core/500.html"

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("status", 500)
        return super().render_to_response(context, **response_kwargs)
