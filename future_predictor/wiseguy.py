#!/usr/bin/env python

import sys
from predictor_constants import *

def get_tweet_lines():
    f = open(TWEET_FILE,'r')
    tweets = []
    for line in f:
        tweets.append(line)
        print(line)
    f.close()
    return tweets

def save_tweet_lines(tweets):
    f = open(TWEET_FILE,'w')
    s = ""
    for a in tweets:
        s += a
    f.write(s)
    f.close()

def get_me_a_tweet():
    tweets = get_tweet_lines()
    tweet = get_me_one_tweet(tweets)
    save_tweet_lines(tweets)
    return tweet
	
def get_me_one_tweet(tweets):
    usage = 99
    idx = -1
    selected_idx = -1
    tweet = ''
    for t in tweets:
        idx = idx+1
        if len(t.split(MAIN_SPLITER)) == 2 and int(t.split(MAIN_SPLITER)[0]) < usage:
            print("new lowest used tweet @ "+str(idx))
            usage = int(t.split(MAIN_SPLITER)[0])
            tweet = str(t.split(MAIN_SPLITER)[1])
            selected_idx = idx
    if selected_idx >= 0:
        upcount = str(usage+1)+MAIN_SPLITER+tweet
        print("upcount "+upcount+" at "+str(selected_idx));
        tweets[selected_idx] = upcount
        save_tweet_lines(tweets)
        return tweet
    return "no tweet found"
"""
def send_tweet():
    tweets = get_tweet_lines()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    c = 0
    while(c<20):
        c = c + 1
        try:
            api.update_status(get_me_one_tweet(tweets))
            break;
        except TweepError:
            pass

if __name__ == '__main__':
    send_tweet()
"""

