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
inputFile = "input.csv"
outputFile = "queues/output.json"

# Grab list of tweet IDs to download
ids = []
df = pd.read_csv(inputFile,encoding='UTF-8')
ids = [x for x in df['id']]

# Connect to API
auth_handler = OAuthHandler(consumer_key,consumer_secret)
auth_handler.set_access_token(access_token,access_token_secret)
api = API(auth_handler)

# Loop through IDs and download them
tweets = []
for id in ids:
    try:
        tweet = api.get_status(
                    id,
                    tweet_mode='extended',
                    wait_on_rate_limit=True)
        tweets.append(tweet)
    except:
        log("Error downloading tweet: "+id)

# Write tweets to file
file = open(outputFile, 'w', encoding='UTF-8')
for tweet in tweets:
    json.dump(tweet._json,file)
    file.write("\n")
file.close()
log("Finished")