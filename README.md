# Realtime Political Sentiment Analysis (RPSA)
Realtime Political Sentiment Analysis (RPSA) is a software stack that samples,
predicts, and presents Twitter user sentiment for political candidates in
realtime. There are three key components to the software: the sentiment
classifier, the server backend, and the web interface. Additionally, RPSA is
designed to be easily extensible. The current implementation includes one
sentiment classifier model (based on TF-IDF and SVM); however, anyone can define
a new model with a single Python class.

# Building RPSA
Before you can build RPSA, you must install Node.js, NPM, and Python 3.7 or
later. Then, you must run the following commands:

```console
# Build the WebUI
$ cd rpsa/webui
$ npm install
$ npm run build

# Build the RPSA program
$ cd ../..
$ pip install -Ur requirements.txt
$ python build.py
```

This will create a `dist` folder with all the files needed to host and run RPSA.
To run RPSA, first specify define the following environmental variables
corresponding to a Twitter API OAuth token:
- `TWITTER_CONSUMER_KEY`
- `TWITTER_CONSUMER_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`

Then, you can run the following to serve the WebUI and run RPSA over port 5000
for candidates @realDonaldTrump and @JoeBiden:
```console
$ cd dist
$ python rpsa.py --model model/tfidf-svc.pkl --candidate realDonaldTrump \
    -- candidate JoeBiden
```

For a full list of arguments you can specify, run:
```console
$ python rpsa.py -h
```

# Dataset
The TFIDF-SVC model was trained using the
[Sentiment140](http://help.sentiment140.com/for-students) provided by Stanford.
