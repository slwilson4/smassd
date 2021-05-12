import tweepy
import datetime
import json

class Streamer(tweepy.StreamListener):

    def initQueue(s, output_dir, rotation_time, label):
        s.output_dir = output_dir
        s.rotation_time = rotation_time
        s.label = label
        # create new output file
        s.last_rotated = datetime.datetime.now()
        s.file_name = s.label+'_'+f'{s.last_rotated:%Y%m%d-%H%M%S}'+'.json'
        s.file = open(s.output_dir+'/'+s.file_name, 'w', encoding='UTF-8')

    def on_status(s, tweet):
        current_time = datetime.datetime.now()
        time_elapsed = (current_time - s.last_rotated).seconds
        if time_elapsed>s.rotation_time:
            s.file.close()
            s.initQueue(s.output_dir, s.rotation_time, s.label)
        json.dump(tweet._json, s.file)
        s.file.write("\n")