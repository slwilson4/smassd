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
inputFile = "congress.csv"
timelineDB = "data/timeline.db"

# Set up database structure
conn = sqlite3.connect(timelineDB)
c = conn.cursor()

# Set up a table for accounts
c.execute("""CREATE TABLE IF NOT EXISTS congress (
            user_id BIGINT,
            screen_name VARCHAR,
            party VARCHAR,
            icpsr VARCHAR,
            chamber VARCHAR,
            state VARCHAR,
            last_id BIGINT,
            name VARCHAR,
            follower_count INT,
            friend_count INT,
            status_count INT,
            verified INT
          )""")
c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS
            idx_screen_name ON accounts(screen_name)''')

df = pd.read_csv(inputFile, encoding='UTF-8')

for index, row in df.iterrows():
    q=(row['user_id'], row['screen_name'], row['party'],
       row['icpsr'], row['chamber'], row['state'])
    c.execute("""REPLACE INTO congress
                (user_id,screen_name,party,icpsr,
                chamber,state,last_id)
                VALUES (?,?,?,?,?,?,1)""", q)

conn.commit()
conn.close()
