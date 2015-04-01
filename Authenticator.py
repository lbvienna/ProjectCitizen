import tweepy

'''
CLASS: Authenticator
-------------------
Authenticates a given session for Twitter. Logs into "antonini3" :)
'''
class Authenticator:
    def __init__(self):
        consumer_key = 'pLrNhYtZ1fejZp6ieXBESWdL3'
        consumer_secret = 'nM3VY8IPdhezYwYXFH7u2EcWFVCwg4a3U0PXlsp0GUF2pn94mH'
        access_token = '21001149-wyjVaXQFOdvbbK8ok70X9wu5zinilSnRojaoFtBI9'
        access_token_secret = 'LyxbkfaxKIuU8K1TfrPWF8BvOSoeRzUr1aUIs0n1fjQkH'

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        # API is main communicator with twitter
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)