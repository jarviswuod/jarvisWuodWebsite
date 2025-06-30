from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

from django.db import models


class UserProfileManager(models.Manager):

    def get_or_create_for_user(self, user):
        profile, created = self.get_or_create(
            user=user,
            defaults={
                'phone': '',
                'bio': '',
            }
        )
        return profile, created

    def ensure_all_users_have_profiles(self):
        from django.db import transaction

        users_without_profiles = User.objects.filter(profile__isnull=True)
        profiles_to_create = []

        for user in users_without_profiles:
            profiles_to_create.append(self.model(user=user))

        if profiles_to_create:
            with transaction.atomic():
                self.bulk_create(profiles_to_create, ignore_conflicts=True)

        return len(profiles_to_create)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserProfileManager()

    @property
    def has_complete_profile(self):
        return bool(self.bio and self.avatar)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserEmailPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notify_on_blog_comments = models.BooleanField(default=True)
    notify_on_comment_replies = models.BooleanField(default=True)
    notify_on_thread_activity = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Email Preferences"


# Updated notification functions with user preferences
def send_blog_author_notification_with_preferences(comment, blog_url):
    """Notify blog author with preference check"""
    try:
        preferences, created = UserEmailPreferences.objects.get_or_create(
            user=comment.blog.author
        )

        if not preferences.notify_on_blog_comments:
            return

        # Rest of the notification code...
        send_blog_author_notification(comment, blog_url)

    except Exception as e:
        logger.error(f"Failed to send blog author notification: {str(e)}")


def send_reply_notification_with_preferences(comment, blog_url):
    """Notify parent comment author with preference check"""
    try:
        preferences, created = UserEmailPreferences.objects.get_or_create(
            user=comment.parent.author
        )

        if not preferences.notify_on_comment_replies:
            return

        # Rest of the notification code...
        send_reply_notification(comment, blog_url)

    except Exception as e:
        logger.error(f"Failed to send reply notification: {str(e)}")
