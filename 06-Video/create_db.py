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
videoDB = "data/videos.db"

# Set up database structure
conn = sqlite3.connect(videoDB)
c = conn.cursor()

# Set up a table for videos
c.execute("""CREATE TABLE IF NOT EXISTS videos (
            file VARCHAR,
            tweet_id BIGINT,
            url VARCHAR,
            duration INT,
            title VARCHAR,
            type VARCHAR,
            checksum VARCHAR
          )""")
c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS
            idx_file ON videos(file)''')

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
