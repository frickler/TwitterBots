#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from xgoogle.translate import LanguageDetector, DetectionError, Translator, TranslationError
from krugi_constants import *
import tweepy, time, pickle, wolframalpha

WHITELIST = ['flurischt','steffstefferson']
OWN_NAME = 'krugi_tha_one'
PICKLE_FILE = 'data.pkl'

class Smart_Krugi():

    def __init__(self, api):
        self.api = api
        self.detect = LanguageDetector().detect
        self.translate = Translator().translate

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
            time.sleep(20)

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
        if username != OWN_NAME and username in WHITELIST:
            text = status.text.lower().replace('@'+OWN_NAME,'')
            #lang = self.detect(text)
            #if lang.lang_code != 'en':
            #    text = self.translate(text)

            # ask wolfram
            query = wolframalpha.WolframAlpha(text)
            #for rs in query.results:
            #    if 'result' in rs.title.lower():
                    #self.reply(status,self.translate(rs.result, lang.lang_code))
            if len(query.results) >= 2:
                self.reply(status,query.results[1].result)
                return

            self.reply(status, 'shut up!')

    def reply(self,status,answer):
        try:
            self.api.update_status(answer+' @'+status.user.screen_name,status.id)
        except TweepError:
            pass
        print answer 

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    smart = Smart_Krugi(api)

    try:
        smart.listen(api)
    except KeyboardInterrupt:
        print 'bye!'
