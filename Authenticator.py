import tweepy

'''
CLASS: TwitterAuthenticator
-------------------
Authenticates a given session for Twitter. Logs into "antonini3" :)
'''
class TwitterAuthenticator:
    def __init__(self):
        # access token owners here is LBronner
        consumer_key = 'OnbNyAnpA1C7W6fOMw1GgUkva'
        consumer_secret = 'BmZdMP2HJcDX0BneJxumHgOj7A8l6UbfKiybV40FUqURl4XOdx'
        access_token = '21001149-R7oOHcOUDW6qyjhEbP2lNRlXEidF2K90Ky9GCAAb3'
        access_token_secret = 'Oinb7yjzbi1cRuy8rrYckfZP49ebjj5aqx3phVQrVL7wZ'

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        # API is main communicator with twitter
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)