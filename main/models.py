from django.db import models

# Create your models here.


class BookCall(models.Model):
    full_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True, null=True)


# class MentorshipContact(models.Model):
#     full_name = models.CharField(max_length=100)
#     email_address = models.EmailField()
#     phone_number = models.CharField(max_length=20, blank=True)
#     start_coding = models.CharField(max_length=50, blank=True)
#     goal = models.CharField(max_length=255, blank=True)
#     obstacle = models.CharField(max_length=255, blank=True)
#     progress_details = models.TextField(blank=True)

#     submitted_at = models.DateTimeField(auto_now_add=True)


# class ExpertiseContact(models.Model):
#     full_name = models.CharField(max_length=100)
#     email_address = models.EmailField()
#     phone_number = models.CharField(max_length=20, blank=True)
#     service_type = models.CharField(max_length=50, blank=True)
#     project_link = models.URLField(blank=True)
#     project_details = models.TextField(blank=True)

#     submitted_at = models.DateTimeField(auto_now_add=True)


# class ResumeReviewContact(models.Model):
#     full_name = models.CharField(max_length=100)
#     email_address = models.EmailField()
#     phone_number = models.CharField(max_length=20, blank=True)
#     resume_frequency = models.CharField(max_length=50, blank=True)
#     resume_reviewed_before = models.CharField(max_length=10, blank=True)
#     uploaded_resume = models.FileField(upload_to='resumes/', blank=True)
#     linkedin_profile = models.URLField(blank=True)
#     portfolio_links = models.URLField(blank=True)
#     job_hunting_experience = models.TextField(blank=True)

#     submitted_at = models.DateTimeField(auto_now_add=True)


# class NewsletterSubscriber(models.Model):
#     email_address = models.EmailField(unique=True)
#     subscribed_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.email_address
