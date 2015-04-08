import csv
import re
import nltk


def main(filename):
    stopWords = getStopWords()
    tweets, featureList = readData(filename, stopWords)

    def extract_features(tweet):
        tweet_words = set(tweet)
        features = {}
        for word in featureList:
            features['contains(%s)' % word] = (word in tweet_words)
        return features

    training_set = nltk.classify.util.apply_features(extract_features, tweets)
    NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
    print NBClassifier.show_most_informative_features(10)


def readData(filename, stopWords):
    input_tweets = csv.reader(open('SentimentAnalysisDataset.csv', 'rb'), delimiter=',')
    tweets = []
    featureList = set()
    i = 0
    for row in input_tweets:
        #so we don't have too much data for testing purposes
        if i == 10000:
            break
        if i % 10000 == 0:
            print i
        sentiment = row[1]
        tweet = row[3]
        processedTweet = processTweet(tweet)
        featureVector = getFeatureVector(processedTweet, stopWords)
        #so that we have a list of all features
        for word in featureVector:
            featureList.add(word)
        tweets.append((featureVector, sentiment))
        i = i + 1
    return tweets, list(featureList)

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

def getStopWords():
    #st = open('stopwordsfile.txt', 'r') #check if needed
    stopWords = getStopWordList('stopwordsfile.txt')
    return stopWords

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    print "got stopWords"
    return stopWords

#start getfeatureVector
def getFeatureVector(tweet, stopWords):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end

#start process_tweet
def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet

main('SentimentAnalysisDataset.csv')
