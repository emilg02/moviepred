import tweepy
from django.http import HttpResponse
from textblob import TextBlob
import json

def get_sentiment(request):

    CONSUMER_KEY = "bip84Du8oeaGwSQbcFqcUvM0I"
    CONSUMER_SECRET = "MCI8PB0p9S5IJniK8WbNEbJWWnwelMM3DdnEY7HXEeUswPCK8W"
    ACCESS_TOKEN = "571056457-lTOTfs9dRJ4y1oastQhHvyOi0cFCghQWyhqqwG8f"
    ACCESS_TOKEN_SECRET = "EGEjE6UOZhanIycpex3wbybNJl9Bd29aZAXHvvzeVKiTh"
    NUMBER_OF_TWEETS = 10
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    sentimentlist = []
    number = NUMBER_OF_TWEETS
    query = request.GET['movie'] + "-filet:retweets";
    tweets = tweepy.Cursor(api.search, q=query,lang='en').items(number)
    for index, tweet in enumerate(tweets):
        print (tweet.text)
        analysis = TextBlob(tweet.text).sentiment
        sentimentlist.append(analysis.polarity)
    sentimentavg = float(sum(sentimentlist) / max(len(sentimentlist), 1))
    return HttpResponse(json.dumps(sentimentavg), content_type="application/json")