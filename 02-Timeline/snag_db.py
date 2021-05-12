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
timelineDB = "data/timeline.db"
outputDir = "queues/"

# Grab list of screen names to download
accounts = []
conn = sqlite3.connect(timelineDB)
c = conn.cursor()
for r in c.execute("SELECT screen_name, last_id FROM accounts"):
    account={'screen_name':r[0], 'last_id':int(r[1])}
    accounts.append(account)
conn.close()

# Connect to API
auth_handler = OAuthHandler(consumer_key,consumer_secret)
auth_handler.set_access_token(access_token,access_token_secret)
api = API(auth_handler)

# Loop through the screen names and download their tweets
for account in accounts:
    last_id = 1
    now = datetime.datetime.now().strftime(".%Y%m%d-%H%M%S")
    outputFile = outputDir + account['screen_name'] + "_" + now + ".json"
    file = open(outputFile, 'a')
    try:
        tweets = Cursor(
                        api.user_timeline,
                        id=account['screen_name'],
                        since_id=account['last_id'],
                        wait_on_rate_limit=True,
                        monitor_rate_limit=True,
                        tweet_mode="extended"
                    )
        counter = 0
        for tweet in tweets.items():
            counter += 1
            json.dump(tweet._json,file)
            file.write("\n")
            last_id = max(tweet.id,last_id)
        conn = sqlite3.connect(timelineDB)
        c = conn.cursor()
        vals = (last_id,account['screen_name'])
        c.execute("UPDATE accounts SET last_id=? WHERE screen_name=?", vals)
        conn.commit()
        conn.close()
        log("Downloaded "+str(counter)+" new tweets from "+account['screen_name'])
    except:
        log("Error downloading tweets for account: "+account['screen_name'])
    file.close()

