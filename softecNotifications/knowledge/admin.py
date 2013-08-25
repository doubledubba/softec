from django.contrib import admin
from knowledge.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'description', 'category',
            'last_modified', 'public']
    list_filter = ['author']
    search_fields = ['title']
    date_hierarchy = 'date_added'


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'get_absolute_url']


admin.site.register(Article, ArticleAdmin)
