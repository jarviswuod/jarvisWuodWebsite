from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['home', 'pricing', 'about', 'blogs', 'contact', 'newsletter_subscription', 'newsletter_success']

    def location(self, item):
        return reverse(item)
