# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Blog(models.Model):
    blog_title = models.CharField(max_length=200, default="null")
    blog_index = models.CharField(max_length=200, default="null")
    blog_author = models.CharField(max_length=200, default="null")
    blog_pub_date = models.DateTimeField('date published')
    blog_content = models.CharField(max_length=1000, default="null")

    def __str__(self):
        return self.blog_title
