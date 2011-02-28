#!/usr/bin/env python

import tweepy

CONSUMER_KEY = 'znpRYzOPEBCV0Iwu3Tgqnw'
CONSUMER_SECRET = 'dKlQCVaoYUKSmBGyTQahWtxA0OvzP3kiZJ3Vxi8rY'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth_url = auth.get_authorization_url()
print 'Please authorize: ' + auth_url
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
print "ACCESS_KEY = '%s'" % auth.access_token.key

#232191328-TRUz7RgA4POW77dUUMSAviBRmrIUMtGjYyUWmstM
