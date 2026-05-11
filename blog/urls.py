from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog list and detail
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('post/<slug:slug>/', views.BlogDetailView.as_view(), name='post_detail'),
    
    # Category posts
    path('category/<slug:slug>/', views.CategoryBlogListView.as_view(), name='category_posts'),
    
    # Tag posts
    path('tag/<slug:slug>/', views.TagBlogListView.as_view(), name='tag_posts'),
    
    # Comment creation
    path('post/<slug:slug>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
]
