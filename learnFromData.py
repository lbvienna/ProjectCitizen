import csv
import nltk
import pickle
import tweetHandler
import stopWords

def main(filename):
    stopWordsList = stopWords.getStopWords()
    tweets, featureList = getData(filename, stopWordsList)

    def extract_features(tweet):
        tweet_words = set(tweet)
        features = {}
        for word in featureList:
            features['contains(%s)' % word] = (word in tweet_words)
        return features

    training_data = nltk.classify.util.apply_features(extract_features, tweets)
    NBClassifier = nltk.NaiveBayesClassifier.train(training_data)
    print "trained"

    classifierFile = open("NaiveBayesClassifier.pickle", 'wb')
    pickle.dump(NBClassifier, classifierFile)
    classifierFile.close()

    featureFile = open("Features.txt", 'wb')
    for feature in featureList:
        print>>featureFile, feature

def getData(filename, stopWords):
    input_tweets = csv.reader(open('SentimentAnalysisDataset.csv', 'rb'), delimiter=',')

    tweets = []
    featureList = set()
    i = 0
    for row in input_tweets:
        #so we don't have too much data for testing purposes
        if i == 100000:
            break
        sentiment = row[1]
        tweet = row[3]
        processedTweet = tweetHandler.processTweet(tweet)
        featureVector = tweetHandler.getFeatureVector(processedTweet, stopWords)
        #so that we have a list of all features
        for word in featureVector:
            featureList.add(word)
        tweets.append((featureVector, sentiment))
        i = i + 1
    return tweets, list(featureList)

main('SentimentAnalysisDataset.csv')
