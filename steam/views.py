# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import commands
import os
import urllib2

from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.template import loader

REQ_ARTWORK_URL = "http://steamcommunity.com/apps/allcontenthome/?l=schinese" \
                  "&browsefilter=trend&browsefilter=trend&appHubSubSection=4" \
                  "&appHubSubSection=4&forceanon=1&userreviewsoffset=0&p=%s" \
                  "&workshopitemspage=%s&readytouseitemspage=%s&mtxitemspage=%s" \
                  "&itemspage=%s&screenshotspage=%s&videospage=%s&artpage=%s" \
                  "&allguidepage=%s&webguidepage=%s&integratedguidepage=%s" \
                  "&discussionspage=%s&numperpage=10&appid=0"


SCREENSHOTS_URL = "http://steamcommunity.com/apps/allcontenthome/?l=schinese" \
                  "&browsefilter=trend&browsefilter=trend&appHubSubSection=2" \
                  "&appHubSubSection=2&forceanon=1&userreviewsoffset=0&p=%s" \
                  "&workshopitemspage=%s&readytouseitemspage=%s&mtxitemspage=%s" \
                  "&itemspage=%s&screenshotspage=%s&videospage=%s&artpage=%s" \
                  "&allguidepage=%s&webguidepage=%s&integratedguidepage=%s" \
                  "&discussionspage=%s&numperpage=10&appid=0"



HEADER = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.youtube.com",
    "Connection": "keep-alive"}

IMAGE_STORE_PATH = "/var/www/html/media/SFTYouTube/image/"


def get_page_soup(page_link):
    web_request = urllib2.Request(page_link, headers=HEADER)
    web_content = urllib2.urlopen(web_request).read()
    # with open("steam.html", 'w') as f:
    #     f.write(web_content)
    page_soup = BeautifulSoup(web_content.decode("utf-8"), "html.parser")
    return page_soup


def find_all_images(page_link):
    img_link_list = []
    page_soup = get_page_soup(page_link)
    for label in page_soup.find_all("img"):
        if label['src'].startswith(
                "https://steamuserimages") \
                and "composite" not in label['src'] \
                and label['src'] not in img_link_list:
            img_link_list.append(label['src'])
    return img_link_list


def write_image_to_disk(page, img_link_list, image_type):
    if not os.path.exists(IMAGE_STORE_PATH):
        mkdir_video_path_cmd = "mkdir -p %s" % IMAGE_STORE_PATH
        commands.getstatusoutput(mkdir_video_path_cmd)
    os.chdir(IMAGE_STORE_PATH)
    for link in img_link_list:
        web_content = urllib2.urlopen(link).read()
        index = img_link_list.index(link)
        with open("%s_%s_%s.jpg" % (image_type, page, index), 'wb') as f:
            f.write(web_content)


def steam_image_home(request):
    template = loader.get_template("steam_home.html")
    context = {}
    return HttpResponse(template.render(context, request))


def artwork_view(request):
    for i in range(1, 20):
        page = str(i)
        page_request_link = REQ_ARTWORK_URL % (
            page, page, page, page, page, page, page, page, page, page, page, page)
        img_link_list = find_all_images(page_request_link)
        write_image_to_disk(page, img_link_list, "ARTWORK")
    image_files = commands.getoutput("ls ARTWORK*").split("\n")
    template = loader.get_template("steam_artwork.html")
    image_path = "/media/SFTYouTube/image/"
    context = {
        'image_path': image_path,
        'image_files': image_files,
    }
    return HttpResponse(template.render(context, request))


def screenshots_view(request):
    for i in range(1, 20):
        page = str(i)
        page_request_link = SCREENSHOTS_URL % (
            page, page, page, page, page, page, page, page, page, page, page, page)
        img_link_list = find_all_images(page_request_link)
        write_image_to_disk(page, img_link_list, "SCREENSHOTS")
    image_files = commands.getoutput("ls SCREENSHOTS*").split("\n")
    template = loader.get_template("steam_screenshots.html")
    image_path = "/media/SFTYouTube/image/"
    context = {
        'image_path': image_path,
        'image_files': image_files,
    }
    return HttpResponse(template.render(context, request))
