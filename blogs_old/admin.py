from django.contrib import admin

from .models import NewsletterSubscriber


class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'subscribed_at', 'is_active')
    search_fields = ('email_address',)
    list_filter = ('is_active',)
    ordering = ('-subscribed_at',)


admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
