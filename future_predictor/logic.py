#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import answer
import storage
import random
import time
import json
import urllib
import string

from predictor_constants import *

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

    def getStars(self,basestars):
        stars = ""
        for v in range(0, basestars):
            stars += "*"
        return stars
        
    def getwochentendenz(self):
        idx = time.strftime("%w")
        idx = int(idx)
        wkdays = ["Mo","Di","Mi","Do","Fr","Sa","So","Mo","Di","Mi","Do","Fr","Sa","So"]
        arry = []
        sreturn = "Deine Wochentendenz:"+NEW_LINE
        basestars = random.randint(0,7)
        for i in range(idx, idx+6):
            sreturn += wkdays[i]+" "
            basestars = random.randint(0,4)-2+basestars
            if random.randint(0,4)-2+basestars < 0:
                basestars = 1
            if random.randint(0,4)-2+basestars > 7:
                basestars = 6    
            sreturn += self.getStars(basestars)
            sreturn += NEW_LINE
        return sreturn
    
    def gettageswerte(self,ssternzeichen):
        sternzeichen = ssternzeichen.lower()
        print "\npredict tageswerte for "+sternzeichen
        count = 0
        for i in range(0,len(sternzeichen)-1):
            count += ord(sternzeichen[i])
        count = count * int(time.strftime("%d"))   + int(time.strftime("%m")) 
        
        sReturn = "Tageswerte für Sternzeichen: "+ssternzeichen+NEW_LINE
        sReturn +=  "Liebe: "+self.getStars((count+10)%7)+NEW_LINE
        sReturn +=  "Glück: "+self.getStars((count*3)%7)+NEW_LINE
        sReturn +=  "Gesundheit: "+self.getStars((count+ord(sternzeichen[2]))%7)+NEW_LINE
        sReturn +=  "Arbeit: "+self.getStars((count+ord(sternzeichen[2])/2)%7)+NEW_LINE
        return sReturn;

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
        
        iMax = random.randint(2,4)
        
        arry.append(2012 + getInt(day,3))
        if iMax > 1:
            arry.append(2000 + getInt(month,4))
        if iMax > 2:
            arry.append(2015 * getInt(month,7) / getInt(year,2012))
        if iMax > 3:
            arry.append(1920 + getInt(month,4) * getInt(day,12))
        
        for i in range(0, len(arry)):
            print(arry[i])
            while(arry[i] < 2012):
                arry[i] = arry[i] + 7
            while(arry[i] > 2050):
                arry[i] = arry[i] - 4
        
        arry.sort()
        
        sReturn = ""
        
        for i in range(0, len(arry)-1):
            if round(arry[i]) > round(arry[i+1]-2):
                arry[i+1] = arry[i+1]+random.randint(1,4)
            sReturn += " "+str(int(arry[i]))
            
        return "Deine Schicksalsjahre sind"+sReturn;
    
    def gettageshoroskop(self,sternzeichen):
        print "input text is "+sternzeichen
        signs = self.datastore.getstarsgins()
        sign = ""
        sternzeichen = sternzeichen.replace(" ","")
        for i in range(0, len(signs)-1):
            if sternzeichen.lower() == signs[i].lower():
                sign = sternzeichen
                print "sign is: "+sign
        if len(sign) == 0:
            print "sign not found"
            #sign = signs[random.randint(0,len(signs)-1)]
            return ""
        url = "http://www.astrowelt.com/horoskop/tag/"+sign
        print "call url: "+url
        f = urllib.urlopen(url)
        s = f.read()
        f.close()

        #achtung hier folgt ein gefrickler von franz frickler
        s = s.replace(NEW_LINE,"")
        start = string.find(s,"<h3 class=\"horoskop\">")
        end = string.find(s,"othersigns")
        s = s[start:end]
        start = string.find(s,"<p>")
        end = string.find(s,"</p>")
        s = s[start+3:end]
        
        i = 0
        while(i < 140):      
            print i
            indexP = s.find(".",i+1)
            if(indexP < 140 and indexP > 0):
                i = indexP
            else:
                break        
        s = s[0:i+1]
        
        return s    
        
    def getanswername(self,question,questioner):
        if(len(self.answers) == 0):        
            self.answers = datastore.getanswers()
            
        best = None
        for a in self.answers:
            a.keywordsmatch(question)
            if(len(a.keywords)>0 and a.keywordmatch == 0):
                #print "not good answer: "+a.tostring()
                continue
            #standard answer
            if(best == None and len(a.keywords)==0 or a.keywordmatch > 0):
                print 'first answer'
                best = a
            #better standard answer
            elif(len(best.keywords) == 0 and len(a.keywords)==0 and best.answerused > a.answerused):
                print 'better standart answer'
                best = a        
            
            elif(best != None and len(best.keywords) == 0 and a.keywordmatch > 0):
                print 'first keywordmatch answer'
                best = a
            elif( len(best.keywords) > 0 and a.getquality() > best.getquality() and a.keywordmatch > 0):
                print 'better keywordmatch answer'
                best = a           

        if(best == None):
            return ""
       
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
    
    def saveUnansweredQuestion(self,text,user):
        if(self.datastore != None):
            self.datastore.saveUnansweredQuestion(text,user)
        
    def saveanswerstofile(self):
        if(self.datastore != None and len(self.answers) > 0):
            self.datastore.saveanswerstofile(self.answers)
            print('saved')

    def updateFiles(self):
        newTweets = urllib.urlopen(TWEETUPDATEFILE)
        fr = open(TWEET_FILE,'a')
        for line in newTweets:
            if line[0:1] != "#" and len(line) > 5:
                fr.write(line)
                print "new tweet added: "+line
        fr.close()
        newTweets.close()
        
        newAnswers = urllib.urlopen(ANSWERUPDATEFILE)
        fa = open(ANSWER_FILE,'a')
        for line in newAnswers:
            if line[0:1] != "#" and len(line) > 5:
                fa.write(line)
                print "new answer added: "+line
        fa.close()
        newAnswers.close()