"""
Script to write data from @dog_rates to file.
"""
import csv
import datetime

def main(datafile_path, account, api):
    """
    Get all tweets from account and write to a given file.
    """

    with open(datafile_path, "a") as f:
        csv_writer = csv.writer(f)
        
        user = api.get_user(account)
        follower_count = user.followers_count

        for tweet in tweepy.Cursor(api.user_timeline, 
                                   tweet_mode="extended", 
                                   screen_name=account).items():
            now = str(datetime.datetime.now())

            csv_writer.writerow([account,
                                 now,
                                 tweet.created_at, 
                                 tweet.id_str,
                                 tweet.full_text, 
                                 tweet.favorite_count, 
                                 tweet.retweet_count,
                                 follower_count])

if __name__ == "__main__":
    import tweepy

    from secrets import *

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    datafile_path = "./main.csv"

    for account in ("@dog_rates",  "@dog_feelings", "@matt___nelson"):
        main(datafile_path=datafile_path,
             account=account,
             api=api)
