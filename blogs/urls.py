from django.urls import path
from .views import blogs, newsletter_subscription, newsletter_success

urlpatterns = [
    path('blogs/', blogs, name="blogs"),
    path('newsletter/', newsletter_subscription,
         name='newsletter_subscription'),
    path('newsletter/success/', newsletter_success, name='newsletter_success'),

]
