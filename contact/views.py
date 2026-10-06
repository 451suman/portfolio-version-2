from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import ContactForm, NewsletterForm
from .models import ContactMessage, EmailTemplate, NewsletterSubscription


class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = "contact/contact.html"
    success_url = reverse_lazy("contact:contact")

    def form_valid(self, form):
        # Set additional fields
        form.instance.ip_address = self.get_client_ip()
        form.instance.user_agent = self.request.META.get("HTTP_USER_AGENT", "")

        # Save the form
        response = super().form_valid(form)

        # Send notification email (in production)
        try:
            self.send_notification_email(form.instance)
        except Exception:
            # Log error but don't fail the form submission
            pass

        messages.success(
            self.request,
            "Your message has been sent successfully! We'll get back to you soon.",
        )
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip

    def send_notification_email(self, contact_message):
        """Send email notification to admin about new contact message"""
        subject = f"New Contact Message: {contact_message.subject}"
        message = f"""
        Name: {contact_message.name}
        Email: {contact_message.email}
        Phone: {contact_message.phone}
        Company: {contact_message.company}
        Inquiry Type: {contact_message.get_inquiry_type_display()}
        Subject: {contact_message.subject}
        
        Message:
        {contact_message.message}
        
        Budget: {contact_message.budget or "Not specified"}
        Timeline: {contact_message.timeline or "Not specified"}
        Urgent: {contact_message.is_urgent}
        Referral: {contact_message.referral_source or "Not specified"}
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )


class NewsletterSubscribeView(FormView):
    form_class = NewsletterForm
    template_name = "contact/newsletter_subscribe.html"
    success_url = reverse_lazy("contact:newsletter_success")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        first_name = form.cleaned_data.get("first_name", "")
        last_name = form.cleaned_data.get("last_name", "")
        
        # Check if already subscribed
        if NewsletterSubscription.objects.filter(email=email).exists():
            subscription = NewsletterSubscription.objects.get(email=email)
            if not subscription.is_active:
                subscription.is_active = True
                subscription.unsubscribe_date = None
                subscription.unsubscribe_reason = ""
                subscription.save()
                messages.info(
                    self.request, "You have been re-subscribed to our newsletter!"
                )
            else:
                messages.info(
                    self.request, "You are already subscribed to our newsletter!"
                )
        else:
            # Create new subscription
            subscription = NewsletterSubscription.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                ip_address=self.get_client_ip(),
                referral_source=self.request.GET.get("ref", ""),
            )

            # Send welcome email (in production)
            try:
                self.send_welcome_email(subscription)
            except Exception:
                # Log error but don't fail the subscription
                pass

            messages.success(
                self.request, "Thank you for subscribing to our newsletter!"
            )

        return super().form_valid(form)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip

    def send_welcome_email(self, subscription):
        """Send welcome email to new subscriber"""
        try:
            template = EmailTemplate.objects.get(
                template_type="newsletter_welcome", is_active=True
            )
        except EmailTemplate.DoesNotExist:
            # Use default template
            subject = "Welcome to Our Newsletter!"
            message = f"""
            Hi {subscription.first_name or "there"},
            
            Thank you for subscribing to our newsletter! We're excited to have you join our community.
            
            You'll receive updates about:
            - Latest projects and case studies
            - Tech tutorials and tips
            - Industry news and insights
            - Special offers and announcements
            
            If you ever want to unsubscribe, you can do so by clicking the unsubscribe link in any of our emails.
            
            Best regards,
            The Team
            """
        else:
            subject = template.subject
            message = template.html_content

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [subscription.email],
            fail_silently=True,
        )


class NewsletterSuccessView(TemplateView):
    template_name = "contact/newsletter_success.html"


class NewsletterUnsubscribeView(TemplateView):
    template_name = "contact/unsubscribe.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", "")
        reason = request.POST.get("reason", "")

        try:
            subscription = NewsletterSubscription.objects.get(email=email)
            subscription.unsubscribe(reason)
            messages.success(
                request, "You have been successfully unsubscribed from our newsletter."
            )
        except NewsletterSubscription.DoesNotExist:
            messages.error(request, "Email not found in our subscription list.")

        return redirect("contact:unsubscribe_success")


class NewsletterUnsubscribeSuccessView(TemplateView):
    template_name = "contact/unsubscribe_success.html"


class AjaxContactView(CreateView):
    """Ajax contact form for dynamic submission"""

    model = ContactMessage
    form_class = ContactForm

    def form_invalid(self, form):
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    def form_valid(self, form):
        form.instance.ip_address = self.get_client_ip()
        form.instance.user_agent = self.request.META.get("HTTP_USER_AGENT", "")

        # Save the form
        self.object = form.save()

        # Send notification email (in production)
        try:
            self.send_notification_email(self.object)
        except Exception:
            # Log error but don't fail the form submission
            pass

        return JsonResponse(
            {"success": True, "message": "Your message has been sent successfully!"}
        )

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip

    def send_notification_email(self, contact_message):
        """Send email notification to admin about new contact message"""
        subject = f"New Contact Message: {contact_message.subject}"
        message = f"""
        Name: {contact_message.name}
        Email: {contact_message.email}
        Subject: {contact_message.subject}
        
        Message:
        {contact_message.message}
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )
