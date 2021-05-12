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
import zipfile
inputDir = "archive/"
zippedDir = "zipped/"

# Loop through each file and compress it
for filename in os.listdir(inputDir):
    if filename.endswith(".json"):
        inputFile = inputDir+filename
        outputFile = zippedDir+filename.replace('json','zip')
        zippedArchive = zipfile.ZipFile(outputFile, 'w',
                                        compression=zipfile.ZIP_DEFLATED)
        zippedArchive.write(inputFile, compress_type = zipfile.ZIP_DEFLATED)
        zippedArchive.close()