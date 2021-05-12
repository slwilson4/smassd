import sys
import wget
# including the SMaSSD support files
sys.path.append("..")
from smassd_functions import *

class UniqueURL:
    def __init__(s, url_id, url, outputDir):
        s.url_id = url_id
        s.url = url
        s.file = outputDir + str(url_id) + '.html'
        s.downloaded = False

    def download(s, c):
        try:
            wget.download(s.url, out=s.file)
            s.downloaded = True
        except:
            s.downloaded = False
        q = (
            s.file, s.downloaded, s.url_id
        )
        c.execute(
            """UPDATE unique_urls SET
                file=?, downloaded=?
                WHERE url_id=?""", q)
