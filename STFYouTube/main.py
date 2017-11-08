import logging as log
import re
import urllib2

from bs4 import BeautifulSoup

from STFYouTube.models import Video

log.basicConfig(
    level=log.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='STFYouTube.log',
    filemode='w')

HEADER = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.youtube.com",
    "Connection": "keep-alive"}


URL_BASE = "https://www.youtube.com"
VIDEO_LINK_REGEX = re.compile(r'(^/watch\?v=[\w_-]{11})$')


def get_soup_from_page(page_link):
    web_request = urllib2.Request(page_link, headers=HEADER)
    web_content = urllib2.urlopen(web_request).read()
    # with open("youtube.html", 'w') as f:
    #     f.write(web_content)
    page_soup = BeautifulSoup(web_content.decode("utf-8"), "html.parser")
    return page_soup


def get_video_link_from_page(page_soup):
    for label in page_soup.find_all("h3", class_="yt-lockup-title "):
        log.info(label)
        try:
            link = label.a["href"]
            video_title = label.a["title"]
            video_link = URL_BASE + link
            video_id = link[-11:]
            video_duration = label.span.string.strip().split(
                "- Duration: ")[1][:-1]
            video_author = label.next_sibling.a.string.strip()
            video_author_link = label.next_sibling.a["href"]
            video_view = label.next_sibling.next_sibling.ul.li.string
            video_pub_date = label.next_sibling.next_sibling.ul.li.next_sibling.string

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
