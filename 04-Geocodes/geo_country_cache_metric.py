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
from functions_geo import *
import shapefile

# Variable definitions
inputDB = "data/data.db"
cacheDB = "cache.db"
sf = shapefile.Reader("../../../../../Shoom/gadm36_levels_shp/gadm36_0.shp")
exact_hash = {}
shape_hash = cacheShapes(sf)
cache = getCache(cacheDB)
guessHash = {}

log("Finished initial cache")

# this function finds country searching cache only:
def scanCacheMetric(shape_hash, cache, lat, lon):
    key = str(int(round(lat))) + "_" + str(int(round(lon)))
    #log(key)
    point = shapely.geometry.Point(lon, lat)
    if key in cache:
        guess = 0
        for country in cache[key]:
            guess+=1
            #log("Trying " + country['c_code'])
            polygon = shape_hash[country['c_code']]
            if polygon.contains(point):
                country['total'] += 1
                country['changed'] = True
                #log(key)
                return country['c_code'], cache, str(guess)
    return 'NOT', cache, '-1'

i=0
conn = sqlite3.connect(inputDB)
c = conn.cursor()
c.execute("SELECT id, lat, lon FROM tweets WHERE country IS NOT NULL")
for r in c.fetchall():
    i+=1
    if i%10==0:
        log("FINISHED: "+str(i))
    (id, lat, lon) = r
    key = str(lat) + '_' + str(lon)
    country = 'NOT'
    if key in exact_hash:
        #country = exact_hash[key]
        log("EXACT!")
    else:
        country, cache, guess = scanCacheMetric(shape_hash, cache, lat, lon)
        if guess in guessHash:
            guessHash[guess]+=1
        else:
            guessHash[guess]=1
        #if country == 'NOT':
        #    country, cache = scanFull(shape_hash, cache, lat, lon)
    save_country(c, id, country)
    if i % 100 == 0:
        conn.commit()
conn.commit()
c.close()
conn.close()

updateCache(cacheDB, cache)

pprint.pprint(guessHash)
