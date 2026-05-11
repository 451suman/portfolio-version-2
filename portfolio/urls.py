from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Project list and detail
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('project/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    
    # Category projects
    path('category/<slug:slug>/', views.CategoryProjectListView.as_view(), name='category_projects'),
    
    # Skill projects
    path('skill/<slug:slug>/', views.SkillProjectListView.as_view(), name='skill_projects'),
    
    # Tag projects
    path('tag/<slug:slug>/', views.TagProjectListView.as_view(), name='tag_projects'),
]
