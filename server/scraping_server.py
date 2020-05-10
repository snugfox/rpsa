# This is Main function.
# Extracting streaming data from Twitter, pre-processing, and send to trained model.

from nltk.corpus import stopwords
import tweepy
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import time
import json
from flask import Flask,request, jsonify
from collections import Counter


def clean_tweet(text):
    '''
    clean tweet text
    '''
    return re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \
                                |(\w+:\/\/\S+)", " ", text)

def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None

def pre_processing(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())


def sentiment_classification(data):
    # raw_data = pandas.read_json(data_path, encoding="ISO-8859-1", orient='records', lines=True)
    # data_list = json.loads(data)
    # raw_data = json_normalize(data_list)
    term_dict = {}
    en_stops = set(stopwords.words('english'))

    raw_data = data
    unique_data = raw_data.drop_duplicates('text')

    pro_list = []
    for tweet in unique_data['text'][:]:
        clean_tweet = pre_processing(tweet)
        pro_list.append(clean_tweet)
    pre_data = pd.Series(pro_list[:])

    vector = TfidfVectorizer(ngram_range=(1, 3), max_features=400,stop_words='english')
    v_data = vector.fit_transform(pre_data)

    clf = pickle.load(open('model20000.pickle', 'rb'))

    # numpy.ndarray
    prediction = clf.predict(v_data)
    p = pd.Series(prediction)
    predicted_tweet = pd.DataFrame({'polarity': p, 'tweet': pre_data})

    all_text_string = ''
    for i in predicted_tweet['tweet'][:]:
        all_text_string += i
    words = [w
             for w in all_text_string.split()
             if w not in en_stops
             if len(w) > 1]
    for item in [words]:
        words_count = Counter(item)
    #  choose the term by edit words_count.most_common()[here :）]
    word_num = words_count.most_common()[22]
    chosen_word = word_num[0]
    chosen_word_num = word_num[1]
    all_word_num = len((set(list(words_count.elements()))))
    popularity = chosen_word_num / all_word_num

    judge = ''
    for_average = predicted_tweet.loc[predicted_tweet['tweet'].str.contains(chosen_word)]
    average_polarity = np.sum(for_average['polarity']) / for_average['polarity'].shape[0]
    if average_polarity > 2:
        judge = 'positive'
    else:
        judge = 'negative'
    # print(judge)

    term_dict = {'term': chosen_word, 'popularity': popularity, 'sentiment': judge}

    return term_dict


def stream(track_words):
    """
    Streaming With Tweepy
    :param track_words: search words from front page
    :return: results of sentiment analysis(dict)
    """
    track_words = str(track_words)
    consumer_key = 'eVXXvtiI6zOFyh28fqlBaLhFG'
    consumer_secret = 'kp5GKGF3leHagSo8J0eLVUICsLfaI76MzjGwkjtLMrPM0jK8EL'
    access_token = '905838785778380801-xE6cTpYspRPpNCNz7dhR7iE6akfuSkn'
    access_token_secret = 'aSF81IzlsesueB9S0BncfMOCU4CnKJ8XzgyNG2WToQOFp'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    hashmap = {'id':[],'id_str':[],'created_at':[],'text':[]}  # store
    i = 0
    # start = time.time()
    for tweet in tweepy.Cursor(api.search, q=track_words, count=100, lang='en',retweeted=False,wait_on_rate_limit=True).items(1000):
        id = tweet.id
        id_str = tweet.id_str
        created_at = str(tweet.created_at) # create time
        text = clean_tweet(tweet.text)  # preprocessing
        finalText = deEmojify(text)

        hashmap['id'].append(id)
        hashmap['id_str'].append(id_str)
        hashmap['created_at'].append(created_at)
        hashmap['text'].append(finalText)

        i += 1
        # end = time.time()
        # collect 200 tweets for every call
        if i == 200:
           break
        else:
            continue

    df = pd.DataFrame(hashmap)
    output = sentiment_classification(df)
    return output






