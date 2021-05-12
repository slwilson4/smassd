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
for r in c.execute("SELECT user_id, screen_name, party FROM congress"):
    G.add_node(r[0], screen_name=r[1], friends=set())

for n in G.nodes():
    for r in c.execute("""SELECT user_id FROM followers
                        WHERE followed_by=?""",[n]):
        G.nodes[n]['friends'].add(r[0])

for a in G.nodes():
    log("(Building network): " + G.nodes[a]['screen_name'])
    for b in G.nodes():
        if a!=b:
            common = len(G.nodes[a]['friends'] & G.nodes[b]['friends'])
            G.add_edge(a,b,weight=common)

conn.close()
