from django.urls import path
from .views import home, about, pricing, contact, view_log_file


urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('pricing/', pricing, name="pricing"),
    path('logs/<str:filename>/', view_log_file, name='view_log_file'),
]
