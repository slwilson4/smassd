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
inputFile = "accounts.csv"
outputDir = "queues/"

# Grab list of screen names to download
accounts = []
df = pd.read_csv(inputFile,encoding='UTF-8')
accounts = [x for x in df['screen_name']]

# Connect to API
auth_handler = OAuthHandler(consumer_key,consumer_secret)
auth_handler.set_access_token(access_token,access_token_secret)
api = API(auth_handler)

# Loop through the screen names and download their tweets
for account in accounts:
    outputFile = outputDir + account + ".json"
    file = open(outputFile, 'w')
    try:
        tweets = Cursor(
                        api.user_timeline,
                        id=account,
                        since_id=1,
                        wait_on_rate_limit=True,
                        monitor_rate_limit=True,
                        tweet_mode="extended"
                    )
        counter=0
        for tweet in tweets.items():
            counter+=1
            json.dump(tweet._json,file)
            file.write("\n")
        log("Downloaded "+str(counter)+" tweets from "+account)
    except:
        log("Error downloading tweets for account: "+account)
    file.close()

