from django.urls import path
from . import views

app_name = 'newsletters'

urlpatterns = [
    # Public URLs
    path('__subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/<uuid:token>/', views.unsubscribe, name='unsubscribe'),
    path('unsubscribe/feedback/<uuid:token>/',
         views.unsubscribe_feedback, name='unsubscribe_feedback'),

    # Tracking URLs
    path('track/open/<uuid:tracking_id>/', views.track_open, name='track_open'),
    path('track/click/<uuid:tracking_id>/',
         views.track_click, name='track_click'),

    # Admin URLs (require authentication)
    path('__newsletters/', views.newsletter_list, name='list'),
    path('__newsletter/create/', views.newsletter_create, name='create'),
    path('__newsletter/<int:pk>/', views.newsletter_detail, name='detail'),
    path('__newsletter/<int:pk>/edit/', views.newsletter_edit, name='edit'),
    path('__newsletter/<int:pk>/send/', views.newsletter_send, name='send'),
    path('__newsletter/<int:pk>/analytics/',
         views.newsletter_analytics, name='analytics'),

    # Subscriber management
    path('subscribers/', views.subscriber_list, name='subscriber_list'),
    path('subscribers/export/', views.export_subscribers,
         name='export_subscribers'),
    path('feedback/', views.feedback_list, name='feedback_list'),
]
