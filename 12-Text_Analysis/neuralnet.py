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
from functions_text import *
from my_settings import *

#########################################
# MAIN CODE FOLLOWS
#########################################
from TextTweet import TextTweet
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import keras.preprocessing.text as kr
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from sklearn.metrics import confusion_matrix

nltk.download('wordnet')
nltk.download('stopwords')

language = 'english'
en_stop = set(stopwords.words(language))

tweetsDB = "data/tweets.db"
tweets = []

labels = [0, 1]
num_categories = len(labels)
output_file = "nn"

train_text = []
train_output = []
test_text = []
test_output = []

conn = sqlite3.connect(tweetsDB)
c = conn.cursor()
for r in c.execute('SELECT id,text,neuralnet,training FROM training_tweets'):
    tweet = TextTweet(r[0], r[1])
    tweet.tokenize()
    tweet.removeURLs()
    tweet.removeStopwords(en_stop)
    tweet.removeMentions()
    tweet.removeShortwords(3)
    processed_text = ' '.join(tweet.words)
    if r[3]==0:
        test_text.append(processed_text)
        test_output.append(r[2])
    else:
        train_text.append(processed_text)
        train_output.append(r[2])
conn.close()

tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_text)
dictionary = tokenizer.word_index

train_text = prep_training(train_text, dictionary, tokenizer)

encoder = LabelEncoder()
train_output = np_utils.to_categorical(encoder.fit_transform(train_output))

model = Sequential()
model.add(Dense(512, input_shape=(len(dictionary)+1,), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='tanh'))
model.add(Dropout(0.5))
model.add(Dense(num_categories, activation='sigmoid'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(train_text, train_output,
          batch_size=32,
          epochs=10,
          verbose=1,
          validation_split=0.2,
          shuffle=True)

test_text = prep_text(test_text,dictionary,tokenizer)
predictions = []
for t in test_text:
    raw_pred = model.predict(t)
    pred = labels[np.argmax(raw_pred)]
    predictions.append(pred)
cm = confusion_matrix(test_output, predictions)
pprint.pprint(cm)

save_model("nn",dictionary,model)
