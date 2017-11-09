import commands
import urllib2

HEADER = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.youtube.com",
    "Connection": "keep-alive"}


def write_html_file(page_link):
    web_request = urllib2.Request(page_link, headers=HEADER)
    web_content = urllib2.urlopen(web_request).read()
    with open("youtube.html", 'w') as f:
        f.write(web_content)


def get_video_formats(video_link):
    format_cmd = "youtube-dl -F %s" % video_link
    print format_cmd
    output = '[youtube] R7RSi9V7FZM: Downloading webpage\n[youtube] R7RSi9V7FZM: Downloading video info webpage\n[youtube] R7RSi9V7FZM: Extracting video information\n[youtube] R7RSi9V7FZM: Downloading js player vfl8XKJyP\n[youtube] R7RSi9V7FZM: Downloading MPD manifest\n[info] Available formats for R7RSi9V7FZM:\nformat code  extension  resolution note\n139          m4a        audio only DASH audio   48k , m4a_dash container, mp4a.40.5@ 48k (22050Hz), 2.20MiB\n249          webm       audio only DASH audio   55k , opus @ 50k, 2.31MiB\n250          webm       audio only DASH audio   74k , opus @ 70k, 3.01MiB\n140          m4a        audio only DASH audio  128k , m4a_dash container, mp4a.40.2@128k (44100Hz), 5.88MiB\n171          webm       audio only DASH audio  136k , vorbis@128k, 5.83MiB\n251          webm       audio only DASH audio  140k , opus @160k, 5.93MiB\n160          mp4        256x144    DASH video  111k , avc1.4d400c, 30fps, video only, 4.54MiB\n278          webm       256x144    144p  146k , webm container, vp9, 15fps, video only, 4.98MiB\n133          mp4        426x240    DASH video  247k , avc1.4d4015, 30fps, video only, 9.36MiB\n242          webm       426x240    240p  295k , vp9, 30fps, video only, 10.68MiB\n243          webm       640x360    360p  535k , vp9, 30fps, video only, 19.67MiB\n134          mp4        640x360    DASH video  641k , avc1.4d401e, 30fps, video only, 23.99MiB\n244          webm       854x480    480p  988k , vp9, 30fps, video only, 36.70MiB\n135          mp4        854x480    DASH video 1274k , avc1.4d401f, 30fps, video only, 47.01MiB\n17           3gp        176x144    small , mp4v.20.3, mp4a.40.2@ 24k\n36           3gp        320x180    small , mp4v.20.3, mp4a.40.2\n43           webm       640x360    medium , vp8.0, vorbis@128k\n18           mp4        640x360    medium , avc1.42001E, mp4a.40.2@ 96k (best)'
    for x in output.split('\n'):
        if 'DASH video' in x:
            print x.split('mp4')[0].strip()


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=R7RSi9V7FZM"
    get_video_formats(url)
