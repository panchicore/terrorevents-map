import json

import tweepy
from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from models import Tweet


def get_tweets():
    """

    :return:
    """
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name="TerrorEvents", count=200)
    return tweets


def save_tweets():
    """

    :return:
    """
    tweets = get_tweets()
    for tweet in tweets:
        t = Tweet()
        t.id = tweet.id
        if not t.exists():
            t.date = tweet.created_at
            t.text = tweet.text
            t.user = tweet.user.screen_name
            t.raw_tweet = json.dumps(tweet._json)
            t.save()
            print "saving", t.id