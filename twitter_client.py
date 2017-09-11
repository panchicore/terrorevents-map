import tweepy
import nlp_client
from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET

def get_twitts():
    """

    :return:
    """
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name="TerrorEvents", count=200)
    return tweets




tweets = get_twitts()
for tweet in tweets:
    # print tweet.created_at, tweet.text
    text = tweet.text.replace("#", "")

    locations = nlp_client.get_locations(text.encode('utf-8'))
    if locations:
        print text
        print locations
        print "-"
