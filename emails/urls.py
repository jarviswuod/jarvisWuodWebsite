
from django.urls import path
from . import views

app_name = 'emails'

urlpatterns = [
    path('send-single/<slug:slug>/', views.send_single_email, name='send_single'),
    path('send-bulk/<slug:slug>/', views.send_bulk_email, name='send_bulk'),
]
