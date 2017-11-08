# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

from main import *


def home_page_view(request):
    url = "https://www.youtube.com/"
    page_soup = get_soup_from_page(url)
    get_video_link_from_page(page_soup)

    return HttpResponse('helllo')
