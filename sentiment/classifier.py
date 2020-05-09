import pandas
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


def pre_processing(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())


# enter the json file path, saved model path
def sentiment_classification(data_path, model_path):
    raw_data = pandas.read_json(data_path, encoding="ISO-8859-1", orient='records', lines=True)
    unique_data = raw_data.drop_duplicates('text')
    pro_list = []
    for tweet in unique_data['text'][:]:
        clean_tweet = pre_processing(tweet)
        pro_list.append(clean_tweet)
    pre_data = pandas.Series(pro_list[:])

    vector = TfidfVectorizer(ngram_range=(1, 3), max_features=400)
    v_data = vector.fit_transform(pre_data)

    with open(model_path, 'rb') as f:
        clf = pickle.load(f)

    # numpy.ndarray
    prediction = clf.predict(v_data)

    return prediction


if __name__ == '__main__':
    data_path = '/Users/yby/PycharmProjects/topic/trump_data1.json'
    model_path = '/Users/yby/PycharmProjects/topic/model200.pickle'
    sc = sentiment_classification(data_path, model_path)
    # 0 = negative 4 = positive
    print(sc.shape)
    print(sc)