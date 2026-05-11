from django.views.generic import DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Profile, SocialLink
from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
    ProfileUpdateForm,
    SocialLinkForm,
)

User = get_user_model()


class ProfileDetailView(DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self):
        return User.objects.select_related("profile").prefetch_related(
            "profile__social_links", "profile__social_links__profile"
        )

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        # Get user's projects
        from portfolio.models import Project

        context["user_projects"] = Project.objects.filter(
            status="completed"
        ).prefetch_related("technologies", "categories", "tags")[:6]

        # Get user's blog posts
        from blog.models import BlogPost

        context["user_posts"] = BlogPost.objects.filter(
            author=user, status="published"
        ).prefetch_related("categories", "tags")[:6]

        return context


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create profile for new user
        Profile.objects.create(user=self.object)
        messages.success(self.request, "Account created successfully! Please log in.")
        return response


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("accounts:profile_update")
    success_message = "Profile updated successfully!"

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add user form for updating user info
        if self.request.POST:
            context["user_form"] = UserUpdateForm(
                self.request.POST, self.request.FILES, instance=self.request.user
            )
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        # Save profile form
        response = super().form_valid(form)

        # Handle user form
        user_form = UserUpdateForm(
            self.request.POST, self.request.FILES, instance=self.request.user
        )
        if user_form.is_valid():
            user_form.save()
            messages.success(self.request, "Account information updated successfully!")

        return response


class SocialLinkCreateView(LoginRequiredMixin, CreateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = "accounts/social_link_form.html"
    success_url = reverse_lazy("accounts:profile_update")

    def form_valid(self, form):
        # Get or create profile
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        form.instance.profile = profile
        messages.success(self.request, "Social link added successfully!")
        return super().form_valid(form)


class SocialLinkUpdateView(LoginRequiredMixin, UpdateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = "accounts/social_link_form.html"
    success_url = reverse_lazy("accounts:profile_update")

    def get_queryset(self):
        # Only allow users to edit their own social links
        return SocialLink.objects.filter(profile__user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Social link updated successfully!")
        return super().form_valid(form)
