#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import answer
from predictor_constants import *

class storage:

    def getanswersfromfile(self):
        f = open(ANSWER_FILE,'r')
        arry = []
        for line in f:
            arry.append(line)
        f.close()
        answer = self.linestoanswers(arry)
        return answer
        
    def gettarotcardsfromfile(self):
        f = open(TAROT_FILE,'r')
        arry = []
        for line in f:
            arry.append(line)
        f.close()
        return arry
        
    def linestoanswers(self,lines):
        answers = []
        for l in lines:
            if(len(l) > 0 and l[0] != '#'):
                arguments = l.split(MAIN_SPLITER)
                if len(arguments) == 3:
                    a = answer.answer(arguments[0],arguments[1],arguments[2].split(KEYWORD_SPLITER))
                    #print(a.tostring())
                    answers.append(a)
        return answers

    def getanswers(self):
        #return self.gettestanswers()
        answers = self.getanswersfromfile()
        print("\nTotal answers loaded: "+str(len(answers)))
        return answers
    
    def saveUnansweredQuestion(self,text,user):
        f = open(UNANSWERED_FILE,'a')
        f.write("\n"+user+"|"+text)
        f.close()
    def saveanswerstofile(self,answers):
        h = open(ANSWER_HEADER_FILE,'r')
        f = open(ANSWER_FILE,'w')
        s = "";
        for headerline in h:
            s += headerline
        s +="\n"
        for a in answers:
            s += a.toLineString()
        f.write(s)
        f.close()
        h.close()

    def gettestanswers(self):
        var = "am montag#0#am;montag\n"
        var += "vielleicht auch nicht|0|vielleicht;auch;nicht\n"
        var += "chäser ist der beste|0|wer;beste;sicher\n"
        var += "das wetter ist schön|0|wetter;morgen\n"
        var += "nach %planet% wird das wetter ist lausig.|0|wetter;morgen\n"
        var += "Ich habe für dich die Karte %card% gezogen. Das bedeutet nichts Gutes. Pass auf dich auf.|0|Job;Arbeit\n"
        var += "Ich sehe in den Karten %card% und %card% nicht gutes du solltest Partner wechseln.|0|Liebe;Partner\n"
        var += "Veränderung tut immer gut %yourname%, ein(e) %starsign% buhlt seit längerm um dich.|0|Liebe;Partner;neu\n"
        var += "Das Sternzeichen %starsign% ist das beste.|-4|Sternzeichen\n"
        var += "Du hast Recht %yourname% davon rate ich dir ab.|-4|Rat\n"
        var += "standart antwort|0|"
        lines = var.split('\n')
        answers = self.linestoanswers(lines)
       
        return answers

    def getplanets(self):
        return ["Merkur","Venus","Mars","Jupiter","Saturn","Uranus","Neptun","Pluto"]

    def getstarsgins(self):
        return ["Widder","Stier","Zwillinge","Krebs","Löwe","Jungfrau","Skorpion","Schütze","Steinbock","Wassermann","Fisch"]

    def getcards(self):
        colors = ["Herz","Karo","Schaufel","Pik","Schellen","Rosen","Schilten","Eichel"]
        numbers = ["Sechs","Sieben","Acht","Neu","Zehn","Bube","Bauer","Dame","König","Under","Ober","Ass"]
        return [colors,numbers]
