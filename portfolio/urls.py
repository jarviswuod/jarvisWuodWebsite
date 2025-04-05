from django.urls import path
from .views import home, about, jobs, contact, blogs, services, mentorship, resume_review, web_dev

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('jobs/', jobs, name="jobs"),
    path('contact/', contact, name="contact"),
    path('blogs/', blogs, name="blogs"),
    path('services/', services, name="services"),

    path('mentorship/', mentorship, name="mentorship"),
    path('resume_review/', resume_review, name="resume_review"),
    path('web_dev/', web_dev, name="web_dev"),

]
