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
from functions_geo import *

#########################################
# MAIN CODE FOLLOWS
#########################################
import shapely.geometry
import shapefile
from GeoTweet import GeoTweet

# Variable definitions
inputDB = "data/data.db"
cacheDB = "cache.db"
sf = shapefile.Reader(shapefile_dir+"gadm36_0.shp")
simple_sf = shapefile.Writer(shapefile_dir+"simple_gadm36_0.shp")
shape_hash = cacheShapes(sf)
simple_shape_hash = cacheShapes(simple_sf)
exact_hash = {}
cache = getCache(cacheDB)

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
        country, cache = scanCache(simple_shape_hash, cache, lat, lon)
        if country == 'NOT':
            country, cache = scanCache(shape_hash, cache, lat, lon)
        if country == 'NOT':
            country, cache = scanFull(simple_shape_hash, cache, lat, lon)
        if country == 'NOT':
            country, cache = scanFull(shape_hash, cache, lat, lon)
        if country == 'NOT':
            country, cache = scanCacheRough(shape_hash, cache, lat, lon)
        if country == 'NOT':
            country, cache = scanFullRough(shape_hash, cache, lat, lon)
    save_country(c, id, country)
conn.commit()
c.close()
conn.close()

updateCache(cacheDB, cache)
