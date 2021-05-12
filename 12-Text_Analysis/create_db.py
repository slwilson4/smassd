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

# Set up a table for tweets
c.execute('ALTER TABLE tweets ADD polarity INT')
c.execute('ALTER TABLE tweets ADD topic INT')
c.execute('ALTER TABLE tweets ADD neuralnet INT')

conn.commit()
conn.close()
