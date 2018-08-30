"""
Script to write data from @dog_rates to file.
"""
import csv
import datetime

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Tweet(Base):
    __tablename__ = "tweet"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    account = sqlalchemy.Column(sqlalchemy.String(250))
    collected_at = sqlalchemy.Column(sqlalchemy.DateTime)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime)
    id_str = sqlalchemy.Column(sqlalchemy.String(250))
    full_text = sqlalchemy.Column(sqlalchemy.String(1000))
    favourite_count = sqlalchemy.Column(sqlalchemy.Integer)
    retweet_count = sqlalchemy.Column(sqlalchemy.Integer)
    follower_count = sqlalchemy.Column(sqlalchemy.Integer)

def main(session, account, api):
    """
    Get all tweets from account and write to an sql session
    """
    user = api.get_user(account)
    follower_count = user.followers_count

    for tweet in tweepy.Cursor(api.user_timeline,
                               tweet_mode="extended",
                               screen_name=account).items():
        now = datetime.datetime.now()

        tweet = Tweet(account=account,
                      collected_at=now,
                      created_at=tweet.created_at,
                      id_str=tweet.id_str,
                      full_text=tweet.full_text,
                      favourite_count=tweet.favorite_count,
                      retweet_count=tweet.retweet_count,
                      follower_count=follower_count)
        session.add(tweet)

    session.commit()

if __name__ == "__main__":
    import tweepy

    from secrets import *

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    engine = sqlalchemy.create_engine('sqlite:///main.sqlite3')
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
    session = DBSession()

    for account in ("@dog_rates",  "@dog_feelings", "@matt___nelson"):
        main(session=session, account=account, api=api)
