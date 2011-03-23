#!/usr/bin/env python

import sys
import answer
import storage
import random

class logic:
    answers = []
    datastore = None
    def __init__(self):
        self.answers = []
        self.datastore = storage.storage()
        self.answers = self.datastore.gettestanswers()
    def getanswer(self,question):      
        return self.getanswername(question,"")

    def getanswername(self,question,questioner):
        if(len(self.answers) == 0):        
            self.answers = datastore.gettestanswers()
            
        best = None
        for a in self.answers:
            a.keywordsmatch(question)
            if(len(a.keywords)>0 and a.keywordmatch == 0):
                continue
            #       standard answer
            if((best == None and (len(a.keywords)==0 or a.keywordmatch > 0))\
            or (a.getquality() > best.getquality() and a.keywordmatch > 0)\
            or (len(best.keywords)==0 and len(a.keywords)==0 and best.answerused > a.answerused)):
                best = a
        if(best == None):
            return "keine antwort"
        
        best.answerused = best.answerused+1
        text = best.answer
        text = self.replacePlanets(text)
        text = self.replaceCards(text)
        text = self.replaceStarSigns(text)
        text = text.replace("%yourname%",questioner)
        return text

    def replacePlanets(self,text):
        return self.basicReplace(text,"%planet%",self.datastore.getplanets())

    def replaceStarSigns(self,text):
        return self.basicReplace(text,"%starsign%",self.datastore.getstarsgins())
        
    def replaceCards(self,text):
        iEndlessLoop = 0
        if(text.find("%card%")==1):
            return    
        text = text.replace("%card%","%cardC%-%cardN%")
        cards = self.datastore.getcards()
        text = self.basicReplace(text,"%cardC%",cards[0])
        return self.basicReplace(text,"%cardN%",cards[1])

    def basicReplace(self,text,variable,data):
        iEndlessLoop = 0
        while(text.find(variable)>-1):
            iEndlessLoop = iEndlessLoop+1
            randomtext = data[random.randint(0,len(data)-1)]
            if(not(text.find(randomtext)>-1) or iEndlessLoop > len(data)*2):
                text = text.replace(variable,randomtext,1)
        return text
