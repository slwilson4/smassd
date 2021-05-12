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
from polyglot.downloader import downloader
from polyglot.text import Text

# Variable definitions
tweetsDB = "data/tweets.db"

conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute('SELECT id,text FROM tweets'):
    polarity = 0
    text = Text(r[1])
    text.language = 'en'
    for w in text.words:
        polarity += w.polarity
    q = (int(polarity), r[0])
    c.execute("UPDATE tweets SET polarity=? WHERE id=?", q)
conn.commit()
conn.close()
