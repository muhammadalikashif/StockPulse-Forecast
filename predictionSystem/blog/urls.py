from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<str:post_slug>/', views.blog_post_detail, name='blog-post-detail'),  # Remove the leading slash here
]
