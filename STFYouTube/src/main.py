import logging as log
import re
import urllib2

from bs4 import BeautifulSoup

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

VIDEO_LINK_REGEX = re.compile(r'(^\/watch\?v\=[\w_-]{11})$')

url = "https://www.youtube.com/"


def get_soup_from_page(page_link):
    web_request = urllib2.Request(page_link, headers=HEADER)
    web_content = urllib2.urlopen(web_request).read()
    soup = BeautifulSoup(web_content.decode("utf-8"), "html.parser")
    return soup


def get_video_link_from_page(soup):
    for label in soup.find_all("a"):
        try:
            video_link = label["href"]
            if VIDEO_LINK_REGEX.match(video_link):
                link = URL_BASE + video_link
                log.info("get video_link: %s" % link)
        except Exception:
            log.error("can't get a video_link from: %s" % label)


if __name__ == '__main__':
    soup = get_soup_from_page(url)
    get_video_link_from_page(soup)
