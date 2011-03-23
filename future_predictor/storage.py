#!/usr/bin/env python

import sys
import answer

class storage:
    def readanswers():
        #res = urllib2.urlopen(THA_LINK)
        #soup = BeautifulSoup(res.read())
        #krugi_file = soup.find('a', title='krugi.txt')['href']
        #lines = urllib2.urlopen(krugi_file).read().split('\n')
        #answers = converttoanswers(lines)
        return answers

    def linestoanswers(self,lines):
        answers = []
        for l in lines:
            if(len(l) > 0 and l[0] != '#'):
                arguments = l.split('|')
                if len(arguments) == 3:
                    a = answer.answer(arguments[0],arguments[1],arguments[2].split(';'))
                    #print(a.tostring())
                    answers.append(a)
        return answers

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
        return ["Widder","Stier","Zwilling","Krebs","Löwe","Jungfrau","Skorpion","Schütze","Steinbock","Wassermann","Fisch"]

    def getcards(self):
        colors = ["Herz","Karo","Schaufel","Pik","Schellen","Rosen","Schilten","Eichel"]
        numbers = ["Sechs","Sieben","Acht","Neu","Zehn","Bube","Bauer","Dame","König","Under","Ober","Ass"]
        return [colors,numbers]
