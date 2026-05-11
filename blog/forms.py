from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for blog post comments"""
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'content']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        return name.strip()
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 5:
            raise forms.ValidationError('Comment must be at least 5 characters long.')
        return content.strip()


class CommentReplyForm(forms.ModelForm):
    """Form for replying to comments"""
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add parent field for replies (will be set in view)
        self.parent = kwargs.get('parent', None)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        return name.strip()
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 5:
            raise forms.ValidationError('Reply must be at least 5 characters long.')
        return content.strip()
