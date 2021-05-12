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
sys.path.append("..")
from smassd_functions import *
from my_settings import *

#########################################
# MAIN CODE FOLLOWS
#########################################

# Variable definitions
dataDB = "data/data.db"

# Set up database structure
conn = sqlite3.connect(dataDB)
c = conn.cursor()

# Set up a table for urls
c.execute("""CREATE TABLE IF NOT EXISTS urls (
            tweet_id BIGINT,
            url VARCHAR,
            file VARCHAR,
            downloaded BOOLEAN
          )""")
c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS
            idx_url ON urls(tweet_id,url)''')

# Set up a table for unique urls
c.execute("""CREATE TABLE IF NOT EXISTS unique_urls (
            url_id INTEGER PRIMARY KEY AUTOINCREMENT,
            url VARCHAR,
            file VARCHAR,
            downloaded BOOLEAN
          )""")

# Set up a table for mentions
c.execute("""CREATE TABLE IF NOT EXISTS mentions (
            tweet_id BIGINT,
            user_id BIGINT
          )""")
c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS
            idx_mention ON mentions(tweet_id,user_id)''')

# Set up a table for tweets
c.execute("""CREATE TABLE IF NOT EXISTS tweets (
            id BIGINT,
            created DATETIME,
            text VARCHAR,
            user_id BIGINT,
            screen_name VARCHAR,
            followers_count INT,
            friends_count INT,
            retweet_count INT,
            favorite_count INT,
            in_reply_to_status_id BIGINT,
            in_reply_to_user_id BIGINT
          )""")
c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS
            idx_id ON tweets(id)''')

conn.commit()
conn.close()
