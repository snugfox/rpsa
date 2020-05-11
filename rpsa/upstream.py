import pandas as pd
import tweepy
from typing import List


def fetch_sample(screen_names: List[str], size: int = 100):
    consumer_key = "eVXXvtiI6zOFyh28fqlBaLhFG"
    consumer_secret = "kp5GKGF3leHagSo8J0eLVUICsLfaI76MzjGwkjtLMrPM0jK8EL"
    access_token = "905838785778380801-xE6cTpYspRPpNCNz7dhR7iE6akfuSkn"
    access_token_secret = "aSF81IzlsesueB9S0BncfMOCU4CnKJ8XzgyNG2WToQOFp"

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
