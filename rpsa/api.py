from collections import Counter
from datetime import datetime, timezone
import pandas as pd
from threading import Event

from typing import Iterable

from sentiment import TfidfClassifier
from upstream import fetch_sample


class RPSA(object):
    def __init__(
        self, screen_names: Iterable[str], sample_size: int, model_filename: str
    ):
        super(RPSA, self).__init__()
        self.screen_names = list(screen_names)
        self.sample_size = sample_size
        self.ticker = None
        self.model = TfidfClassifier()
        self.model.load(model_filename)
        self.history = {
            "names": self.screen_names,
            "times": [],
            "sentiment": [[] for _ in self.screen_names],
        }
        self.key_stems = {}

    def update(self):
        self.history["times"].append(datetime.now(tz=timezone.utc).isoformat())
        tweets = fetch_sample(self.screen_names, size=self.sample_size)
        tweet_texts = tweets["text"].tolist()
        tweets["clean"] = self.model.preprocess(tweets["text"].tolist())
        tweets["sentiment"] = self.model.test(tweet_texts)
        for id, name in enumerate(self.screen_names):
            mention_tweets = tweets[tweets["text"].str.contains(name)]
            self.history["sentiment"][id].append(
                mention_tweets["sentiment"].mean() if len(mention_tweets) > 0 else 0.0
            )
            all_stems = " ".join(mention_tweets["clean"].tolist()).split(" ")
            stem_count = Counter(all_stems)
            key_stems = []
            for stem, count in stem_count.most_common(5):
                key_stems.append(
                    {
                        "term": stem,
                        "popularity": count / len(all_stems),
                        "sentiment": 1
                        if mention_tweets[mention_tweets["clean"].str.contains(stem)][
                            "sentiment"
                        ].mean()
                        >= 0
                        else 0,
                    }
                )
            self.key_stems[str(id)] = key_stems

    def run(self, interval: float):
        self.ticker = Event()
        while not self.ticker.wait(interval):
            self.update()

    def candidates(self):
        return [
            {"name": f"@{name}", "id": id} for id, name in enumerate(self.screen_names)
        ]

    def sentiment(self):
        return self.history

    def terms(self):
        return self.key_stems
