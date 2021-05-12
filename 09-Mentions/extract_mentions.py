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
outputDB = "data/mentions.db"
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
                tweet_processed = BasicTweet(tweet_json)
                if tweet_processed:
                    tweets.append(tweet_processed)
        infile.close()
        os.rename(inputJSON, archiveJSON)

# Extract mentions and write to database
i = 0
conn = sqlite3.connect(outputDB)
c = conn.cursor()
for tweet in tweets:
    i += 1
    log(str(i) + " of " + str(len(tweets)))
    tweet.extractMentions()
    tweet.insert(c)
    for mention in tweet.mentions:
        mention.save(c)
conn.commit()
conn.close()
