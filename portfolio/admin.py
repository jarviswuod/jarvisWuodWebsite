from django.contrib import admin

# Register your models here.
from .models import (
    BookCall,
    MentorshipContact,
    ExpertiseContact,
    ResumeReviewContact,
)


class BookCallAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email_address',
        'phone_number',
        'booking_reason',
        'submitted_at'
    )
    search_fields = ('full_name', 'email_address')
    list_filter = ('submitted_at',)
    ordering = ('-submitted_at',)


class MentorshipContactAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email_address',
        'phone_number',
        'start_coding',
        'goal',
        'obstacle',
        'progress_details',
        'submitted_at'
    )
    search_fields = ('full_name', 'email_address')
    list_filter = ('submitted_at',)
    ordering = ('-submitted_at',)


class ExpertiseContactAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email_address',
        'phone_number',
        'service_type',
        'project_link',
        'project_details',
        'submitted_at'
    )
    search_fields = ('full_name', 'email_address')
    list_filter = ('submitted_at',)
    ordering = ('-submitted_at',)


class ResumeReviewContactAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email_address',
        'phone_number',
        'resume_frequency',
        'resume_reviewed_before',
        'uploaded_resume',
        'linkedin_profile',
        'portfolio_links',
        'submitted_at'
    )
    search_fields = ('full_name', 'email_address')
    list_filter = ('submitted_at',)
    ordering = ('-submitted_at',)


admin.site.register(BookCall, BookCallAdmin)
admin.site.register(MentorshipContact, MentorshipContactAdmin)
admin.site.register(ExpertiseContact, ExpertiseContactAdmin)
admin.site.register(ResumeReviewContact, ResumeReviewContactAdmin)
