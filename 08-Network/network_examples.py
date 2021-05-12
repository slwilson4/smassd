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
import matplotlib.pyplot as plt
tweetsDB = "data/network.db"

accounts = []

G = nx.DiGraph()

conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute("SELECT user_id, screen_name FROM accounts"):
    #accounts.append({'user_id':r[0],
    #                 'screen_name':r[1]})
    G.add_node(r[0],screen_name=r[1])

#adjacency_hash = {}
for r in c.execute("select followed_by,user_id from followers where user_id in (select user_id from accounts) and followed_by in (select user_id from accounts)"):
    #key = str(r[0])+'_'+str(r[1])
    G.add_edge(r[0],r[1])
    #adjacency_hash[key] = True

#for a in accounts:
#    for b in accounts:
#        key_1 = a['user_id'] + '_' + b['user_id']
#        key_2 = b['user_id'] + '_' + a['user_id']
#        if key_1 in adjacency_hash and key_2 in adjacency_hash:
#            G.add_edge()

pprint.pprint(G)
for n in nx.nodes(G):
    pprint.pprint(n)

print("Next!")

for e in nx.edges(G):
    pprint.pprint(e)

print("Drawing...")
nx.draw(G)
plt.savefig("simple_path.png")
plt.show()
print("Done")

out = nx.to_pandas_adjacency(G)
pprint.pprint(out)


#for a in accounts:

pprint.pprint(G.nodes[803694179079458816])

G.nodes[803694179079458816]['screen_name']='abc'

pprint.pprint(G.nodes[803694179079458816])

conn.close()