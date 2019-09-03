#!/usr/bin/env python
# coding: utf-8

import json
import logging as log
import os
import re
import requests
import subprocess

from bs4 import BeautifulSoup

from STFYouTube.models import Video

log.basicConfig(
    level=log.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] '
           '%(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='STFYouTube.log',
    filemode='w')

HEADER = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) "
                  "Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,"
              "application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.youtube.com",
    "Connection": "keep-alive"}

M4A_CODE = 140
VIDEO_STORE_PATH = "/var/www/html/media/SFTYouTube/video/"
URL_BASE = "https://www.youtube.com"
VIDEO_LINK_REGEX = re.compile(r'(^/watch\?v=[\w_-]{11})$')


class Utils(object):

    @staticmethod
    def get_soup_from_page(page_link):
        kwargs = {"headers": HEADER}
        web_resp = requests.get(page_link, kwargs)
        web_content = web_resp.content

        page_soup = BeautifulSoup(web_content.decode("utf-8"), "html.parser")
        return page_soup

    @staticmethod
    def get_video_model_from_page(page_soup):
        for label in page_soup.find_all("h3", class_="yt-lockup-title "):
            log.info(label)
            try:
                link = label.a["href"]
                video_title = label.a["title"].encode('utf-8').strip()
                video_link = URL_BASE + link
                video_id = link[-11:]
                video_duration = label.span.string.strip().split(
                    "- Duration: ")[1][:-1]
                video_author = label.next_sibling.a.string.strip()
                video_author_link = label.next_sibling.a["href"]
                video_view = label.next_sibling.next_sibling.ul.li.string
                video_pub_date = \
                    label.next_sibling.next_sibling.ul.li.next_sibling.string

                if not Video.objects.filter(video_id=video_id):
                    Video(
                        video_id=video_id,
                        video_title=video_title,
                        video_link=video_link,
                        video_author=video_author,
                        video_duration=video_duration,
                        video_author_link=video_author_link,
                        video_view=video_view,
                        video_pub_date=video_pub_date).save()
                log.info("get video_link: %s" % video_link)
            except Exception:
                pass

    @classmethod
    def get_video_formats(cls, video_link):
        format_cmd = "youtube-dl -F %s" % video_link
        formats_string = cls.exe_cmd(format_cmd)[1]
        formats = ["%s||%s" % (line.split('mp4')[0].strip(),
                               line.split('mp4')[1].split("DASH video")[0].strip())
                   for line in formats_string.split('\n') if "DASH video" in line]
        formats = json.dumps(formats)
        print(formats)
        model = Video.objects.get(video_link=video_link)
        model.video_formats = formats
        model.save()

    @classmethod
    def get_video_best_quality(cls, video_link):
        formats = Video.objects.get(video_link=video_link).video_formats
        formats = json.loads(formats)
        print(formats)
        best_pixel = max([x.split("x")[1] for x in formats])
        return cls.get_code_from_pixel(video_link, best_pixel)

    @staticmethod
    def get_pixel_from_code(video_link, code):
        formats = Video.objects.get(video_link=video_link).video_formats
        formats = json.loads(formats)
        for fm in formats:
            if code in fm:
                pixel = fm.split("x")[1] + "p"
                return pixel

    @staticmethod
    def get_code_from_pixel(video_link, pixel):
        formats = Video.objects.get(video_link=video_link).video_formats
        formats = json.loads(formats)
        for fm in formats:
            if pixel in fm:
                code = fm.split('||')[0]
                return code

    @classmethod
    def download_video(cls, video_link, code=137):
        if not os.path.exists(VIDEO_STORE_PATH):
            os.makedirs(VIDEO_STORE_PATH)
        os.chdir(VIDEO_STORE_PATH)
        download_cmd = "youtube-dl -f %s+%s %s" % (code, M4A_CODE, video_link)
        print(download_cmd)
        status, content = cls.exe_cmd(download_cmd)
        log.info("status:%s, content:%s" % (status, content))
        if status != 0:
            log.error("download video from %s failed" % video_link)

    @classmethod
    def rename_video(cls, video_link, code):
        video_title = Video.objects.get(video_link=video_link).video_title
        pixel = cls.get_pixel_from_code(video_link, code)
        video_name = video_title + "-" + pixel + ".mp4"
        video_id = video_link[-11:]
        log.info("video_name: %s, video_id:%s" % (video_name, video_id))
        rename_video_cmd = "qt-faststart *%s*.mp4 '%s'" % (video_id, video_name)
        status, content = cls.exe_cmd(rename_video_cmd)
        log.info("rename_video_cmd:%s, status:%s, content:%s" %
                 (rename_video_cmd, status, content))
        if status != 0:
            log.error("rename video to %s failed" % video_name)
        return video_name

    @staticmethod
    def exe_cmd(cmd_list, timeout=None):
        try:
            p = subprocess.Popen(
                cmd_list, stdout=subprocess.PIPE, encoding="utf-8")
            p.wait(timeout)
            output = p.communicate()[0]
            if p.poll() == 0:
                return True, output
        except Exception:
            pass
        raise
