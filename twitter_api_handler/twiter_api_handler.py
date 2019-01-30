import tweepy
from tweepy import Stream

from twitter_api_handler.stream_listener import TwitterStreamListener
from twitter_api_handler.twiter_api_handler_conf import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


class TwitterAPIHandler:
    """This class responsible for any twitter API calls"""

    def __init__(self):
        self.auth = self.authenticate()

    def authenticate(self):
        """
        This method authenticate with the API
        :return: authenticated object
        """

        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth

    def stream_term(self, term, time_frame):
        """
        This method listen to twitter stream
        :param time_frame: time frame
        :param term: The term to listen
        :return: hashtags which are linked to the keyword
        """

        stream_listener = TwitterStreamListener(self.auth, time_frame)
        stream = Stream(self.auth, stream_listener)
        hashtags_dict = stream.filter(track=term, languages=['en'])
        return hashtags_dict
