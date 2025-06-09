from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Newsletter, Subscriber, EmailSent, EmailOpen, LinkClick, UnsubscribeFeedback


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created_by',
                    'created_at', 'is_sent', 'sent_at']
    list_filter = ['is_sent', 'created_at', 'sent_at']
    search_fields = ['title', 'subject']
    readonly_fields = ['created_at', 'sent_at']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_sent:
            return self.readonly_fields + ['title', 'subject', 'content', 'html_content']
        return self.readonly_fields


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'get_full_name', 'is_active', 'date_subscribed']
    list_filter = ['is_active', 'date_subscribed']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['date_subscribed', 'unsubscribe_token']

    def get_full_name(self, obj):
        return obj.get_full_name() or '-'
    get_full_name.short_description = 'Name'


@admin.register(EmailSent)
class EmailSentAdmin(admin.ModelAdmin):
    list_display = ['newsletter', 'subscriber',
                    'sent_at', 'is_opened', 'open_count']
    list_filter = ['is_opened', 'sent_at', 'newsletter']
    search_fields = ['subscriber__email', 'newsletter__title']
    readonly_fields = ['tracking_id', 'sent_at']


@admin.register(EmailOpen)
class EmailOpenAdmin(admin.ModelAdmin):
    list_display = ['get_newsletter',
                    'get_subscriber', 'opened_at', 'ip_address']
    list_filter = ['opened_at']
    search_fields = ['email_sent__subscriber__email',
                     'email_sent__newsletter__title']
    readonly_fields = ['opened_at']

    def get_newsletter(self, obj):
        return obj.email_sent.newsletter.title
    get_newsletter.short_description = 'Newsletter'

    def get_subscriber(self, obj):
        return obj.email_sent.subscriber.email
    get_subscriber.short_description = 'Subscriber'


@admin.register(UnsubscribeFeedback)
class UnsubscribeFeedbackAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'primary_reason',
                    'would_resubscribe', 'created_at']
    list_filter = ['primary_reason', 'would_resubscribe', 'created_at']
    search_fields = ['subscriber__email']
    readonly_fields = ['created_at']

    def get_newsletter(self, obj):
        return obj.email_sent.newsletter.title
    get_newsletter.short_description = 'Newsletter'

    def get_subscriber(self, obj):
        return obj.email_sent.subscriber.email
    get_subscriber.short_description = 'Subscriber'


@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    list_display = ['get_newsletter', 'get_subscriber', 'url', 'clicked_at']
    list_filter = ['clicked_at']
    search_fields = ['email_sent__subscriber__email', 'url']
    readonly_fields = ['clicked_at']

    def get_newsletter(self, obj):
        return obj.email_sent.newsletter.title if obj.email_sent and obj.email_sent.newsletter else "N/A"
    get_newsletter.short_description = 'Newsletter'

    def get_subscriber(self, obj):
        return obj.email_sent.subscriber.email if obj.email_sent and obj.email_sent.subscriber else "N/A"
    get_subscriber.short_description = 'Subscriber'
