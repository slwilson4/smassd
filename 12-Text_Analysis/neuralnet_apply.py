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
from functions_text import *

#########################################
# MAIN CODE FOLLOWS
#########################################
from TextTweet import TextTweet
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import keras.preprocessing.text as kr
from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from sklearn.metrics import confusion_matrix
import random

nltk.download('wordnet')
nltk.download('stopwords')

# Variable definitions
en_stop = set(stopwords.words('english'))
tweetsDB = "data/tweets.db"
labels = [0, 1]
num_categories = len(labels)
input_file = "nn"

model, dictionary = load_model(input_file)
tokenizer = Tokenizer(num_words=len(dictionary)+1)

tweets = []
conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute('SELECT id,text FROM tweets'):
    tweet = TextTweet(r[0], r[1])
    tweet.tokenize()
    tweet.removeURLs()
    tweet.removeStopwords(en_stop)
    tweet.removeMentions()
    tweet.removeShortwords(3)
    tweet.text = ' '.join(tweet.words)
    tweets.append(tweet)

for tweet in tweets:
    text = prep_tweet(tweet.text, dictionary, tokenizer)
    raw_pred = model.predict(text)
    tweet.neuralnet = labels[np.argmax(raw_pred)]
    q = (tweet.neuralnet, tweet.id)
    c.execute("""UPDATE tweets SET neuralnet=? WHERE id=?""",q)
conn.commit()
conn.close()
