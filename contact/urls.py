from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    # Contact pages
    path('', views.ContactView.as_view(), name='contact'),
    path('success/', views.ContactSuccessView.as_view(), name='success'),
    
    # Newsletter
    path('newsletter/', views.NewsletterSubscribeView.as_view(), name='newsletter'),
    path('newsletter/success/', views.NewsletterSuccessView.as_view(), name='newsletter_success'),
    path('newsletter/unsubscribe/', views.NewsletterUnsubscribeView.as_view(), name='unsubscribe'),
    path('newsletter/unsubscribe/success/', views.NewsletterUnsubscribeSuccessView.as_view(), name='unsubscribe_success'),
    
    # Ajax contact
    path('ajax/', views.AjaxContactView.as_view(), name='ajax_contact'),
]
