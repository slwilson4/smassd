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
inputJSON = "queues/output.json"
outputCSV = "data/output.csv"
columns = ['id', 'created', 'user_id', 'screen_name', 'text']
output_tweets = []


# The function to process an individual tweet
def processTweet(a):
    try:
        text = a['full_text'].replace('\n', ' ')
        text = text.replace('\r', '').replace('\t', ' ')
        timestamp = procTimestamp(a['created_at'])
        ret = {
            'id': a['id'],
            'created': timestamp,
            'user_id': a['user']['id'],
            'screen_name': a['user']['screen_name'],
            'text': text
        }
        return ret
    except KeyError:
        return False


# Open JSON file and process each tweet
infile = codecs.open(inputJSON, "r", "utf-8")
for line in infile:
    line.rstrip("\n")
    tweet_json = False
    tweet_processed = False

    # Catch whether the line is properly formed JSON, else skip
    try:
        tweet_json = json.loads(line)
    except ValueError:
        tweet_json = False

    if tweet_json:
        tweet_processed = processTweet(tweet_json)
    if tweet_processed:
        output_tweets.append(tweet_processed)

infile.close()

# Write those tweets to a CSV file
output_tweets_pd = pd.DataFrame(output_tweets)
output_tweets_pd.to_csv(outputCSV, index=False)
