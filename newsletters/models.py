from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from django.utils import timezone


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    content = models.TextField()
    html_content = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('newsletter:detail', kwargs={'pk': self.pk})


class EmailSent(models.Model):
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.CASCADE, related_name='emails_sent')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    tracking_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    is_opened = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True)
    open_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['newsletter', 'subscriber']

    def __str__(self):
        return f"{self.newsletter.title} -> {self.subscriber.email}"


class EmailOpen(models.Model):
    email_sent = models.ForeignKey(
        EmailSent, on_delete=models.CASCADE, related_name='opens')
    opened_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    def __str__(self):
        return f"Open: {self.email_sent.newsletter.title} by {self.email_sent.subscriber.email}"


class LinkClick(models.Model):
    email_sent = models.ForeignKey(
        EmailSent, on_delete=models.CASCADE, related_name='link_clicks')
    url = models.URLField()
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    def __str__(self):
        return f"Click: {self.url} from {self.email_sent.newsletter.title}"


class UnsubscribeFeedback(models.Model):
    FEEDBACK_CHOICES = [
        ('too_frequent', 'Emails too frequent'),
        ('not_relevant', 'Content not relevant'),
        ('poor_quality', 'Poor content quality'),
        ('never_signed_up', 'Never signed up'),
        ('technical_issues', 'Technical issues'),
        ('other', 'Other'),
    ]

    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    primary_reason = models.CharField(max_length=20, choices=FEEDBACK_CHOICES)
    additional_feedback = models.TextField(blank=True)
    would_resubscribe = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.subscriber.email}"
