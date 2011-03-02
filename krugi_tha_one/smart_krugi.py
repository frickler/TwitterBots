#!/usr/bin/env python
# -*- coding: utf-8 -*-

from krugi_constants import *
import tweepy, time, pickle, wolframalpha, random, sys, traceback

WHITELIST = ['flurischt','steffstefferson','webair84','krigu_tha_one', 'buergich']
OWN_NAME = 'krugi_tha_one'
PICKLE_FILE = 'data.pkl'
COUNTER_QUESTIONS = [ 'I\'m not sure what you mean...', 'Is this rhetorical?', 'yes', 'nope', 'Do YOU know this?', 'what????', 'haha, this is too easy for me...', 'How should I know that?? I\'m not IBM\'s Watson!' ]

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

    def listen(self, api):
        last_id = self.recover()
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
        print 'got a message from @' + username + ':', status.text
        if username != OWN_NAME and username in WHITELIST:
            text = status.text.lower().replace('@'+OWN_NAME,'')
            
            # ask wolfram
            query = wolframalpha.WolframAlpha(text)
            
            if len(query.results) >= 2:
                answer = query.results[1].result_raw.replace('Wolfram|Alpha',OWN_NAME)
            else:
                if '?' in status.text:
                    if 'clothes' in status.text:
                        answer = 'me julie went shopping for me... http://www.youtube.com/watch?v=JB6YL1ko8_s'
                    else:
                        answer = COUNTER_QUESTIONS[random.randint(0,len(COUNTER_QUESTIONS)-1)]
                else:
                    if 'funny' in status.text or 'brilliant' in status.text or 'intelligent' in status.text or 'smart' in status.text:
                        answer = 'thank you!'
                    else:
                        answer = 'Check your spelling, and use English!! (Errcode ' + str(random.randint(0,10000)) + ')'

            self.reply(status,answer)


    def reply(self,status,answer):
        message = '@'+status.user.screen_name+' '+answer
        message.replace('\n', ' ')
        if len(message) > 140:
            message = message[0:139]
            print message
        try:
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
        print 'bye!'
