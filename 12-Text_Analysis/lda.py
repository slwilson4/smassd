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
from TextTweet import TextTweet
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import gensim
from gensim import corpora
from gensim import models
import pyLDAvis.gensim

nltk.download('wordnet')
nltk.download('stopwords')

language = 'english'
en_stop = set(stopwords.words(language))
stemmer = SnowballStemmer(language)

tweetsDB = "data/tweets.db"
outputHTML = "output.html"
num_topics = 5

# Connect to the database and loop through all tweets
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
    #tweet.stemWords(stemmer)
    tweet.lemmatizeWords()
    tweets.append(tweet)
conn.close()
documents = [x.words for x in tweets]


# Construct and run LDA model
dictionary = gensim.corpora.Dictionary(documents)
dictionary.filter_extremes(no_below=50, no_above=0.5, keep_n=10000)
corpus = [dictionary.doc2bow(x) for x in documents]
lda_model = gensim.models.ldamodel.LdaModel(
    corpus=gensim.models.TfidfModel(corpus)[corpus],
    id2word=dictionary,
    num_topics=num_topics)

# Loop through and save results of model to database
threshold = 0.5
conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for tweet in tweets:
    bow = dictionary.doc2bow(tweet.words)
    topics = lda_model.get_document_topics(bow)
    max_prob = 0
    for t in topics:
        if t[1]>max_prob and t[1]>threshold:
            max_prob = t[1]
            tweet.topic = t[0]
    if tweet.topic is not None:
        q = (tweet.topic, tweet.id)
        c.execute("UPDATE tweets SET topic=? WHERE id=?", q)
conn.commit()
conn.close()

# Printing out topic details
for index, topic in lda_model.print_topics(num_topics=-1, num_words=20):
    print(str(index)+": "+topic)

# Generating visualization HTML file
lda_display = pyLDAvis.gensim.prepare(lda_model,corpus,dictionary)
pyLDAvis.save_html(lda_display,outputHTML)