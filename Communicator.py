import codecs, os
import tweepy
from geopy import geocoders
from Authenticator import *
from tweetHandler import *

class TwitterCommunicator:
    def __init__(self, file_name = None):
        self.twitterAuth = TwitterAuthenticator()
        if file_name != None:
            self.file = codecs.open(os.getcwd() + '/database/' + file_name, 'wb', 'utf-8')
            self.file_name = file_name

    def get_api(self):
        twitterAuth = self.twitterAuth
        twitterAPI = tweepy.API(twitterAuth)
        return twitterAPI

    #takes a location of the form City State (e.g. Stockton CA)
    def get_geolocation(self, location):
        geolocator = geocoders.Nominatim()
        try:
            location = geolocator.geocode(location)
        except ValueError, e:
            print e
        except geocoders.google.GQueryError, e:
            print e

        return location.latitude, location.longitude

    #location: City State
    def get_tweets(self, query, location, language = 'en'):
        twitterAuth = self.twitterAuth

        radius = "5km"
        geo = self.get_geolocation(location)
        geo_string = str(geo[0]) + "," + str(geo[1]) + "," + radius

        n = 1

        tweets = []
        tweet_set = set()
        for i in range(n):
            try:
                new_tweets = twitterAuth.api.search(q = query, geocode = geo_string, lang=language, show_user=True)
                for tweet in new_tweets:
                    if tweet not in tweet_set:
                        tweet_set.add(tweet)
                        cleaned_tweet = tweetToDict(tweet)
                        tweets.append(cleaned_tweet)
            except tweepy.TweepError, e:
                print e
                break

        return tweets

    #find topics that are trending in that location
    def find_trends(self, location):
        twitterAuth = self.twitterAuth

        geo = self.get_geolocation(location)

        topics = []
        try:
            places = twitterAuth.api.trends_closest(geo[0], geo[1])
            for loc in places:
                try:
                    topics += twitterAuth.api.trends_place(loc["woeid"])
                except tweepy.TweepError, e:
                    print e
                    break
        except tweepy.TweepError, e:
            print e

        return topics

