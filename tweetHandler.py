import re
import stopWords

#These method should all handle tweets

def tweetToDict(original):
    tweet = {}
    processedTweet = processTweet(original.text)
    tweet['text'] = processedTweet
    tweet['features'] = getFeatureVector(processedTweet, stopWords.getStopWords())
    tweet['id'] = original.id
    if original.created_at.date != None:
        tweet['created'] = str(original.created_at)
    else:
        tweet['created'] = None
    tweet['geo'] = original.geo
    tweet['contributors'] = original.contributors
    tweet['coordinates'] = original.coordinates
    tweet['favorited'] = original.favorited
    if original.place != None:
        tweet['place'] = original.place.full_name
    else:
        tweet['place'] = None
    tweet['retweeted'] = original.retweeted
    tweet['retweetCount'] = original.retweet_count
    tweet['source'] = original.source
    return tweet

# fotten from http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
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

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

#start getfeatureVector
def getFeatureVector(tweet, stop_words):
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
        if(w in stop_words or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
