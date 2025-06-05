from django.urls import path
from .views import newsletter_subscription, newsletter_success, blogs, blog_detail, toggle_like, add_comment, share_blog

urlpatterns = [
    path('newsletter/', newsletter_subscription,
         name='newsletter_subscription'),
    path('newsletter/success/', newsletter_success, name='newsletter_success'),

    path('blogs/', blogs, name='blogs'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/like/', toggle_like, name='toggle_like'),
    path('blog/<slug:slug>/comment/', add_comment, name='add_comment'),
    path('blog/<slug:slug>/share/', share_blog, name='share_blog'),

]
