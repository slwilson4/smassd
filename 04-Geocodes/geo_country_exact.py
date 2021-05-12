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
from functions_geo import *
import shapefile

# Variable definitions
inputDB = "data/data.db"
sf = shapefile.Reader(shapefile_dir+"gadm36_0.shp")
exact_hash = {}

conn = sqlite3.connect(inputDB)
c = conn.cursor()
c.execute("SELECT id, lat, lon FROM tweets WHERE country IS NULL AND geo_type='precise'")
for r in c.fetchall():
    (id, lat, lon) = r
    key = str(lat) + '_' + str(lon)
    country = 'NOT'
    if key in exact_hash:
        country = exact_hash[key]
    else:
        country = scanBruteForce(sf, lat, lon)
    save_country(c, id, country)
c.close()
conn.close()
