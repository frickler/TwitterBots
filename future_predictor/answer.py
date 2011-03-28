#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, string
from predictor_constants import *

class answer:
 def __init__(self,init_answer,init_answercount,init_keywords):
  self.keywords = []
  for a in init_keywords:
      self.keywords.append(a) # keywords to match
  self.answerused = int(init_answercount) # how may time this answer is used
  self.answer = init_answer # answer string
  self.question = ""
  self.keywordmatch = 0
  
 def tostring(self):
      s =  "keywords: "+str(self.keywords)
      s += " answerused "+str(self.answer)
      s += " answer "+str(self.answer)
      return s
 def keywordsmatch(self,init_question):
     self.question = init_question
     self.keywordmatch = 0
     for kword in self.keywords:
        if str(kword) in init_question:
            self.keywordmatch += 1
            #print("found "+kword)
     return self.keywordmatch

 def getquality(self):
     return self.keywordmatch - self.answerused

 def toLineString(self):   
     return self.answer+MAIN_SPLITER+str(self.answerused)+MAIN_SPLITER+KEYWORD_SPLITER.join(str(x) for x in self.keywords) 
