import pickle
import json

def main(classifierFilename, tweetFilename):
    classifier = getClassifier(classifierFilename)
    tweets = getTweets(tweetFilename)
    print classifier.show_most_informative_features(10)
    classify(tweets, classifier)

def classify(tweets, classifier):
    featureList = getFeatureList()

    def extract_features(tweet):
        tweet_words = set(tweet)
        features = {}
        for word in featureList:
            features['contains(%s)' % word] = (word in tweet_words)
        return features

    for tweet in tweets:
        print tweet
        dist = classifier.prob_classify(extract_features(tweet))
        for label in dist.samples():
            print("%s: %f" % (label, dist.prob(label)))
        print classifier.classify(extract_features(tweet))

    '''
    test_tweet = "musicmonday followfriday laugh"
    print test_tweet
    dist = classifier.prob_classify(extract_features(test_tweet.split()))
    for label in dist.samples():
        print("%s: %f" % (label, dist.prob(label)))
    print classifier.classify(extract_features(test_tweet.split()))
    '''

def getClassifier(classifierFilename):
    f = open(classifierFilename)
    classifier = pickle.load(f)
    f.close()
    return classifier

def getFeatureList():
    featureFile = open("Features.txt", 'r')
    featureList = []
    for word in featureFile:
        featureList.append(word.strip())
    return featureList

def getTweets(tweetFilename):
    twitter_file = open(tweetFilename, 'r')
    tweets = []



    for tweet_string in twitter_file:
        tweet = json.loads(tweet_string)
        tweets.append(tweet['features'])
    return tweets

#classifierFilename = 'NaiveBayesClassifier.pickle'
#tweetFilename = "test_tweet_file.txt"

main('NaiveBayesClassifier.pickle', "test_tweet_file.txt")