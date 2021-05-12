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
    G.add_node(r[0],screen_name=r[1],party=r[2])

for r in c.execute("""SELECT followed_by, user_id FROM followers WHERE
                        user_id in (select user_id from congress) and
                        followed_by in (select user_id from congress)"""):
    G.add_edge(r[0],r[1])

centralities = nx.degree_centrality(G)
for user_id in centralities:
    q = (centralities[user_id],user_id)
    c.execute("""UPDATE congress SET centrality_degree=?
                    WHERE user_id=?""",q)

centralities = nx.closeness_centrality(G)
for user_id in centralities:
    q = (centralities[user_id],user_id)
    c.execute("""UPDATE congress SET centrality_closeness=?
                    WHERE user_id=?""",q)

centralities = nx.betweenness_centrality(G)
for user_id in centralities:
    q = (centralities[user_id],user_id)
    c.execute("""UPDATE congress SET centrality_betweenness=?
                    WHERE user_id=?""",q)

conn.commit()
conn.close()

nx.write_gexf(G, 'congress.gexf')
adjacency = nx.to_pandas_adjacency(G)
adjacency.to_csv('congress_adj.csv', index=False)
