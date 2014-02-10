#! /usr/bin/env python
#coding=utf-8
from __future__ import division
import subprocess
import math

malletPath='c:\\mallet\\dist;c:\\mallet\\dist\\mallet.jar;c:\\mallet\\dist\\mallet-deps.jar'

def getlexicon(documents):
    words=[]
    # get the words use in train documents
    for document in documents:
        words+=document.words.keys()
    words=set(words)
    
    # create the (word,id) pairs
    lexicon=dict([(word,i+1) for i,word in enumerate(words)])
    return lexicon
    

def createMEText(documents,lexicon,path):
    lines=[]
    for i,document in enumerate(documents):
        if document.polarity==True:
            line="%s 1 " % (i+1)
        else:
            line="%s 0 " % (i+1)
        pairs=[(lexicon[word],document.words[word]) for word in document.words.keys() if word in lexicon]
        line+=' '.join(['%d=%f' %(pair[0],pair[1]) for pair in pairs])
        #line+=' '.join(['%d:1' %pair[0] for pair in pairs])
        lines.append(line)
        
    text='\n'.join(lines)
    output=open(path,'w')
    output.write(text)
    output.close()
    
def createResults(tests):
    input=open('result.output','rb')
    results=[]
    
    p=n=tp=tn=fp=fn=0
    for i,line in enumerate(input):
        label,prob=line.split()[2].split(':')
        if label=='0':
            results.append(-1*float(prob))
        else:
            results.append(float(prob))
        
        if tests[i].polarity==True:
            p+=1
            if label=='1':
                tp+=1
            else:
                fn+=1
        else:
            n+=1
            if label=='0':
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

def fileToBin(trainFilePath,trainBinPath,testFilePath,testBinPath):
    # train file to binary
    cmd='java -cp %s lltCsv2Vectors --input %s --output  %s' %(malletPath,trainFilePath,trainBinPath)
    retcode=subprocess.Popen(cmd.split())      
    retcode.wait()
    if retcode < 0:
        print 'child is terminated'
    else:
        print 'vector modification successful'
    
    # test file to binary
    cmd='java -cp %s lltCsv2Vectors  --use-pipe-from %s --input %s --output %s' %(malletPath,trainBinPath,testFilePath,testBinPath)
    retcode=subprocess.Popen(cmd.split())      
    retcode.wait()
    if retcode < 0:
        print 'child is terminated'
    else:
        print 'vector modification successful'
    
    

def train(trainBinPath,modelPath):
    cmd='java -cp %s cc/mallet/classify/tui/Vectors2Classify --input %s --output-classifier  %s --trainer MaxEnt' %(malletPath,trainBinPath,modelPath)
    retcode=subprocess.Popen(cmd.split())      
    retcode.wait()
    if retcode < 0:
        print 'child is terminated'
    else:
        print 'classifier training successful'

    
def classify(modelPath,testBinPath,resultPath):
    cmd='java -cp %s lltClassification --classifier %s --testing-file %s --report test:raw' % (malletPath,modelPath,testBinPath)
    retcode=subprocess.Popen(cmd.split(),stdout=file(resultPath,'w'))
    retcode.wait()
    if retcode < 0:
        print 'testing is terminated'
    else:
        print 'testing successful'
    
    
def me_classify(trains,tests):
    lexicon=getlexicon(trains)
    createMEText(trains,lexicon,'train.txt')
    createMEText(tests,lexicon,'test.txt')
    
    fileToBin('train.txt','train.bin','test.txt','test.bin')
    train('train.bin','train.model')
    classify('train.model','test.bin','result.output')
    
    #根据result.output创建结果集合
    return createResults(tests)

def run_classify(tests):
    fileToBin('train.txt','train.bin','test.txt','test.bin')
    train('train.bin','train.model')
    classify('train.model','test.bin','result.output')
        
    #根据result.output创建结果集合
    return createResults(tests)
    
