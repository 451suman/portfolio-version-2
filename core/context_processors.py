from django.conf import settings
from accounts.models import Profile, SocialLink
from portfolio.models import Project, Skill
from blog.models import BlogPost, Category, Tag


def site_settings(request):
    """
    Global context processor for site-wide settings and data
    """
    context = {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Developer Portfolio"),
        "SITE_DESCRIPTION": getattr(
            settings, "SITE_DESCRIPTION", "Professional Django Developer Portfolio"
        ),
        "SITE_AUTHOR": getattr(settings, "SITE_AUTHOR", "John Doe"),
        "SITE_EMAIL": getattr(settings, "SITE_EMAIL", "contact@example.com"),
        "SITE_PHONE": getattr(settings, "SITE_PHONE", "+1234567890"),
        "SITE_ADDRESS": getattr(settings, "SITE_ADDRESS", "San Francisco, CA"),
        "GITHUB_USERNAME": getattr(settings, "GITHUB_USERNAME", "johndoe"),
        "LINKEDIN_URL": getattr(
            settings, "LINKEDIN_URL", "https://linkedin.com/in/johndoe"
        ),
        "TWITTER_USERNAME": getattr(settings, "TWITTER_USERNAME", "johndoe"),
    }

    # Get profile data if available
    try:
        profile = Profile.objects.select_related("user").first()
        if profile:
            context.update(
                {
                    "profile": profile,
                    "social_links": profile.social_links.filter(
                        is_active=True
                    ).order_by("order"),
                }
            )
    except:
        pass

    # Get featured projects
    context["featured_projects"] = Project.objects.filter(
        is_featured=True, status="completed"
    ).prefetch_related("technologies", "images")[:6]

    # Get featured skills
    context["featured_skills"] = Skill.objects.filter(is_featured=True).order_by(
        "order"
    )[:8]

    # Get recent blog posts
    context["recent_posts"] = (
        BlogPost.objects.filter(status="published")
        .select_related("author")
        .prefetch_related("categories", "tags")[:3]
    )

    # Get all skills for navigation
    context["nav_skills"] = Skill.objects.filter(is_featured=True).order_by("order")

    return context
