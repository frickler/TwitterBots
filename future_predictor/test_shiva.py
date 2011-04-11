#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tests the shiva bot in debug mode.
USAGE: python test_shiva.py "message"
"""

from predictor_constants import *
import tweepy, time, pickle, random, sys, traceback, sys
from smart_predictor import Smart_Predictor


if __name__ == '__main__':
    # dirty workaround for the unicode problems
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    smart = Smart_Predictor(api, True)
    smart.process_dbg(sys.argv[1])
