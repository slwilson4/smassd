import datetime
import re
import random
import time
import sys
import shapely.geometry
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import box
from shapely.geometry import mapping
from shapely.geometry import MultiPoint
import shapefile
import sqlite3
import pandas as pd
import pprint

sys.path.append("..")
from smassd_functions import *

# this function finds which country a given lat/lon set is in
def scanBruteForce(sf, lat, lon):
    point = shapely.geometry.Point(lon, lat)
    for country in sf.shapeRecords():
        polygon = shapely.geometry.asShape(country.shape)
        if polygon.contains(point):
            return country.record['GID_0']
    return 'NOT'

# load the country codes hash from CSV file
def loadCountryHash():
    c_codes = {}
    df = pd.read_csv("c_codes.csv", encoding='UTF-8')
    i = 0
    for c_code in df['c_code']:
        c_codes[c_code] = df['gid_0'][i]
        i += 1
    return c_codes

# cache the countries for all the places in the database
def getPlaces(inputDB):
    places = {}
    conn = sqlite3.connect(inputDB)
    c = conn.cursor()
    c.execute("SELECT id, country FROM places")
    for r in c.fetchall():
        places[r[0]] = r[1]
    c.close()
    conn.close()
    return places

# this function caches the shapes from a shapefile by country
def cacheShapes(sf):
    country_hash = {}
    for country in sf.shapeRecords():
        polygon = shapely.geometry.asShape(country.shape)
        c_code = country.record['GID_0']
        country_hash[c_code] = polygon
    return country_hash

# this function loads the cache of previous lat/lon/country matches:
def getCache(cacheDB):
    cache = {}
    conn = sqlite3.connect(cacheDB)
    c = conn.cursor()
    c.execute("SELECT lat, lon, country, total FROM cache ORDER BY lat, lon, total DESC")
    for r in c.fetchall():
        key = str(r[0]) + '_' + str(r[1])
        if key not in cache:
            cache[key] = []
        cache[key].append({'c_code': r[2], 'total': r[3], 'changed': False})
    c.close()
    conn.close()
    return cache

# update the database cache
def updateCache(cacheDB, cache):
    conn = sqlite3.connect(cacheDB)
    c = conn.cursor()
    for key in cache:
        for country in cache[key]:
            if country['changed']:
                lat, lon = key.split('_')
                q = (lat, lon, country['c_code'], country['total'])
                c.execute("""REPLACE INTO cache (lat, lon, country, total)
                            VALUES (?, ?, ?, ?)""", q)
    conn.commit()
    c.close()
    conn.close()

# this function finds country searching cache only:
def scanCache(shape_hash, cache, lat, lon):
    key = str(int(round(lat))) + "_" + str(int(round(lon)))
    log(key)
    point = shapely.geometry.Point(lon, lat)
    if key in cache:
        for country in cache[key]:
            log("Trying " + country['c_code'])
            if country['c_code'] in shape_hash:
                polygon = shape_hash[country['c_code']]
                if polygon.contains(point):
                    country['total'] += 1
                    country['changed'] = True
                    return country['c_code'], cache
    return 'NOT', cache

# this function scans all countries, but also saves changes to cache
def scanFull(shape_hash, cache, lat, lon):
    key = str(int(round(lat))) + "_" + str(int(round(lon)))
    log(key)
    point = shapely.geometry.Point(lon, lat)
    for c_code in shape_hash:
        polygon = shape_hash[c_code]
        log("(Full) Trying: "+c_code)
        if polygon.contains(point):
            if key not in cache:
                cache[key] = []
            cache[key].append({'c_code': c_code, 'total': 1, 'changed': True})
            return c_code, cache

    return 'NOT', cache

# scan cached countries only, with rough intersection logic
def scanCacheRough(shape_hash, cache, lat, lon):
    key = str(int(round(lat))) + "_" + str(int(round(lon)))
    log(key)
    roughPoint = shapely.geometry.Point(lon, lat).buffer(0.1)
    if key in cache:
        for country in cache[key]:
            log("Trying " + country['c_code'])
            if country['c_code'] in shape_hash:
                polygon = shape_hash[country['c_code']]
                if polygon.intersects(roughPoint):
                    country['total'] += 1
                    country['changed'] = True
                    return country['c_code'], cache
    return 'NOT', cache

# scan full country list with rough intersection logic
def scanFullRough(shape_hash, cache, lat, lon):
    key = str(int(round(lat))) + "_" + str(int(round(lon)))
    log(key)
    roughPoint = shapely.geometry.Point(lon, lat).buffer(0.1)
    for c_code in shape_hash:
        polygon = shape_hash[c_code]
        log("(Full) Trying: "+c_code)
        if polygon.intersects(roughPoint):
            if key not in cache:
                cache[key] = []
            cache[key].append({'c_code': c_code, 'total': 1, 'changed': True})
            return c_code, cache

    return 'NOT', cache

def save_country(c, id, country):
    q = (country, id)
    c.execute("""UPDATE tweets SET country = ? WHERE id=?""", q)


