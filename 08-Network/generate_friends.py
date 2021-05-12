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
import networkx as nx
tweetsDB = "data/network.db"

G = nx.DiGraph()

conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute("SELECT user_id, screen_name, party FROM congress"):
    G.add_node(r[0],screen_name=r[1])

for r in c.execute("""SELECT followed_by, user_id FROM followers WHERE
                        user_id in (select user_id from congress) and
                        followed_by in (select user_id from congress)"""):
    G.add_edge(r[0],r[1])

conn.close()
