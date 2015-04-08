from Communicator import *
import json

def main():
    location = "Stockton CA"
    twitterCommunicator = TwitterCommunicator()
    topics = twitterCommunicator.find_trends(location)
    trends = topics[0]['trends']
    tweets_by_topic = {}
    for trend in trends:
        name = trend["name"]
        tweets = twitterCommunicator.get_tweets(name, location)
        tweets_by_topic[name] = tweets
    for topic in tweets_by_topic:
        print "topic: ", topic
        for tweet in tweets_by_topic[topic]:
            print tweet
            print "\n"
        print "------"

    tweet_set = set()
    twitter_file = open('test_tweet_file.txt', 'w')
    for topic in tweets_by_topic:
        for tweet in tweets_by_topic[topic]:
            json_tweet = json.dumps(tweet)
            if json_tweet not in tweet_set:
                twitter_file.write("%s\n" % json_tweet)
                tweet_set.add(json_tweet)
    twitter_file.close()

def locations():
    location = "San Mateo CA"
    twitterCommunicator = TwitterCommunicator()
    topics = twitterCommunicator.find_trends(location)
    print topics

#locations()
main()
