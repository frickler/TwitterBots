#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logic
import storage

l = logic.logic()

def askfrage(frage):
    resp = l.getanswer(frage)
    print("\n----------------------------------------\n")
    print("aks: "+frage)
    print("the answer is:"+ resp)
    print("\n-------------------------------------------\n")

def askfragename(frage,name):
    resp = l.getanswername(frage,name)
    print("\n----------------------------------------\n")
    print("aks: "+frage)    
    print("the answer is:"+ resp)
    print("\n-------------------------------------------\n")

print("these are the loaded answers: ")
for a in l.answers:
    print(a.tostring())
    print("\n")

print("\n")
print("\n")
  
#askfrage("wer ist der beste")
#askfrage("wie ist das wetter")
askfrage("Soll ich meinem Partner treu bleiben?")
askfrage("Welches Sternzeichen ist das beste?")
askfrage("Soll ich Lotto spielen?")
askfragename("Bitte um Rat: Soll ich mich scheiden lassen?","Stefan")
print("\n")
print("\n")

print("matching was:")
for a in l.answers:
    print("answer: "+a.answer +" keywords: "+str(a.keywords))
    print("keywordmatch: "+str(a.keywordmatch)+" quality: "+str(a.getquality())+" used: "+str(a.answerused))

l.saveanswerstofile();

