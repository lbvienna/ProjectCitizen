import codecs, os
import Authenticator

class Communicator:
    def __init__(self, file_name):
        self.twitterAuth = Authenticator()
        self.file = codecs.open(os.getcwd() + '/database/' + file_name, 'wb', 'utf-8')
        self.file_name = file_name

    def open_channel(self, query, language, locations):
        twitterAuth = self.twitterAuth
