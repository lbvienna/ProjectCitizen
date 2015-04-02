import codecs, os
import tweepy
from geopy import geocoders
import Authenticator

class Communicator:
    def __init__(self, file_name):
        self.twitterAuth = Authenticator()
        self.file = codecs.open(os.getcwd() + '/database/' + file_name, 'wb', 'utf-8')
        self.file_name = file_name

    #takes a location of the form City State (e.g. Stockton CA)
    def get_geolocation(location):
        geolocator = geocoders.Nominatim()
        location
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
        twitterAPI = tweepy.API(twitterAuth)
        twitterAPI.update_status('tweepy + oauth!')

        radius = "5km"
        geo = self.get_geolocation(location)
        geo_string = str(geo[0]) + "," + str(geo[1]) + "," + radius

        n = 1
        tweets = []
        for i in range(n):
            try:
                new_tweets = twitterAPI.search(q = query, geocode = geo_string, lang=language, show_user=True)
                tweets.append(new_tweets)
            except tweepy.TweepError, e:
                print "ERROR:", e
                break

    #find topics that are trending in that location
    def find_trends(self):
        pass