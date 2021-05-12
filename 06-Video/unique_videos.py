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
from Video import Video
sys.path.append("..")
from smassd_functions import *
from my_settings import *

#########################################
# MAIN CODE FOLLOWS
#########################################

# Variable definitions
outputDB = "data/videos.db"
videos = []

conn = sqlite3.connect(outputDB)
c = conn.cursor()

# Extract Unique URLs from database
for u in c.execute("""SELECT tweet_id, file, url,
                    title, duration FROM videos"""):
    videos.append(Video(u[0],u[1],u[2],u[3],u[4]))

i = 0
for video in videos:
    i += 1
    log(str(i) + " of " + str(len(videos)))
    video.checksum(c)

conn.commit()
conn.close()



