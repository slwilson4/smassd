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
networkDB = "data/network.db"

# Set up database structure
conn = sqlite3.connect(networkDB)
c = conn.cursor()

# Set up a table for followers
c.execute("""CREATE TABLE IF NOT EXISTS followers (
            user_id BIGINT,
            followed_by BIGINT
          )""")
c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS
            idx_followers ON followers(user_id,followed_by)''')

conn.commit()
conn.close()
