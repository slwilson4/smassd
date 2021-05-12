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
K = nx.Graph()

conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute("SELECT user_id, screen_name, party FROM congress"):
    G.add_node(r[0],screen_name=r[1],friends=set())
    color1 = '0'
    color2 = '170'
    if r[2] == 'Republican':
        color1 = '170'
        color2 = '0'
    K.add_node(r[0], screen_name=r[1], viz={'color': {'r': color1, 'b': color2, 'g': "0", 'a': "0.7"}})

for n in G.nodes():
    for r in c.execute("""SELECT user_id FROM followers
                        WHERE followed_by=? AND user_id IN
                        (SELECT user_id FROM congress)
                        """,[n]):
        G.nodes[n]['friends'].add(r[0])

for a in G.nodes():
    log("(Building network): " + G.nodes[a]['screen_name'])
    for b in G.nodes():
        if a!=b and b in G.nodes[a]['friends']:
            if a in G.nodes[b]['friends']:
                G.add_edge(a,b)
                K.add_edge(a, b)

conn.close()

nx.write_gexf(K, 'congress_both.gexf')

import networkx.algorithms.community as nxcom
communities = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)
pprint.pprint(len(communities))

result = nxcom.girvan_newman(G)
communities = next(result)
pprint.pprint(len(communities))

#cliques = list(nx.find_cliques(G))
#pprint.pprint(len(cliques))
#max_clique = max(cliques, key=len)

communities = nxcom.k_clique_communities(G,6)
pprint.pprint(communities)



#pprint.pprint(max_clique)
