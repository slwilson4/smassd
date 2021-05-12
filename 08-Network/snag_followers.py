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

# Grab list of screen names to download
accounts = []
conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute("SELECT user_id, screen_name FROM accounts"):
    accounts.append({'user_id':r[0],
                     'screen_name':r[1]})
conn.close()

# Connect to API
auth_handler = OAuthHandler(consumer_key,consumer_secret)
auth_handler.set_access_token(access_token,access_token_secret)
api = API(auth_handler, wait_on_rate_limit=True)

conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for a in accounts:
    tc = tweepy.Cursor(api.followers_ids,screen_name=a['screen_name'])
    for follower_id in tc.items():
        q=(a['user_id'],follower_id)
        c.execute("""REPLACE INTO followers (user_id,followed_by)
                  VALUES (?,?)""",q)
        conn.commit()
conn.close()