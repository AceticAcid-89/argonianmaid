#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader

from .main import Utils
from STFYouTube.models import Video

import logging as log

APACHE_VIDEO_PATH = "/media/SFTYouTube/video/"


def home_page_view(request):
    url = "https://www.youtube.com/"
    page_soup = Utils.get_soup_from_page(url)
    Utils.get_video_model_from_page(page_soup)
    video_model = Video.objects.all()
    template = loader.get_template("home.html")
    context = {
        'video_model': video_model,
    }
    return HttpResponse(template.render(context, request))


def watch_video_page_view(request):
    video_id = request.GET['id']
    video_link = Video.objects.get(video_id=video_id).video_link
    print(video_link)
    # write video formats into video model
    Utils.get_video_formats(video_link)
    # get init best video quality
    best_code = Utils.get_video_best_quality(video_link)
    # download the video
    Utils.download_video(video_link, code=best_code)
    # rename the video
    video_name = Utils.rename_video(video_link, best_code)
    video_path = APACHE_VIDEO_PATH
    template = loader.get_template("watch_video.html")
    context = {
        'video_path': video_path,
        'video_name': video_name,
    }
    return HttpResponse(template.render(context, request))
