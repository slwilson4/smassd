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
tweetDB = "data/tweets.db"

# Set up database structure
conn = sqlite3.connect(tweetDB)
c = conn.cursor()

# Set up a table for training tweets
c.execute('''CREATE TABLE training_tweets (
            id BIGINT,
            text VARCHAR,
            neuralnet INT,
            training INT
          )''')

# Open CSV file:
d = pd.read_csv("neuralnet_trained.csv")
for i in range(0,len(d['id'])):
    q = (int(d['id'][i]),
            d['text'][i],
            int(d['neuralnet'][i])
         )
    c.execute(
        """REPLACE INTO training_tweets
        (id, text, neuralnet) VALUES(?,?,?)""", q)

c.execute("UPDATE training_tweets SET training=1")
c.execute("UPDATE training_tweets SET training=0 WHERE RANDOM()%10=0")

conn.commit()
conn.close()
