import sys
import pprint
import json
import re
import os
import shutil
import codecs
import time as t
import unicodedata
import pandas as pd
import requests
import datetime

# including the SMaSSD support files
sys.path.append("../Classes/")
sys.path.append("..")
from smassd_functions import *
from my_settings import *

#####################

def create_headers(bt):
    headers = {"Authorization": "Bearer {}".format(bt)}
    return headers

def create_url(keyword, start_date, end_date, max_results):
    
    search_url = "https://api.twitter.com/2/tweets/search/all" #Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    #'expansions': 'author_id,in_reply_to_user_id,geo.place_id,attachments.media_keys,attachments.poll_ids,referenced_tweets.id,referenced_tweets.id.author_id',
                    #'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source,entities',
                    #'media.fields': 'duration_ms,height,media_key,preview_image_url,type,url,width',
                    #'user.fields': 'id,name,username,created_at,description,public_metrics,verified,entities,location,profile_image_url,url',
                    #'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#####################

log("starting")

accounts=['senrubiopress','aoc']

a_num=0
# Loop through the screen names and download their tweets
for a in accounts:
    a_num+=1
    total=0
    log("Snagging: "+a)

    page=0
    catdir='queues'
    if not os.path.exists(catdir):
        os.makedirs(catdir)

    filename = catdir+'/raw_'+a+".json"

    headers = create_headers(bearer_token)
    keyword = "from:"+a
    start_time = "2006-03-21T00:00:00.000Z"
    end_time = "2022-06-22T00:00:00.000Z"
    max_results = 500

    next_token = None
    more_tweets = True

    while more_tweets:
        page+=1
        log("Page #"+str(page))
        url = create_url(keyword, start_time, end_time, max_results)
        json_response = connect_to_endpoint(url[0], headers, url[1], next_token)

        if 'data' in json_response:
            file = open(filename, 'a')
            for status in json_response['data']:
                total+=1
                file.write(status['id'])
                file.write("\n")

            file.close()

            if 'next_token' in json_response['meta']:
                next_token = json_response['meta']['next_token']
            else:
                more_tweets = False

        else:
            log("No tweets this time period")
            more_tweets = False
        t.sleep(4)
        break

    log("Finished #"+str(a_num)+" "+a+": "+str(total)+" tweets")

    t.sleep(60)

