
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blogs.models import Blog


class StaticViewSitemap(Sitemap):
    def items(self):
        static_pages = ['home', 'pricing', 'about', 'blogs',
                        'contact', 'newsletter_subscription', 'newsletter_success']
        published_blogs = list(Blog.objects.filter(is_published=True))

        return static_pages + published_blogs

    def location(self, item):
        if isinstance(item, str):
            return reverse(item)
        else:
            return item.get_absolute_url()

    def lastmod(self, item):
        if hasattr(item, 'updated_at'):
            return item.updated_at
        return None

    def changefreq(self, item):
        if isinstance(item, str):
            return 'weekly'
        else:
            return 'weekly'

    def priority(self, item):
        if isinstance(item, str):
            priorities = {
                'home': 1.0,
                'blogs': 0.9,
                'pricing': 0.8,
                'about': 0.7,
                'contact': 0.6,
                'newsletter_subscription': 0.5,
                'newsletter_success': 0.3
            }
            return priorities.get(item, 0.8)
        else:
            return 0.7
