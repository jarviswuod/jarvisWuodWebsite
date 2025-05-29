# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/like/', views.toggle_like, name='toggle_like'),
    path('blog/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('blog/<slug:slug>/share/', views.share_blog, name='share_blog'),
]
