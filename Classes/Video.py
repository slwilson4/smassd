import sys
import wget
# including the SMaSSD support files
sys.path.append("..")
from smassd_functions import *

class Video:
    def __init__(s, tweet_id, file, url, title, duration, type):
        s.tweet_id = tweet_id
        s.file = file
        s.url = url
        s.title = title
        s.duration = duration
        s.type = type

    def download(s, c):
        wget.download(s.url, out=s.file)
        q = (
            s.tweet_id, s.file, s.url,
            s.title, s.duration
        )
        c.execute(
            """REPLACE INTO videos
            (tweet_id, file, url, title, duration, type)
            VALUES(?,?,?,?,?,?)""", q)

    def checksum(s, c):
        s.checksum = getMD5(s.file)
        if s.checksum is not None:
            q = (s.checksum, s.file)
            c.execute("""UPDATE videos
                    SET checksum=?
                    WHERE file=?""", q)
