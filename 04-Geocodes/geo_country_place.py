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
from functions_geo import *
from my_settings import *

#########################################
# MAIN CODE FOLLOWS
#########################################
# Variable definitions
inputDB = "data/data.db"
places = getPlaces(inputDB)

conn = sqlite3.connect(inputDB)
c = conn.cursor()
c.execute("SELECT id, place_id FROM tweets WHERE country IS NULL AND geo_type='place'")
for r in c.fetchall():
    (id, place_id) = r
    if place_id in places:
        save_country(c, id, places[place_id])
    conn.commit()
c.close()
conn.close()
