from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['home', 'about', 'blogs', 'services', 'mentorship', 'resume', 'software']

    def location(self, item):
        return reverse(item)
