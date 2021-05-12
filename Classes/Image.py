import sys
import wget

# including the SMaSSD support files
sys.path.append("..")
from smassd_functions import *

class Image:
    def __init__(s, tweet_id, file, url):
        s.tweet_id = tweet_id
        s.file = file
        s.url = url
        s.checksum = None
        s.downloaded = False

    def insert(s, c):
        q = (
            s.tweet_id, s.file, s.url, s.downloaded
        )
        c.execute(
            """REPLACE INTO images
            (tweet_id, file, url, downloaded)
            VALUES(?,?,?,?)""", q)

    def download(s, c):
        try:
            wget.download(s.url, out=s.file)
            s.checksum = getMD5(s.file)
            s.downloaded = True
        except:
            s.checksum = None
            s.downloaded = False

        q = (
            s.checksum, s.downloaded, s.tweet_id
        )
        c.execute(
            """UPDATE images SET
            checksum=?,downloaded=?
            WHERE file=?""", q)
