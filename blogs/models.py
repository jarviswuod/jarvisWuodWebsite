from django.db import models

# Create your models here.


class NewsletterSubscriber(models.Model):
    email_address = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email_address
