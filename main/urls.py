from django.urls import path
from .views import home, about, pricing, contact


urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('pricing/', pricing, name="pricing"),

]
