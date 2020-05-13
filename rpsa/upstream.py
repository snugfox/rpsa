import pandas as pd
import tweepy
import os
from typing import List


def fetch_sample(screen_names: List[str], size: int = 100):
    consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    query = " OR ".join(f"@{sn}" for sn in screen_names)
    query += " -filter:retweets"
    api_kwargs = {
        "q": query,
        "lang": "en",
        "result_type": "recent",
        "tweet_mode": "extended",
        "count": min((size, 100)),
    }
    tweets = {
        "id": [],
        "text": [],
    }
    for tweet in tweepy.Cursor(api.search, **api_kwargs).items(size):
        tweets["id"].append(tweet.id)
        tweets["text"].append(tweet.full_text)

    df_dtypes = {"id": "int64", "text": "string"}
    df = pd.DataFrame(tweets)
    df = df.astype(dtype=df_dtypes, copy=False)
    df.set_index("id", inplace=True)
    return df
