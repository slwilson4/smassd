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
outputCSV = "output_grid.csv"
columns = ['grid_lat','grid_lon','total']
output = []
output_hash = {}

conn = sqlite3.connect("data/data.db")
c = conn.cursor()
for r in c.execute("""SELECT lat,lon,p.lat_1,p.lon_1,p.lat_2,p.lon_2
                FROM tweets t, places p where t.place_id=p.id"""):
    grid_lat = None
    grid_lon = None
    if r[0] and r[1]:
        grid_lat = int(r[0] + 0.5)
        grid_lon = int(r[1] + 0.5)
    elif r[2]:
        if abs(r[4]-r[2]) < 2 and abs(r[5]-r[3]) < 2:
            grid_lat = int(((r[2] + r[4]) / 2) + 0.5)
            grid_lon = int(((r[3] + r[5]) / 2) + 0.5)

    if grid_lat is not None:
        key = str(grid_lat) + "_" + str(grid_lon)
        if key in output_hash:
            output_hash[key] += 1
        else:
            output_hash[key] = 1

for key in output_hash:
    (grid_lat, grid_lon) = key.split("_")
    ret = {
        'grid_lat': grid_lat,
        'grid_lon': grid_lon,
        'total': output_hash[key]
    }
    output.append(ret)

output_pd = pd.DataFrame(output)
output_pd.to_csv(outputCSV, index=False)
