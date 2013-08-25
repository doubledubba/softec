from knowledge.models import Article

from django.contrib.sitemaps import Sitemap

class Knowledge_Map(Sitemap):
    def items(self):
        return Article.objects.filter(public=True)

    def lastmod(self, obj):
        return obj.last_modified
