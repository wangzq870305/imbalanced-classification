#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from maxent import me_classify
import random
import math

class CDocument:
    def __init__(self,polarity,words):
        self.polarity=polarity
        self.words=words

def cosine(source,target):
    numerator=sum([source[word]*target[word] for word in source if word in target])
    sourceLen=math.sqrt(sum([value*value for value in source.values()]))
    targetLen=math.sqrt(sum([value*value for value in target.values()]))
    denominator=sourceLen*targetLen
    if denominator==0:
        return 0
    else:
        return numerator/denominator

def SMOTE(posTrains,negTrains,tests,classify=me_classify):
    synSamples=[]
    k=50
    for i in range(len(posTrains)-len(negTrains)):
        index=i%len(negTrains)
        s=negTrains[index]
        
        similars=sorted([(cosine(sample.words,s.words),sample) for j,sample in enumerate(negTrains) if j!=index])
        similars.reverse()
        nearest=[similar[1] for similar in similars[:k]]
        nS=nearest[random.randint(0,k-1)]
        
        delta=random.random()
        
        totalWords=set(s.words.keys()+nS.words.keys())
        words={}
        for word in totalWords:
            x=0
            if word in s.words:
                x=s.words[word]
            if word in nS.words:
                x+=delta*(nS.words[word]-x)
            if x>0:words[word]=x
        synSamples.append(CDocument(s.polarity,words))
        print i
    
    classify(posTrains+negTrains+synSamples,tests)