from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['home', 'pricing', 'about', 'blogs', 'contact']

    def location(self, item):
        return reverse(item)
