from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from configurations import COUNT, KEYWORD, LAST_APPEARANCE_DATE


class HashTagManager:
    """This class implementing the data analyzing"""

    def __init__(self, time_frame=7):
        self.hashtag_dict = {}
        self.time_frame = time_frame
        self.fig = plt.figure()
        self.plot = self.fig.add_subplot(1, 1, 1)

    def update_data_source(self, new_hashtags):
        """
        This method updates the data source
        :param new_hashtags: new hastags dict
        """

        for hashtag in new_hashtags:
            hashtag_key = list(hashtag.keys())[0]
            # if an existing hashtag update the count and the last appearance
            if hashtag_key in self.hashtag_dict:
                self.hashtag_dict[hashtag_key][COUNT] = self.hashtag_dict[hashtag_key][COUNT] + 1
                self.hashtag_dict[hashtag_key][LAST_APPEARANCE_DATE] = hashtag[hashtag_key][LAST_APPEARANCE_DATE]
            # else add a new hashtag to the dict
            else:
                self.hashtag_dict.update(hashtag)
                self.hashtag_dict[hashtag_key][COUNT] = 1
                self.hashtag_dict[hashtag_key][KEYWORD] = hashtag_key

        if self.hashtag_dict:
            hashtags_df = pd.DataFrame(self.hashtag_dict.values())
            hashtags_df = hashtags_df.set_index(hashtags_df[KEYWORD])

            # filter old hashtags
            is_old_hashtag = (hashtags_df[LAST_APPEARANCE_DATE].map(
                lambda day: (datetime.now() - day).days > self.time_frame))
            hashtags_df = hashtags_df[~is_old_hashtag]
            self.hashtag_dict = hashtags_df.to_dict(orient='index')

            # sort by count and relevancy and take the top 10
            hashtags_df = hashtags_df.sort_values(by=[COUNT, LAST_APPEARANCE_DATE], ascending=False)[:10]

            self.plot.clear()
            self.plot.barh(hashtags_df[KEYWORD], hashtags_df[COUNT])
            plt.draw()
            plt.pause(0.001)
