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
from MediaTweet import MediaTweet
inputDir = "queues/"
archiveDir = "archive/"
outputDB = "data/data.db"
tweets = []

# Loop through each file and process its tweets
for filename in os.listdir(inputDir):
    if filename.endswith(".json"):
        inputJSON = inputDir+filename
        archiveJSON = archiveDir+filename
        # Open JSON file and process each tweet
        infile = codecs.open(inputJSON, "r", "utf-8")
        for line in infile:
            line.rstrip("\n")
            tweet_json = False
            tweet_processed = None

            # Catch whether the line is properly formed JSON, else skip
            try:
                tweet_json = json.loads(line)
            except ValueError:
                tweet_json = False

            if tweet_json:
                tweet_processed = MediaTweet(tweet_json)
                if tweet_processed:
                    tweets.append(tweet_processed)
        infile.close()
        os.rename(inputJSON, archiveJSON)

# Write those tweets and URLs to the database
outputDir = "files/"
i = 0
conn = sqlite3.connect(outputDB)
c = conn.cursor()
for tweet in tweets:
    i += 1
    log(str(i) + " of " + str(len(tweets)))
    tweet.insert(c)
    tweet.extractURLs()
    num = 0
    for url in tweet.urls:
        num += 1
        url.insert(c)
        url.download(c, outputDir, num)
conn.commit()
conn.close()
