# general libraries used
import sys
import pprint
import json
import re
import os
import shutil
import codecs
import time

# specific libraries used
import numpy as np
import pandas as pd
import tweepy
from tweepy import *
import sqlite3

# including the SMaSSD support files
sys.path.append("../Classes/")
from UniqueURL import UniqueURL
sys.path.append("..")
from smassd_functions import *
from my_settings import *

#########################################
# MAIN CODE FOLLOWS
#########################################

# Variable definitions
outputDir = "files/"
outputDB = "data/network.db"
urls = []

# Generate unique URLs table
conn = sqlite3.connect(outputDB)
c = conn.cursor()
c.execute('DELETE FROM unique_urls')
c.execute("""INSERT INTO unique_urls (url)
                SELECT DISTINCT url FROM urls
          """)
conn.commit()

# Extract Unique URLs from database
for u in c.execute("SELECT url_id, url FROM unique_urls"):
    urls.append(UniqueURL(u[0],u[1],outputDir))

i = 0
for url in urls:
    i += 1
    log(str(i) + " of " + str(len(urls)))
    url.download(c)
    conn.commit()
conn.close()



