# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import BlogPost, Blog, BlogPage


admin.site.register(BlogPost)
admin.site.register(BlogPage)
admin.site.register(Blog)
