from django.contrib import admin
from .models import UserProfile, UserEmailPreferences


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'phone')


@admin.register(UserEmailPreferences)
class UserEmailPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'notify_on_blog_comments',
                    'notify_on_comment_replies', 'notify_on_thread_activity')
    list_filter = ('notify_on_blog_comments',
                   'notify_on_comment_replies', 'notify_on_thread_activity')
    search_fields = ('user__username', 'user__email')
