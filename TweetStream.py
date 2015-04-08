import tweepy
import sys
import pika
import json
import time
from geopy import geocoders

#credentials
consumer_key = 'OnbNyAnpA1C7W6fOMw1GgUkva'
consumer_secret = 'BmZdMP2HJcDX0BneJxumHgOj7A8l6UbfKiybV40FUqURl4XOdx'
access_token = '21001149-R7oOHcOUDW6qyjhEbP2lNRlXEidF2K90Ky9GCAAb3'
access_token_secret = 'Oinb7yjzbi1cRuy8rrYckfZP49ebjj5aqx3phVQrVL7wZ'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# auth = TwitterAuthenticator()
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        #setup rabbitMQ Connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = connection.channel()

        #set max queue size
        args = {"x-max-length": 2000}

        self.channel.queue_declare(queue='twitter_topic_feed', arguments=args)

    def on_status(self, status):
        print status.text, "\n"

        data = {}
        data['text'] = status.text
        data['created_at'] = time.mktime(status.created_at.timetuple())
        data['geo'] = status.geo
        data['source'] = status.source

        #queue the tweet
        self.channel.basic_publish(exchange='',
                                    routing_key='twitter_topic_feed',
                                    body=json.dumps(data))

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream

# geolocator = geocoders.Nominatim()
# location = geolocator.geocode("San Jose")
# print(location)

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
# sapi.filter(track=['police'])
sapi.filter(locations=[-122.75,36.8,-121.75,37.8]) # hard code San Francisco for now

