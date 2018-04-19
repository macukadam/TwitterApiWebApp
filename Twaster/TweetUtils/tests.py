from django.test import TestCase

import tweepy
import math
import threading
try:
    from .svm_resources import svm
    from .svm_resources import start
    from .svm_resources import googleMapsApi
except ImportError:
    from svm_resources import svm
    from svm_resources import start
    from svm_resources import googleMapsApi
import sqlite3

import json




consumer_key = "poNrjE0WvJnUu0HWe7L51Lpz1"
consumer_secret = "Ml0bygRn4Zjc6zuJeoPTzhWsC5r5nmO9Q0QZZKztq0VsebimOe"
access_token = "787726935363358720-2lpPfeOvOqhZPfa6KNwayscYksxxlgp"
access_token_secret = "wbvwy4LEJrGr4gUGHc9d8ef4dQWxV10Mvwr6W0hXDAioD"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweetcount = 0

class MyStreamListener(tweepy.StreamListener):
    tweetcount = 0
    def on_exception(self, exception):
        print(exception)
        return

    def on_status(self, status):
        status = status._json
        global tweetcount
        tweetcount += 1
        if status['coordinates']:
            long = status['coordinates']['coordinates'][0]
            lat = status['coordinates']['coordinates'][1]
            print(tweetcount, ' : ', 'with coordinates = long : ', round(long,6) , ' lat : ', round(lat,6))
        elif status['geo']:
            long = status['geo']['coordinates'][1]
            lat = status['geo']['coordinates'][0]
            print(tweetcount, ' : ', 'with geo = long : ', round(long,6) , ' lat : ', round(lat,6))
        elif status['place']:
            coords = status['place']['bounding_box']['coordinates'][0]
            long = (coords[0][1] + coords[2][1]) / 2
            lat = (coords[0][0] + coords[1][0]) / 2
            print(tweetcount, ' : ', 'with place = long : ', round(long,6) , ' lat : ', round(lat,6))
        elif status['user']['location']:
            try:
                coords = googleMapsApi.getLoc(status['user']['location'])
                lat = coords['lat']
                long = coords['lng']
                print(tweetcount, ' : ', 'google maps =  long : ', round(long,6) , ' lat : ', round(lat,6))
            except IndexError:
                pass
        

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['day'], async=True) 
print("Listening tweets now!")




















































# import datetime
# import math

# lmbda = 0.34
# pf = 0.35
# n0 = 10
# def p_occur(t):
#     return 1-pf**(n0*(1-math.exp(-lmbda*(t +1)))/(1-math.exp(-lmbda)))

# print(p_occur(0))

# import threading

# def printit():
#     threading.Timer(5.0, printit).start()
#     print("Hello, World!")

# printit()


#json basis
#print(json.dumps(status, indent=4, sort_keys=True))