from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Error pages
    path('404/', views.Error404View.as_view(), name='404'),
    path('500/', views.Error500View.as_view(), name='500'),
]
