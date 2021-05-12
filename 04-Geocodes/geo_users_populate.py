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
inputDB = "data/data.db"
outputDB = "data/data.db"
updates = []

conn = sqlite3.connect(inputDB)
c = conn.cursor()
c.execute("SELECT id, country FROM geo_users where pct>=0.5")
for r in c.fetchall():
    update = {'id': r[0], 'country': r[1]}
    updates.append(update)
c.close()
conn.close()

conn = sqlite3.connect(outputDB)
c = conn.cursor()
for update in updates:
    q = (update['country'], update['id'])
    c.execute("""UPDATE tweets SET geo_type='guess', country = ?
                WHERE user_id=? AND geo_type='not'""", q)
conn.commit()
conn.close()