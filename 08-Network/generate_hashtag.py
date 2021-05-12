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

G = nx.Graph()

conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute("""SELECT hashtag,count(*) FROM hashtags
                        GROUP BY hashtag ORDER BY count(*) DESC
                        LIMIT 100"""):
    G.add_node(r[0],tweets=set())

for n in G.nodes():
    for r in c.execute("""SELECT tweet_id FROM hashtags
                        WHERE hashtag=?""",[n]):
        G.nodes[n]['tweets'].add(r[0])

for a in G.nodes():
    for b in G.nodes():
        if a!=b:
            common = len(G.nodes[a]['tweets'] & G.nodes[b]['tweets'])
            G.add_edge(a,b,weight=common)

conn.close()
