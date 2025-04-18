from django.urls import path
from .views import home, about, jobs, contact, blogs, services, mentorship, resume, software

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('jobs/', jobs, name="jobs"),
    path('contact/', contact, name="contact"),
    path('blogs/', blogs, name="blogs"),
    path('services/', services, name="services"),

    path('mentorship/', mentorship, name="mentorship"),
    path('resume/', resume, name="resume"),
    path('software/', software, name="software"),

]
