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
sys.path.append("..")
from smassd_functions import *
from my_settings import *

#########################################
# MAIN CODE FOLLOWS
#########################################

# Variable definitions
from BasicTweet import BasicTweet
inputDir = "queues/"
archiveDir = "archive/"
outputDir = "images/"
outputDB = "data/images.db"
tweets = []

conn = sqlite3.connect(outputDB)
c = conn.cursor()
for r in c.execute('SELECT id,text FROM tweets'):
    tweet = BasicTweet(r[0], r[1])
    tweet.getImages(c)
    for image in tweet.images:
        image.download(c)
conn.commit()
conn.close()
