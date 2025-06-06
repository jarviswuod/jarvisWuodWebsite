from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.


class NewsletterSubscriber(models.Model):
    email_address = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email_address


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    content = CKEditor5Field(config_name='extends', null=True)
    excerpt = models.TextField(max_length=300, blank=True)
    featured_image = models.ImageField(
        upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.filter(is_active=True).count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f'{self.user.username} likes {self.blog.title}'


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog.title}'

    def get_replies(self):
        return self.replies.filter(is_active=True)


class Share(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('copy_link', 'Copy Link'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='shares')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} shared {self.blog.title} on {self.platform}'
