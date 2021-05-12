import sys

sys.path.append("..")
from smassd_functions import *

from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer

class TextTweet:
    def __init__(s, id, text):
        s.id = id
        s.text = text
        s.polarity = None
        s.topic = None
        s.neuralnet = None
        s.words = []

    def removeMentions(s):
        new_words = []
        for w in s.words:
            if not (w.startswith('@')):
                new_words.append(w)
        s.words = new_words

    def removeHashtags(s):
        new_words = []
        for w in s.words:
            if not (w.startswith('#')):
                new_words.append(w)
        s.words = new_words

    def removeURLs(s):
        new_words = []
        for w in s.words:
            if not (w.startswith('http')):
                new_words.append(w)
        s.words = new_words

    def removeStopwords(s, stop_words):
        new_words = []
        for w in s.words:
            if w not in stop_words:
                new_words.append(w)
        s.words = new_words

    def removeShortwords(s, min_length):
        new_words = []
        for w in s.words:
            if len(w) >= min_length:
                new_words.append(w)
        s.words = new_words

    def tokenize(s):
        tokenizer = TweetTokenizer(preserve_case=False)
        s.words = tokenizer.tokenize(s.text)

    def stemWords(s, stemmer):
        new_words = []
        for w in s.words:
            new_word = w
            if not (w.startswith('#') or w.startswith('@')):
                new_word = stemmer.stem(w)
            new_words.append(new_word)
        s.words = new_words

    def lemmatizeWords(s):
        # this only works for English
        wnl = WordNetLemmatizer()
        new_words = []
        for w in s.words:
            new_word = w
            if not (w.startswith('#') or w.startswith('@')):
                new_word = wnl.lemmatize(w)
            new_words.append(new_word)
        s.words = new_words
