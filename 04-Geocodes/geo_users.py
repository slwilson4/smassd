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
user_hash = {}
sums_hash = {}
country_hash = {}

conn = sqlite3.connect(inputDB)
c = conn.cursor()
for r in c.execute("""SELECT user_id, country FROM tweets
                    WHERE geo_type IN ('precise','place')"""):
    if r[1] is not None:
        uid = str(r[0])
        if uid not in user_hash:
            user_hash[uid] = True
        if r[1] not in country_hash:
            country_hash[r[1]] = True
        key = uid + '_' + r[1]
        if key not in sums_hash:
            sums_hash[key] = 0
        sums_hash[key] += 1

for u in user_hash:
    maxVal = 0
    my_country = None
    u_total = 0
    for country in country_hash:
        key = u + '_' + country
        if key in sums_hash:
            u_total += sums_hash[key]
            if sums_hash[key]>maxVal:
                maxVal=sums_hash[key]
                my_country = country
    pct = float(maxVal)/float(u_total)
    q = (u, my_country, pct)
    c.execute("""INSERT INTO geo_users (id,country,pct) VALUES (?,?,?)""", q)

conn.commit()
conn.close()
