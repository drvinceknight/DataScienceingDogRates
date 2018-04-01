"""
Script to write data from @dog_rates to file.
"""
import csv
import datetime

import pandas as pd
import tweepy

from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

datafile_path = "./main.csv"
columns = ["collected_at", "created_at", "full_text", "like_count", "retweet_count"]

df = pd.read_csv(datafile_path, header=None, names=columns)
last_tweet_date = pd.to_datetime(df["created_at"]).max()
num_new_tweets = 0

with open(datafile_path, "a") as f:
    csv_writer = csv.writer(f)
    for tweet in tweepy.Cursor(api.user_timeline, 
                               tweet_mode="extended", 
                               screen_name='@dog_rates').items():
        now = str(datetime.datetime.now())
        csv_writer.writerow([now,
                             tweet.created_at, 
                             tweet.full_text, 
                             tweet.favorite_count, 
                             tweet.retweet_count])
        if tweet.created_at > last_tweet_date or last_tweet_date is pd.NaT:
            num_new_tweets += 1
print(f"{now}: {num_new_tweets} new tweets collected since {last_tweet_date}")
