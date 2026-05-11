from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Project, Skill, ProjectImage


class ProjectListView(ListView):
    model = Project
    template_name = "portfolio/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Project.objects.filter(status="completed")
            .prefetch_related("technologies", "images")
            .order_by("-is_featured", "-created_at")
        )

        # Search functionality
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(short_description__icontains=search_query)
                | Q(technologies__name__icontains=search_query)
            ).distinct()

        # Skill filter
        skill_slug = self.request.GET.get("skill", "")
        if skill_slug:
            queryset = queryset.filter(technologies__slug=skill_slug)

        # Status filter
        status = self.request.GET.get("status", "")
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get skills for sidebar
        context["skills"] = Skill.objects.all().order_by(
            "-is_featured", "order", "name"
        )
        # Get current filters
        context["current_skill"] = self.request.GET.get("skill", "")
        context["current_status"] = self.request.GET.get("status", "")
        context["search_query"] = self.request.GET.get("search", "")

        # Featured projects
        context["featured_projects"] = Project.objects.filter(
            is_featured=True, status="completed"
        )[:3]

        # Project statistics
        context["project_stats"] = {
            "total_projects": Project.objects.filter(status="completed").count(),
            "featured_projects": Project.objects.filter(
                is_featured=True, status="completed"
            ).count(),
            "in_progress": Project.objects.filter(status="in_progress").count(),
        }

        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "portfolio/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.prefetch_related(
            "technologies", "categories", "tags", "images"
        )

    def get_object(self):
        slug = self.kwargs.get("slug")
        project = get_object_or_404(Project, slug=slug)

        # Increase view count
        project.increase_view_count()

        return project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        # Get project images
        context["project_images"] = project.images.all().order_by("order")

        # Get related projects
        context["related_projects"] = (
            Project.objects.filter(technologies__in=project.technologies.all())
            .exclude(id=project.id)
            .distinct()[:3]
        )

        # Get all projects for navigation
        context["all_projects"] = Project.objects.filter(status="completed").order_by(
            "-created_at"
        )

        # Get project index for navigation
        project_list = list(context["all_projects"])
        try:
            current_index = project_list.index(project)
            context["previous_project"] = (
                project_list[current_index - 1] if current_index > 0 else None
            )
            context["next_project"] = (
                project_list[current_index + 1]
                if current_index < len(project_list) - 1
                else None
            )
        except (ValueError, IndexError):
            context["previous_project"] = None
            context["next_project"] = None

        return context


class CategoryProjectListView(ListView):
    model = Project
    template_name = "portfolio/category_projects.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        category_slug = self.kwargs.get("slug")
        self.category = get_object_or_404(Category, slug=category_slug, is_active=True)

        return (
            Project.objects.filter(categories=self.category, status="completed")
            .prefetch_related("technologies", "categories", "tags")
            .order_by("-is_featured", "-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["category_projects_count"] = self.get_queryset().count()
        return context


class SkillProjectListView(ListView):
    model = Project
    template_name = "portfolio/skill_projects.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        skill_slug = self.kwargs.get("slug")
        self.skill = get_object_or_404(Skill, slug=skill_slug)

        return (
            Project.objects.filter(technologies=self.skill, status="completed")
            .prefetch_related("technologies", "categories", "tags")
            .order_by("-is_featured", "-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skill"] = self.skill
        context["skill_projects_count"] = self.get_queryset().count()
        return context


class TagProjectListView(ListView):
    model = Project
    template_name = "portfolio/tag_projects.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        tag_slug = self.kwargs.get("slug")
        self.tag = get_object_or_404(Tag, slug=tag_slug)

        return (
            Project.objects.filter(tags=self.tag, status="completed")
            .prefetch_related("technologies", "categories", "tags")
            .order_by("-is_featured", "-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        context["tag_projects_count"] = self.get_queryset().count()
        return context
