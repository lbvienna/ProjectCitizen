from Communicator import *

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

main()
