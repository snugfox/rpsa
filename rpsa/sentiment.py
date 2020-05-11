from argparse import ArgumentParser
from nltk import corpus, stem, tokenize
import numpy as np
import pandas as pd
import pickle
import re
from sklearn import feature_extraction, svm
import tweepy

from typing import Iterable, List

from upstream import fetch_sample


class TfidfClassifier(object):
    stemmer = stem.PorterStemmer()
    stopwords = corpus.stopwords.words("english")

    def __init__(self):
        super(TfidfClassifier, self).__init__()
        self.words = set()
        self.vectorizer = feature_extraction.text.TfidfVectorizer(ngram_range=(1, 2))
        self.classifier = svm.SVC()

    def save(self, filename: str):
        state_dict = {
            "words": self.words,
            "vectorizer": self.vectorizer,
            "classifier": self.classifier,
        }
        with open(filename, "wb") as f:
            pickle.dump(state_dict, f)

    def load(self, filename: str):
        state_dict = None
        with open(filename, "rb") as f:
            state_dict = pickle.load(f)
        self.words = state_dict["words"]
        self.vectorizer = state_dict["vectorizer"]
        self.classifier = state_dict["classifier"]

    def preprocess(self, texts: Iterable[str]) -> List[str]:
        re_del = r"(http\S+)|([@#]\S+)"
        clean_texts = []
        for text in texts:
            text = re.sub(re_del, "", text)
            text_tok = tokenize.word_tokenize(text)
            clean_tok = []
            for tok in text_tok:
                tok = tok.lower()
                if tok not in self.stopwords:
                    tok_stem = self.stemmer.stem(tok)
                    if tok_stem in self.words:
                        clean_tok.append(tok_stem)
            clean_texts.append(" ".join(clean_tok))
        return clean_texts

    def train(self, texts: Iterable[str], sents_true: np.ndarray):
        self.words = set()
        for word in corpus.words.words():
            self.words.add(self.stemmer.stem(word.lower()))

        texts_clean = self.preprocess(texts)
        texts_emb = self.vectorizer.fit_transform(texts_clean)
        self.classifier.fit(texts_emb, sents_true)
        sents_pref = self.classifier.predict(texts_emb)

    def test(self, texts: Iterable[str]) -> np.ndarray:
        texts_clean = self.preprocess(texts)
        texts_emb = self.vectorizer.transform(texts_clean)
        sents_pred = self.classifier.predict(texts_emb)
        return sents_pred


if __name__ == "__main__":
    parser = ArgumentParser()
    args = parser.parse_args()

    cl = TfidfClassifier()
    texts = []
    sentiment = []
    for tweet in corpus.twitter_samples.strings("positive_tweets.json"):
        texts.append(tweet)
        sentiment.append(1)
    for tweet in corpus.twitter_samples.strings("negative_tweets.json"):
        texts.append(tweet)
        sentiment.append(-1)
    cl.train(texts, np.array(sentiment))
    cl.save("model/tfidf-svc.pkl")
