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
import botometer
tweetsDB = "data/tweets.db"

bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=botometer_key,
                          **twitter_app_auth)

accounts = []
conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute("SELECT distinct user_id FROM tweets"):
    accounts.append(r[0])

for id, result in bom.check_accounts_in(accounts):
    if 'scores' in result:
        q = (id, result['scores']['english'],
                 result['scores']['universal'])
        c.execute("""REPLACE INTO bot_users
                        (user_id,bot_english,bot_universal)
                        VALUES (?,?,?)""", q)
        conn.commit()
c.close()
