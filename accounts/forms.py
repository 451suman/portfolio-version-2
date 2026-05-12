from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Profile, SocialLink

User = get_user_model()


class CustomUserCreationForm(BaseUserCreationForm):
    """Custom user registration form"""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Please enter a valid email address.')
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with that email already exists.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'bio', 'location', 'birth_date', 
                 'website', 'github_username', 'linkedin_url', 'twitter_username', 
                 'is_available', 'avatar')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_github_username(self):
        username = self.cleaned_data.get('github_username')
        if username:
            # Basic validation for GitHub username
            if not username.replace('-', '').replace('_', '').isalnum():
                raise forms.ValidationError('GitHub username can only contain letters, numbers, hyphens, and underscores.')
        return username
    
    def clean_twitter_username(self):
        username = self.cleaned_data.get('twitter_username')
        if username:
            # Basic validation for Twitter username
            if not username.replace('-', '').replace('_', '').isalnum():
                raise forms.ValidationError('Twitter username can only contain letters, numbers, hyphens, and underscores.')
        return username


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating profile information"""
    
    class Meta:
        model = Profile
        fields = ('title', 'profession_titles', 'phone', 'experience_years', 
                 'hourly_rate', 'preferred_work_type', 'skills_summary', 
                 'about_short', 'about_detailed', 'resume_file')
        widgets = {
            'profession_titles': forms.Textarea(attrs={'rows': 3, 'help_text': 'Enter titles separated by commas'}),
            'skills_summary': forms.Textarea(attrs={'rows': 4}),
            'about_short': forms.TextInput(attrs={'maxlength': 200}),
            'about_detailed': forms.Textarea(attrs={'rows': 6}),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Basic phone validation
            phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not phone.isdigit() or len(phone) < 10:
                raise forms.ValidationError('Please enter a valid phone number.')
        return phone
    
    def clean_profession_titles(self):
        titles = self.cleaned_data.get('profession_titles')
        if titles:
            # Convert to list for JSONField
            titles_list = [title.strip() for title in titles.split(',') if title.strip()]
            return titles_list
        return []


class SocialLinkForm(forms.ModelForm):
    """Form for social media links"""
    
    class Meta:
        model = SocialLink
        fields = ['platform', 'url', 'icon_class', 'is_active', 'order']
    
    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url and not url.startswith(('http://', 'https://')):
            raise forms.ValidationError('URL must start with http:// or https://')
        return url
    
    def clean_platform(self):
        platform = self.cleaned_data.get('platform')
        if platform:
            return platform.strip().title()
        return platform


class SocialLinkFormSet(forms.ModelForm):
    """Formset for managing multiple social links"""
    
    class Meta:
        model = SocialLink
        fields = ['platform', 'url', 'icon_class', 'is_active', 'order']
        extra = 1
        can_delete = True
