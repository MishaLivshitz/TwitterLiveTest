import json
from datetime import datetime
from time import sleep

import matplotlib.pyplot as plt
from tweepy import StreamListener

from main_package.configurations import HASHTAGS, ENTITIES, TIMESTAMP, TEXT, LAST_APPEARANCE_DATE
from hashtags_manager.hashtag_manager import HashTagManager
from twitter_api_handler.twiter_api_handler_conf import REACHED_API_CALLS_LIMIT_ERROR


class TwitterStreamListener(StreamListener):
    """This is a twitter stream listener"""

    def __init__(self, auth, time_frame):
        super().__init__()
        self.hashtag_manager = HashTagManager(time_frame)
        self.api_auth = auth

    def on_data(self, data):
        """
        This method fires when a tweet received
        :param data: data received
        :return: dict of {hashtag_text:date}
        """

        if data:
            received_data = json.loads(data)
            if ENTITIES in received_data and received_data[ENTITIES][HASHTAGS]:
                creation_date = datetime.fromtimestamp(int(received_data[TIMESTAMP]) / 1000)
                hashtag_dict = [{hashtag[TEXT].lower(): {LAST_APPEARANCE_DATE: creation_date}} for hashtag in
                                received_data[ENTITIES][HASHTAGS]]
                plt.ion()
                plt.show()
                self.hashtag_manager.update_data_source(hashtag_dict)

    def on_error(self, status):

        if status == REACHED_API_CALLS_LIMIT_ERROR:
            print("Sleeping for 15 minutes due to limit reaching of api calls")
            sleep(15 * 60)
