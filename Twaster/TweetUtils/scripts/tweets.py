import tweepy
import math
import threading
from http.client import IncompleteRead

from . import eqdetection
from . import svm
from . import start
from . import googleMapsApi
from . import keys

import sqlite3

consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
access_token = keys.access_token
access_token_secret = keys.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweetcount = 0
loccount = 0

class MyStreamListener(tweepy.StreamListener):
    tweetcount = 0
    def on_exception(self, exception):
        print(exception)
        start.startTweets()
        return

    def on_status(self, status):
        status = status._json
        global tweetcount
        # and not status['text'].find("breaking") and not status['text'].find("magnitude")
        if status['retweeted']==False and not status['text'].startswith('RT') and status['lang'] == "en" and status['text'].find("earthquake") >= 0:
            isEq = svm.eq_or_not(status['text'])
            if isEq == "It is eq":
                tweetcount += 1
                with sqlite3.connect('/Users/BigMac/Desktop/t/termproject/Twaster/db.sqlite3') as conn:
                    c = conn.cursor()
                    created_at = status['created_at']
                    username = status['user']['screen_name']
                    tweet = str(status['text'])
                    location = status['user']['location']
                    long = ''
                    lat = ''
                    if status['coordinates']:
                        long = status['coordinates']['coordinates'][0]
                        lat = status['coordinates']['coordinates'][1]
                        print(tweetcount, ' : ', status['text'], '\n', 'with coordinates = long : ', round(long,6) , ' lat : ', round(lat,6))
                        c.execute("insert into TweetUtils_tweet_info values (NULL, ?, ?, ?, ?, ?, ?);", (tweet,username,created_at,long,lat,location))
                        conn.commit()
                    elif status['geo']:
                        long = status['geo']['coordinates'][1]
                        lat = status['geo']['coordinates'][0]
                        print(tweetcount, ' : ', status['text'], '\n', 'with geo = long : ', round(long,6) , ' lat : ', round(lat,6))
                        c.execute("insert into TweetUtils_tweet_info values (NULL, ?, ?, ?, ?, ?, ?);", (tweet,username,created_at,long,lat,location))
                        conn.commit()
                    elif status['place']:
                        coords = status['place']['bounding_box']['coordinates'][0]
                        long = (coords[0][1] + coords[2][1]) / 2
                        lat = (coords[0][0] + coords[1][0]) / 2
                        print(tweetcount, ' : ', status['text'], '\n', 'with place = long : ', round(long,6) , ' lat : ', round(lat,6))
                        c.execute("insert into TweetUtils_tweet_info values (NULL, ?, ?, ?, ?, ?, ?);", (tweet,username,created_at,long,lat,location))
                        conn.commit()
                    elif status['user']['location']:
                        try:
                            coords = googleMapsApi.getLoc(status['user']['location'])
                            long = coords['lng']
                            lat = coords['lat']
                            print(tweetcount, ' : ', status['text'], '\n', 'google maps =  long : ', round(long,6) , ' lat : ', round(lat,6))
                            c.execute("insert into TweetUtils_tweet_info values (NULL, ?, ?, ?, ?, ?, ?);", (tweet,username,created_at,long,lat,location))
                            conn.commit()
                        except IndexError:
                            pass

                if lat != '' and long != '':
                    eqdetection.location_predicter(lat,long,created_at)
try:
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=['earthquake'], async=True) 
    print("Listening tweets now!")
except IncompleteRead:
    pass
except KeyboardInterrupt:
    myStream.disconnect()

def run():
    va = MyStreamListener()
    