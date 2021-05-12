import sys
import wget
# including the SMaSSD support files
sys.path.append("..")
from smassd_functions import *

class URL:
    def __init__(s, tweet_id, url):
        s.tweet_id = tweet_id
        s.url = url
        s.downloaded = False

    def insert(s, c):
        q = (
            s.tweet_id, s.url
        )
        c.execute(
            """REPLACE INTO urls
                (tweet_id, url)
                VALUES(?,?)""", q)

    def download(s, c, outputDir, num):
        s.file = outputDir + str(s.tweet_id) + '_' + str(num) + '.html'
        try:
            wget.download(s.url, out=s.file)
            s.downloaded = True
        except:
            s.downloaded = False
        q = (
            s.file, s.downloaded,
            s.url, s.tweet_id
        )
        c.execute(
            """UPDATE urls SET
                file=?, downloaded=?
                WHERE url=? AND tweet_id=?""", q)
