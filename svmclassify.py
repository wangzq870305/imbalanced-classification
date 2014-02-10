#! /usr/bin/env python
#coding=utf-8
from __future__ import division
import subprocess
import math

def getlexicon(documents):
    words=[]
    for document in documents:
        words+=document.words.keys()
    words=set(words)
    
    lexicon=dict([(word,i+1) for i,word in enumerate(words)])
    return lexicon
    
def createSvmText(documents,lexicon,path):
    text=''
    for document in documents:
        if document.polarity==True:
            line="+1 "
        else:
            line="-1 "
        pairs=[(lexicon[word],document.words[word]) for word in document.words.keys() if word in lexicon]
        pairs.sort()
        for pair in pairs:
            line+='%d:%d ' %(pair[0],pair[1])
        text+=line+'\n'
    if len(text)>0:
        output=open(path,'w')
        output.write(text)
     
def createResults(tests):
    input=open('result.output','rb')
    results=[]
    count=0
    p=n=tp=tn=fp=fn=0
    for i,line in enumerate(input):
        score=float(line)
        if (tests[i].polarity==True and score>0) or (tests[i].polarity==False and score<0):
           count+=1 
        distance=float(line)
        x0=1/(1+math.exp(abs(distance)))
        x1=1/(1+math.exp(-1*abs(distance)))
        prob=x1/(x0+x1)
        if distance<0:prob*=-1
        results.append(prob)
#    acc=float(count)/len(tests)
#    print 'accuracy is %f(%d/%d)' % (acc,count,len(tests))
#    return acc,results
        if tests[i].polarity==True:
            p+=1
            if prob>0:
                tp+=1
            else:
                fn+=1
        else:
            n+=1
            if prob<0:
                tn+=1
            else:
                fp+=1
           
    acc=(tp+tn)/(p+n)
    if p==0 or n==0:
        precisionP=0
        precisionN=0
        recallP=0
        recallN=0
        gmean=0
        f_p=0
        f_n=0
    else:
        precisionP=tp/(tp+fp)
        precisionN=tn/(tn+fn)
        recallP=tp/(tp+fn)
        recallN=tn/(tn+fp)
        gmean=math.sqrt(recallP*recallN)
        f_p=2*precisionP*recallP/(precisionP+recallP)
        f_n=2*precisionN*recallN/(precisionN+recallN)
    print '{gmean:%s recallP:%s recallN:%s} {precP:%s precN:%s fP:%s fN:%s} acc:%s' %(gmean,recallP,recallN,precisionP,precisionN,f_p,f_n,acc)
    return {'gmean':gmean,'recallP':recallP,'recallN':recallN,'precP':precisionP,'precN':precisionN,'fP':f_p,'fN':f_n,'acc':acc},results

    
def svm_classify(trains,tests):
    lexicon=getlexicon(trains)
    createSvmText(trains,lexicon,'train.txt')
    createSvmText(tests,lexicon,'test.txt')
    subprocess.call("cmd.bat",shell=True)
    return createResults(tests)

def run_svm_classify(tests):
    subprocess.call("cmd.bat",shell=True)
    return createResults(tests)

