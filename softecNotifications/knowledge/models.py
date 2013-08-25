from urllib import quote

from django.db import models
from django import forms
from django.contrib.auth.models import User

from softecNotifications.settings import DOMAIN, MEDIA_URL
from knowledge.choices import categories

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User)
    description = models.CharField(max_length=80, blank=True)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False)
    category = models.CharField(max_length=255, choices=categories)
    keywords = models.CharField(max_length=80, help_text='Separate each keyword with one space')
    views = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        description = self.title or self.description
        return '<Article: %s>' % description

    def get_absolute_url(self):
        try:
            Article.objects.get(title=self.title)
            slug = self.title
        except Article.MultipleObjectsReturned:
            slug = self.pk

        return DOMAIN + '/knowledge/%s' % quote(str(slug))


