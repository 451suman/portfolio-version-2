from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import ContactMessage, NewsletterSubscription


class ContactForm(forms.ModelForm):
    """Contact form for getting in touch"""
    
    class Meta:
        model = ContactMessage
        fields = [
            'name', 'email', 'phone', 'company', 'inquiry_type',
            'subject', 'message', 'budget', 'timeline', 'is_urgent', 'referral_source'
        ]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        return message
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        return name.strip()


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    
    class Meta:
        model = NewsletterSubscription
        fields = ['email', 'first_name', 'last_name']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Please enter a valid email address.')
        return email.lower()
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            return first_name.strip().title()
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            return last_name.strip().title()
        return last_name


class QuickContactForm(forms.Form):
    """Quick contact form for homepage and sidebar"""
    
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        return message.strip()


class UnsubscribeForm(forms.Form):
    """Newsletter unsubscribe form"""
    
    email = forms.EmailField()
    reason = forms.CharField(required=False, widget=forms.Textarea)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Please enter a valid email address.')
        return email.lower()


class ProjectInquiryForm(forms.ModelForm):
    """Specific form for project inquiries"""
    
    class Meta:
        model = ContactMessage
        fields = [
            'name', 'email', 'phone', 'company', 'subject', 
            'message', 'budget', 'timeline', 'is_urgent'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inquiry_type'].initial = 'project'
        self.fields['inquiry_type'].widget = forms.HiddenInput()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 20:
            raise forms.ValidationError('Project description must be at least 20 characters long.')
        return message.strip()
