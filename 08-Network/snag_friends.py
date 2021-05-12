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
tweetsDB = "data/network.db"
accounts = []

conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute("SELECT user_id, screen_name FROM congress where user_id not in (select distinct followed_by from followers)"):
    accounts.append({'user_id':r[0],
                     'screen_name':r[1]})

auth_handler = OAuthHandler(consumer_key,consumer_secret)
auth_handler.set_access_token(access_token,access_token_secret)
api = API(auth_handler, wait_on_rate_limit=True)

for a in accounts:
    log("getting: "+a['screen_name'])
    friends = []
    successful_download = True
    try:
        tc = tweepy.Cursor(api.friends_ids,screen_name=a['screen_name'])
        for friend_id in tc.items():
            friends.append(friend_id)
    except Exception as e:
        log(a['screen_name'] + ": " + str(e))
        successful_download = False

    if successful_download:
        for friend_id in friends:
            q=(friend_id,a['user_id'])
            c.execute("""REPLACE INTO followers (user_id,followed_by)
                      VALUES (?,?)""",q)
        conn.commit()
conn.close()
