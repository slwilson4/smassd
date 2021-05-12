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
from Streamer import Streamer

# Variable definitions
keywords = ['corona', 'covid', 'health', '#pandemic', '@CDCgov']
output_dir = "queues"

auth_handler = OAuthHandler(consumer_key, consumer_secret)
auth_handler.set_access_token(access_token, access_token_secret)
api = API(auth_handler)

listener = Streamer()
listener.initQueue(output_dir, 3600, 'kw')
stream = tweepy.Stream(auth=api.auth, listener=listener)
stream.filter(track=keywords)

