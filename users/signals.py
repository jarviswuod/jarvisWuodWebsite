from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        try:
            UserProfile.objects.create(user=instance)
            logger.info(f"Profile created for new user: {instance.username}")
        except Exception as e:
            logger.error(
                f"Failed to create profile for {instance.username}: {e}")
    else:
        try:
            profile = instance.profile
            profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)
            logger.info(
                f"Profile created for existing user: {instance.username}")
        except Exception as e:
            logger.error(
                f"Error handling profile for {instance.username}: {e}")
