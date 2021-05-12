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
import math

sf = shapefile.Reader(shapefile_dir+"gadm36_0.shp")
simple_sf = shapefile.Writer(shapefile_dir+"simple_gadm36_0")
simple_sf.fields = sf.fields[1:]
areaOldTotal = 0
areaNewTotal = 0

for country in sf.iterShapeRecords():
    startShape = shapely.geometry.asShape(country.shape)
    # calculate old areas:
    areaOld = startShape.area
    areaOldTotal = areaOldTotal + areaOld
    # calculate tolerances:
    tolerance = .03 * math.sqrt(areaOld)
    if tolerance > 0.5:
        tolerance = 0.5
    # shrink shape inwards:
    simpleShape = startShape.buffer(-1*tolerance)
    # simplify borders of shape:
    simpleShape = simpleShape.simplify(tolerance)
    if not simpleShape.within(startShape):
        try:
            simpleShape2 = simpleShape.intersection(startShape)
            simpleShape = simpleShape2
        except Exception as e:
            log(country.record['GID_0'])

    # calculate new areas:
    areaNew = simpleShape.area
    areaNewTotal = areaNewTotal + areaNew
    efficiency = 100 * areaNew / areaOld
    if efficiency > 10:
        simple_sf.record(*country.record)
        simple_sf.shape(mapping(simpleShape))
    log(country.record['GID_0']+": " + str(efficiency) + "%")

efficiencyTotal = 100*areaNewTotal/areaOldTotal
log("Total Efficiency of "+str(efficiencyTotal)+"%")
simple_sf.close()