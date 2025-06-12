from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    @property
    def has_complete_profile(self):
        return bool(self.bio and self.avatar)

    def __str__(self):
        return f"{self.user.username}'s Profile"
