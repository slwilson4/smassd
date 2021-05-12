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
timelineDB = "data/timeline.db"

# Set up database structure
conn = sqlite3.connect(timelineDB)
c = conn.cursor()

# Set up a table for accounts
c.execute("""CREATE TABLE IF NOT EXISTS accounts (
            user_id BIGINT,
            screen_name VARCHAR,
            last_id BIGINT,
            name VARCHAR,
            follower_count INT,
            friend_count INT,
            status_count INT,
            verified INT
          )""")
c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS
            idx_screen_name ON accounts(screen_name)''')

# Grab list of screen names to download
accounts = []
df = pd.read_csv(inputFile, encoding='UTF-8')
accounts = [x for x in df['screen_name']]

for account in accounts:
    q = [account]
    c.execute("""REPLACE INTO accounts
                (screen_name,last_id)
                VALUES (?,1)""", q)

conn.commit()
conn.close()

conn = sqlite3.connect(timelineDB)
c = conn.cursor()
# Set up a table for tweets
c.execute("""CREATE TABLE IF NOT EXISTS tweets (
            id BIGINT,
            created DATETIME,
            text VARCHAR,
            user_id BIGINT,
            screen_name VARCHAR
          )""")
c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS
            idx_id ON tweets(id)''')

conn.commit()
conn.close()