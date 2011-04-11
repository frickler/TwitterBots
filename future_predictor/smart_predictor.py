#!/usr/bin/env python
# -*- coding: utf-8 -*-

from predictor_constants import *
import tweepy, time, pickle, random, sys, traceback
import logic
import storage


## SETTINGS ##
PICKLE_FILE = 'data.pkl'
DEBUG = True


def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)
    
class Smart_Predictor():

    def __init__(self, api, debug):
        self.api = api
        self.refresh_whitelist()
        self.predictorlogic = logic.logic()
        self.debug = debug


    def refresh_whitelist(self):
        self.WHITELIST = self.api.friends_ids()

    def listen(self, api):
        last_id = self.recover()
        print 'DEBUG: %s' % self.debug
        print 'recovered:', last_id
        i = 0
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

            if i % 50 == 0:
                self.refresh_whitelist()
            i += 1

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
        user = status.user
        print 'got a message from @%s : %s' % (user.screen_name,status.text)
        if user.screen_name.lower() != OWN_NAME:
        
            #to get popular follow the questionasker:
            try:

                if not self.debug:
                    if not API.exists_friendship(OWN_NAME, user.screen_name):
                        api.create_friendship(user.screen_name)
                        print('I follow now %s' % user.screen_name)
                    else:
                        print 'I follow already this guy: '+user.screen_name
            except tweepy.error.TweepError:
                print('cannot follow %s' % user.screen_name)
                
            #tweeted question is:
            text = status.text.lower().replace('@'+OWN_NAME,'')
            print 'asked question '+text
            #want to now the schicksalsjahre
            if 'schicksalsjahre' in text or 'schicksalsjahr' in text:
                sdatum = text.replace('Schicksalsjahre','').replace(" ","").replace("<","").replace(">","")
                if len(sdatum) < 6:
                    self.reply(status,'Du hast dein Geburtsdatum vergessen')
                    return
                self.reply(status,self.predictorlogic.getschicksalsjahre(sdatum))
                return
            if 'wochentendenz' in text:
                self.reply(status,self.predictorlogic.getwochentendenz())
                return
                
            if 'tageswerte' in text:
                sternzeichen = text.replace('Tageswerte','').replace(" ","").replace("<","").replace(">","")
                if len(sternzeichen) < 3:
                    self.reply(status,'Sag mir auch dein Sternzeichen.')
                    return
                self.reply(status,self.predictorlogic.gettageswerte(sternzeichen))
                return  
            
            if 'tageshoroskop' in text:
                sternzeichen = text.replace('tageshoroskop','').replace(" ","").replace("<","").replace(">","")
                if len(sternzeichen) < 3:
                    self.reply(status,'Sag mir auch dein Sternzeichen.')
                    return
                self.reply(status,self.predictorlogic.gettageshoroskop(sternzeichen))
                return
                
            #get an answer
            answer = self.predictorlogic.getanswer(text)
            if len(answer) > 0:
                self.reply(status,answer)


    def process_dbg(self, text):
        user = tweepy.User()
        status = tweepy.Status() 
        user.screen_name = 'flurischt'
        user.id = 999999
        status.id = 99999
        status.text = text
        status.user = user
        self.process(status)

    def reply(self,status,answer):        
        message = '@%s %s' % (status.user.screen_name, answer)
        
        if len(message) == 0:
            print 'no message to return, do not reply'
            return
        
        if len(message) > 140:
            message = message[0:139]
        try:
            if not self.debug:
                self.api.update_status(message,status.id)
            print message
        except tweepy.error.TweepError:
            print formatExceptionInfo()

if __name__ == '__main__':
    # dirty workaround for the unicode problems
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    smart = Smart_Predictor(api, DEBUG)
    try:
        smart.listen(api)
    except KeyboardInterrupt:
        print '\nbye!'
