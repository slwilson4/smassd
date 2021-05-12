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
imageDB = "data/images.db"

# Set up database structure
conn = sqlite3.connect(imageDB)
c = conn.cursor()

# Set up a table for images
c.execute("""CREATE TABLE IF NOT EXISTS images (
            file VARCHAR,
            tweet_id BIGINT,
            url VARCHAR,
            checksum VARCHAR,
            downloaded BOOLEAN
          )""")
c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS
            idx_file ON images(file)''')

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
