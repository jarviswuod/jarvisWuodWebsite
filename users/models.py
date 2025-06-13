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

    objects = UserProfileManager()

    @property
    def has_complete_profile(self):
        return bool(self.bio and self.avatar)

    def __str__(self):
        return f"{self.user.username}'s Profile"
