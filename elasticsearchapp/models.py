# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Blog(models.Model):
    subdomain = models.CharField(max_length=16)
    name = models.CharField(max_length=32)

    def __str__(self):
        return 'Blog: {}-{}'.format(self.subdomain, self.name).encode('utf-8')


# Blogpost to be indexed based on blog into ElasticSearch
class BlogPost(models.Model):
    blog = models.ForeignKey(Blog)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost')
    posted_date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return 'Post: {}'.format(self.title).encode('utf-8')

    def indexing(self):
        from .search import BlogPostIndex

        obj = BlogPostIndex(
            meta={
                'id': self.id
            },
            author=self.author.username,
            posted_date=self.posted_date,
            title=self.title,
            text=self.text
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    @classmethod
    def post_save(cls, sender, instance, **kwargs):
        instance.indexing()


models.signals.post_save.connect(BlogPost.post_save, sender=BlogPost)
