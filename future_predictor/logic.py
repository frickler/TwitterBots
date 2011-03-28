#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import answer
import storage
import random
import time
import json

def getInt(strin,defaultint):
    try:
        number = int(strin)
    except (ValueError, IndexError):
        number = defaultint
    return number    

class logic:
    answers = []
    datastore = None
    def __init__(self):
        self.answers = []
        self.datastore = storage.storage()
        self.answers = self.datastore.getanswers()
    def getanswer(self,question):      
        return self.getanswername(question,"")

    def getwochentendenz(self):
        idx = time.strftime("%w")
        idx = int(idx)
        wkdays = ["Mo","Di","Mi","Do","Fr","Sa","So","Mo","Di","Mi","Do","Fr","Sa","So"]
        arry = []
        sreturn = "Deine Wochentendenz: \n"
        basestars = random.randint(0,7)
        for i in range(idx+1, idx+7):
            sreturn += wkdays[i]+" "
            basestars = random.randint(0,4)-2+basestars
            if random.randint(0,4)-2+basestars < 0:
                basestars = 1
            if random.randint(0,4)-2+basestars > 7:
                basestars = 6    
            for v in range(0, basestars):
                sreturn += "*"
            sreturn += "\n"
        return sreturn
            
    def getschicksalsjahre(self,text):
        month = "1"
        year = "2000"
        day = "1"
        if len(text.split('.')) == 3:
            day = text.split('.')[0]
            month =text.split('.')[1]
            year = text.split('.')[2]
        elif len(text.split(' ')) == 3:
            day = text.split(' ')[0].replace(".","")
            month = text.split(' ')[1].replace(".","")
            year = text.split(' ')[2].replace(".","")
        elif(len(text) >= 3):
            day = text[0]
            month = text[1]
            year = text[2]    
        
        arry = []
        arry.append(2012 + getInt(day,3))
        arry.append(2000 + getInt(month,4))
        arry.append(2015 * getInt(month,7) / getInt(year,2012))
        arry.append(1920 + getInt(month,4) * getInt(day,12))
        
        for i in range(0, len(arry)):
            print(arry[i])
            while(arry[i] < 2012):
                arry[i] = arry[i] + 7
            while(arry[i] > 2050):
                arry[i] = arry[i] - 4
        
        arry.sort()
        
        for i in range(0, len(arry)-1):
            if round(arry[i]) > round(arry[i+1]-2):
                arry[i+1] = arry[i+1]+3+i
        
        return "Deine Schicksalsjahre sind"+" "+str(int(arry[0]))+" "+str(int(arry[1]))+" "+str(int(arry[2]))+" "+str(int(arry[3]));
        
        
    def getanswername(self,question,questioner):
        if(len(self.answers) == 0):        
            self.answers = datastore.getanswers()
            
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

    def saveanswerstofile(self):
        if(self.datastore != None and len(self.answers) > 0):
            self.datastore.saveanswerstofile(self.answers)
            print('saved')
