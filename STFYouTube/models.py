# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Video(models.Model):
    video_id = models.CharField(max_length=200, default="null")
    video_title = models.CharField(max_length=200, default="null")
    video_link = models.CharField(max_length=200, default="null")
    video_author = models.CharField(max_length=200, default="null")
    video_duration = models.CharField(max_length=200, default="null")
    video_author_link = models.CharField(max_length=200, default="null")
    video_view = models.CharField(max_length=200, default="null")
    video_pub_date = models.CharField(max_length=200, default="null")
