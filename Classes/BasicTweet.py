import sys
from Image import Image
from Video import Video
from Mention import Mention
from Hashtag import Hashtag
from Place import Place
from URL import URL

sys.path.append("..")
from smassd_functions import *

class BasicTweet:
    def __init__(s, json):
        s.json = json
        s.valid = True
        try:
            s.tweet_id = json['id']
            s.text = json['text']
            if 'full_text' in json:
                s.text = json['full_text']
            if 'extended_tweet' in json:
                if 'full_text' in json['extended_tweet']:
                    s.text = json['extended_tweet']['full_text']
            s.text = s.text.replace('\n', ' ')
            s.text = s.text.replace('\r', '')
            s.text = s.text.replace('\t', ' ')
            s.created = procTimestamp(json['created_at'])
            s.user_id = json['user']['id']
            s.screen_name = json['user']['screen_name']
        except KeyError:
            s.valid = False

    def insert(s, c):
        q = (
            s.tweet_id, s.created, s.user_id,
            s.screen_name, s.text
        )
        c.execute(
            """REPLACE INTO tweets
            (id, created, user_id, screen_name, text)
            VALUES(?,?,?,?,?)""", q)

    def extractImages(s, outputDir):
        s.images = []
        i = 0
        if 'extended_entities' in s.json:
            media = s.json['extended_entities'].get('media', [])
            for m in media:
                i += 1
                s.procImage(m, i, outputDir)
        if 'quoted_status' in s.json:
            q_json = s.json['quoted_status']
            if 'extended_entities' in q_json:
                media = q_json['extended_entities'].get('media', [])
                for m in media:
                    i += 1
                    s.procImage(m, i, outputDir)
        if 'retweeted_status' in s.json:
            q_json = s.json['retweeted_status']
            if 'extended_entities' in q_json:
                media = q_json['extended_entities'].get('media', [])
                for m in media:
                    i += 1
                    s.procImage(m, i, outputDir)

    def procImage(s, img, num, outputDir):
        tweet_id = s.tweet_id
        url = img['media_url']
        file_type = getFileExtension(url)
        file_name = str(tweet_id) + '_' + str(num) + file_type
        output_file = outputDir + file_name
        image = Image(tweet_id, output_file, url)
        s.images.append(image)

    def extractVideo(s, outputDir):
        s.video = None
        s.procVideo(s.json, outputDir)
        if s.video is None and 'quoted_status' in s.json:
            s.procVideo(s.json['quoted_status'], outputDir)
        if s.video is None and 'retweeted_status' in s.json:
            s.procVideo(s.json['retweeted_status'], outputDir)

    def procVideo(s, tweet_json, outputDir):
        if 'extended_entities' in tweet_json:
            media = tweet_json['extended_entities'].get('media', [])
            vid_type = media[0]['type']
            if vid_type == "video":
                title = None
                if 'title' in media[0]['additional_media_info']:
                    title = media[0]['additional_media_info']['title']
                duration = None
                if 'duration_millis' in media[0]['video_info']:
                    duration = media[0]['video_info']['duration_millis']
                url = ''
                for v in media[0]['video_info']['variants']:
                    if 'bitrate' in v:
                        if v['bitrate'] > 0:
                            url = v['url']
                if url != '':
                    file_name = str(s.tweet_id) + '.mp4'
                    file = outputDir + file_name
                    s.video = Video(s.tweet_id, file, url, title, duration, vid_type)
            elif vid_type == "animated_gif":
                title = None
                duration = None
                url = media[0]['video_info']['variants'][0]['url']
                file_name = str(s.tweet_id) + '.gif'
                file = outputDir + file_name
                s.video = Video(s.tweet_id, file, url, title, duration, vid_type)

    def extractMentions(s):
        s.mentions = []
        mentions = s.json['entities'].get('user_mentions', [])
        for m in mentions:
            mention = Mention(s.tweet_id, m)
            if mention.user_id != s.user_id:
                s.mentions.append(mention)

    def extractHashtags(s):
        s.hashtags = []
        hashtags = s.json['entities'].get('hashtags', [])
        for h in hashtags:
            hashtag = Hashtag(s.tweet_id, h)
            s.hashtags.append(hashtag)

    def extractURLs(s):
        s.urls = []
        if 'urls' in s.json['entities']:
            for u in s.json['entities']['urls']:
                s.processURL(u)
        # next grab any URLs in the quoted status
        if 'quoted_status' in s.json:
            for u in s.json['quoted_status']['entities']['urls']:
                s.processURL(u)

    def processURL(s, raw_url):
        tweet_id = s.tweet_id
        url = raw_url['expanded_url']
        my_url = URL(tweet_id, url)
        # only grab external URLs
        if not (url.startswith('https://twitter.com/')):
            s.urls.append(my_url)

    def getImages(s, c):
        s.images = []
        for r in c.execute("""SELECT tweet_id, file, url, checksum,
                                downloaded FROM tweets
                                WHERE tweet_id="""+str(s.tweet_id)):
            image = Image(r[0], r[1], r[2])
            image.checksum = r[3]
            image.downloaded = r[4]
            s.images.append(image)

    def getGeo(s):
        s.lat = None
        s.lon = None
        s.place_id = None
        s.place = None
        s.geo_type = "not"
        if 'place' in s.json and s.json['place'] is not None:
            s.geo_type = 'place'
            s.place_id = s.json['place']['id']
            s.place = Place(s.place_id)
            s.place.loadJSON(s.json['place'])
        if 'coordinates' in s.json and s.json['coordinates'] is not None:
            s.geo_type = 'precise'
            s.lat = s.json['coordinates']['coordinates'][1]
            s.lon = s.json['coordinates']['coordinates'][0]

    def insertGeo(s, c):
        q = (
            s.tweet_id, s.created, s.user_id,
            s.screen_name, s.text, s.lat, s.lon,
            s.place_id, s.geo_type
        )
        c.execute(
            """REPLACE INTO tweets
            (id, created, user_id, screen_name, text,
            lat, lon, place_id, geo_type)
            VALUES(?,?,?,?,?,?,?,?,?)""", q)
        if s.place:
            s.place.insert(c)