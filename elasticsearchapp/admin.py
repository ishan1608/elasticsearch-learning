# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import BlogPost

# Need to register my BlogPost so it shows up in the admin
admin.site.register(BlogPost)
