import datetime
import re
import random
import time
import hashlib
import sys
import datetime
import json

sys.path.append("..")
from smassd_functions import *

import keras.preprocessing.text as kr
from keras.models import model_from_json

def prep_training(texts, dictionary, tokenizer):
    wordArrays = []
    for t in texts:
        words = kr.text_to_word_sequence(t)
        wordArray = []
        for w in words:
            if w in dictionary:
                wordArray.append(dictionary[w])
        wordArrays.append(wordArray)
    return tokenizer.sequences_to_matrix(wordArrays, mode='binary')

def prep_text(texts, dictionary, tokenizer):
    wordArrays = []
    for t in texts:
        words = kr.text_to_word_sequence(t)
        wordArray = []
        for w in words:
            if w in dictionary:
                wordArray.append(dictionary[w])
        wordArrays.append(tokenizer.sequences_to_matrix([wordArray], mode='binary'))
    return wordArrays

def prep_tweet(text, dictionary, tokenizer):
    words = kr.text_to_word_sequence(text)
    wordArray = []
    for w in words:
        if w in dictionary:
            wordArray.append(dictionary[w])
    return tokenizer.sequences_to_matrix([wordArray], mode='binary')

def save_model(name,dictionary,model):
    #curtime = datetime.datetime.now()
    #file_prefix = 'models/'+f'{curtime:%Y%m%d-%H%M%S}'
    file_prefix = 'models/'+name
    output_dictionary = file_prefix + "_dict.json"
    output_structure = file_prefix + "_structure.json"
    output_weights = file_prefix + "_weights.h5"
    with open(output_dictionary, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False)
    with open(output_structure, 'w') as f:
        f.write(model.to_json())
    model.save_weights(output_weights)

def load_model(name):
    file_prefix = 'models/' + name
    input_dictionary = file_prefix + "_dict.json"
    input_structure = file_prefix + "_structure.json"
    input_weights = file_prefix + "_weights.h5"
    with open(input_dictionary, 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
    with open(input_structure, 'r') as f:
        loaded_model_json = f.read()
    model = model_from_json(loaded_model_json)
    model.load_weights(input_weights)
    return model, dictionary