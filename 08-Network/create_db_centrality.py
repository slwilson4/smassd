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
sys.path.append("..")
from smassd_functions import *
from my_settings import *

#########################################
# MAIN CODE FOLLOWS
#########################################

# Variable definitions
networkDB = "data/network.db"

# Set up database structure
conn = sqlite3.connect(networkDB)
c = conn.cursor()

c.execute("ALTER TABLE congress ADD centrality_degree FLOAT")
c.execute("ALTER TABLE congress ADD centrality_closeness FLOAT")
c.execute("ALTER TABLE congress ADD centrality_betweenness FLOAT")

conn.commit()
conn.close()
