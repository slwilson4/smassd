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

nltk.download('wordnet')
nltk.download('stopwords')

language = 'english'
en_stop = set(stopwords.words(language))
stemmer = SnowballStemmer(language)

# Variable definitions
tweetsDB = "data/tweets.db"
tweets = []

# Set up LDA functions


# Connect to the database and loop through all tweets
tweets = []
conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute('SELECT id,text FROM tweets'):
    tweets.append(TextTweet(r[0], r[1]))
conn.close()

# Now calculate polarity for each
documents = []
for tweet in tweets:
    tweet.tokenize()
    tweet.removeURLs()
    tweet.removeStopwords(en_stop)
    # explains why remove mentions for this
    tweet.removeMentions()
    tweet.removeShortwords(3)
    #tweet.stemWords(stemmer)
    tweet.lemmatizeWords()
    #pprint.pprint(tweet.text)
    #for w in tweet.words:
    #    pprint.pprint(w)
    documents.append(tweet.words)

# explain dictionary as hash of occurences of words
dictionary = gensim.corpora.Dictionary(documents)
# get rid of extreme cases
dictionary.filter_extremes(no_below=50, no_above=0.5, keep_n=10000)
# turn this into a bag of words, explain what that is
bow_corpus = [dictionary.doc2bow(doc) for doc in documents]
# explain TFIDF
tfidf = gensim.models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

# build LDA model! Set number of topics
lda_model = gensim.models.ldamodel.LdaModel(
    corpus=corpus_tfidf,
    id2word=dictionary,
    num_topics=5)

import pyLDAvis.gensim
#pyLDAvis.enable_notebook()
lda_display = pyLDAvis.gensim.prepare(lda_model,bow_corpus,dictionary,sort_topics=False)
pyLDAvis.save_html(lda_display,'test.html')
# NEAT! That creates a self contained html file!
