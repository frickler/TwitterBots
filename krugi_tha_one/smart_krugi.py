#!/usr/bin/env python
# -*- coding: utf-8 -*-

from krugi_constants import *
import tweepy, time, pickle, wolframalpha, random, sys, traceback

## SETTINGS ##
OWN_NAME = 'krugi_tha_one'
THE_OWNER = 'flurischt'
PICKLE_FILE = 'data.pkl'
DEBUG = True

## some phrases that are matched by keyword ##
KEYWORD_PHRASES = [
    ( 'clothes', 'me julie went shopping for me... http://www.youtube.com/watch?v=JB6YL1ko8_s' ),
    ( 'brilliant', 'thank you!' ),
    ( 'intelligent', 'yeah, thanks!' ),
    ( 'smart', 'thx!' )
]

## possible answers to a question ##
COUNTER_QUESTIONS = [ 
    'I\'m not sure what you mean...', 
    'Is this rhetorical?', 
    'yes', 
    'nope', 
    'do YOU know this?', 
    'what????', 
    'haha, this is too easy for me...', 
    'How should I know that?? I\'m not IBM\'s Watson!', 
    'only @flurischt could answer this! ;-)' 
]

## random answers if everything else failed ##
RANDOM_PHRASES = [ 'shut up!', 'Check your spelling, and use English!!' ]

## the following keywords will always be hidden in krugis answer ##
HIDE = [
    ( 'Wolfram|Alpha', OWN_NAME ),
    ( 'Stephen Wolfram', 'a frickler' ),
]

def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)
    
class Smart_Krugi():

    def __init__(self, api):
        self.api = api
        self.refresh_whitelist()

    def refresh_whitelist(self):
        self.WHITELIST = ['flurischt','steffstefferson','webair84','krigu_tha_one', 'buergich']

    def listen(self, api):
        last_id = self.recover()
        print 'DEBUG: %s' % DEBUG
        print 'recovered:', last_id
        while(True):
            if last_id:
                tweets = api.mentions(last_id)
            else:
                tweets = api.mentions()
            for t in tweets:
                self.process(t)
                last_id = t.id
            
            self.backup(last_id)
            # at maximum 350 requests per hour !!!
            time.sleep(30)

    def recover(self):
        pkl_file = open(PICKLE_FILE, 'rb')
        id = pickle.load(pkl_file)
        pkl_file.close()
        return id

    def backup(self, last_id):
        if not last_id:
            return
        output = open(PICKLE_FILE, 'wb')
        pickle.dump(last_id, output)
        output.close()

    def process(self, status):
        username = status.user.screen_name.lower()
        print 'got a message from @%s : %s' % (username,status.text)
        if username != OWN_NAME and username in self.WHITELIST:
            text = status.text.lower().replace('@'+OWN_NAME,'')
            
            # ask wolfram
            answer = None
            query = wolframalpha.WolframAlpha(text)
                       
            if len(query.results) >= 2:
                answer = query.results[1].result_raw
            else:
                # wolfram had no idea...
                for (k,v) in KEYWORD_PHRASES:
                    if k in text:
                        answer = v
                        break

                if not answer and '?' in text:
                    answer = COUNTER_QUESTIONS[random.randint(0,len(COUNTER_QUESTIONS)-1)]
                else:
                    answer = '%s (Errcode %i)' % (RANDOM_PHRASES[random.randint(0,len(RANDOM_PHRASES)-1)], random.randint(0,10000))

            self.reply(status,answer)

    def process_dbg(self, text):
        user = tweepy.User()
        status = tweepy.Status() 
        user.screen_name = 'flurischt'
        status.id = 99999
        status.text = text
        status.user = user
        self.process(status)

    def reply(self,status,answer):
        # remove the "forbidden" keywords 
        for (k,v) in HIDE:
            answer.replace(k, v)
        
        message = '@%s %s' % (status.user.screen_name, answer)

        if len(message) > 140:
            message = message[0:139]
        try:
            if not DEBUG:
                self.api.update_status(message,status.id)
            print message
        except tweepy.TweepError:
            print formatExceptionInfo()

if __name__ == '__main__':
    # dirty workaraound for the unicode problems
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    smart = Smart_Krugi(api)

    try:
        smart.listen(api)
    except KeyboardInterrupt:
        print '\nbye!'
