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

# Grab list of screen names to download
screen_names = []
conn = sqlite3.connect(timelineDB)
c = conn.cursor()
for r in c.execute("SELECT screen_name FROM accounts"):
    screen_names.append(r[0])

# Connect to API
auth_handler = OAuthHandler(consumer_key,consumer_secret)
auth_handler.set_access_token(access_token,access_token_secret)
api = API(auth_handler)

for screen_name in screen_names:
    successful_download=True
    try:
        u = api.get_user(screen_name, wait_on_rate_limit=True)
    except Exception as e:
        log(screen_name+": "+str(e))
        successful_download=False

    if successful_download:
        q = (u.id,u.name,u.followers_count,u.friends_count,
             u.statuses_count,u.verified,screen_name)
        c.execute("""UPDATE accounts SET user_id=?,
                    name=?,follower_count=?,friend_count=?,
                    status_count=?,verified=?
                    WHERE screen_name=?""", q)
        conn.commit()

conn.close()
