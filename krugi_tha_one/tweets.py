#!/usr/bin/env python

import sys
import tweepy
import urllib2, random
from BeautifulSoup import BeautifulSoup
from tweepy.error import TweepError
from krugi_constants import *

def get_tweet_lines():
    res = urllib2.urlopen(THA_LINK)
    soup = BeautifulSoup(res.read())
    krugi_file = soup.find('a', title='krugi.txt')['href']
    lines = urllib2.urlopen(krugi_file).read().split('\n')
    tweets = []
    for l in lines:
        if len(l) >1 and l[0] != '#':
            tweets.append(l)

    return tweets

def get_me_a_tweet(tweets):
    tweet = tweets[random.randint(0,len(tweets)-1)]
    if len(tweet) > 140:
        return tweet[0:140]
    else: 
        return tweet

def send_tweet():
    tweets = get_tweet_lines()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    c = 0
    while(c<20):
        c = c + 1
        try:
            api.update_status(get_me_a_tweet(tweets))
            break;
        except TweepError:
            pass

if __name__ == '__main__':
    send_tweet()


