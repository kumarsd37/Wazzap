import tweepy
import threading
import psycopg2
import re
import parsedatetime
import secrets


def authorize():
    """
    Use OAuth to setup access token for the app.
    """
    auth = tweepy.OAuthHandler(
        secrets.tweepy_consumer_key,
        secrets.tweepy_consumer_secret
    )
    auth.set_access_token(
        secrets.access_token,
        secrets.access_secret
    )

    return tweepy.API(auth)


def fetch_related_statuses(api, name, how_many_tweets=25):
    """
    Return a list of (user name, related tweet content).
    """
    pass


def write_data(tweets_list):
    with open('tweets.txt') as f:
        f.write(tweets_list)


def fetch_user_statuses(api, target_twitter_handle=None, reference=0, how_many_tweets=50):
    """
    Return a list of (user name, content, tweet time(gmt)).
    """
    content = []
    # If no twitter handle, do not run
    if target_twitter_handle:
        tweets = api.user_timeline(screen_name=target_twitter_handle, count=how_many_tweets)
        # parser = parsedatetime.Calendar()
        for tweet in tweets:
            parser = parsedatetime.Calendar()
            try:
                if parser.parse(tweet.text)[1]: 
                    # If retweeted, a tweet begins with 'RT @name:'
                    if tweet.text.startswith(u'RT @'):
                        author = re.compile(r'RT @\S+:').match(tweet.text).group()[4:-1]
                    else:
                        author = target_twitter_handle  # Venue twitter handle

                    content.append(
                        [reference, author, tweet.text.encode('utf-8'), tweet.created_at, 1, tweet.id_str]
                    )
            except KeyError:
                pass

        # else continue 
    return content
