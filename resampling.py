#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from maxent import me_classify
import random
import math
from naivebayes import nb_classify
from svmclassify import svm_classify

class CDocument:
    def __init__(self,polarity,words):
        self.polarity=polarity
        self.words=words

def classify_feature(trains,tests,features,classify=me_classify):
    fTrains=[]
    for document in trains:
        fTrains.append(CDocument(document.polarity,dict([(word,document.words[word]) for word in document.words if word in features])))
    
    fTests=[]
    for document in tests:
        fTests.append(CDocument(document.polarity,dict([(word,document.words[word]) for word in document.words if word in features])))
    
    return classify(fTrains,fTests)



def classify_combined(tests,resultsList):
    p=n=tp=tn=fp=fn=0
    for i in range(len(tests)):
        multPos=multNeg=1
        for j in range(len(resultsList)):
            posProb=resultsList[j][i]
            if posProb>0:
                negProb=1-posProb
            elif posProb<0:
                negProb=abs(posProb)
                posProb=1-negProb
            else:
                negProb=posProb=1
            multPos*=posProb
            multNeg*=negProb
        score=multPos-multNeg
        
        if tests[i].polarity==True:
            p+=1
            if score>0:
                tp+=1
            else:
                fn+=1
        else:
            n+=1
            if score<0:
                tn+=1
            else:
                fp+=1

    acc=(tp+tn)/(p+n)
    precisionP=tp/(tp+fp)
    precisionN=tn/(tn+fn)
    recallP=tp/(tp+fn)
    recallN=tn/(tn+fp)
    gmean=math.sqrt(recallP*recallN)
    f_p=2*precisionP*recallP/(precisionP+recallP)
    f_n=2*precisionN*recallN/(precisionN+recallN)
    print 'combined results'
    print '{gmean:%s recallP:%s recallN:%s} {precP:%s precN:%s fP:%s fN:%s} acc:%s' %(gmean,recallP,recallN,precisionP,precisionN,f_p,f_n,acc)
    return {'gmean':gmean,'recallP':recallP,'recallN':recallN,'precP':precisionP,'precN':precisionN,'fP':f_p,'fN':f_n,'acc':acc},[]
  


def fullyTraining(trains,tests,classify=me_classify):
    classify(trains,tests)

def overSampling(posTrains,negTrains,tests,classify=me_classify):
    fold=20
    accSum={'gmean':0,'recallP':0,'recallN':0,'precP':0,'precN':0,'fP':0,'fN':0,'acc':0}

    for i in range(fold):
        trains=[]
        for j in range(len(posTrains)):
            index=int(random.random()*len(negTrains))
            trains.append(negTrains[index])
        trains+=posTrains
        acc,results=classify(trains,tests)
        for key in accSum.keys():
            accSum[key]+=acc[key]
    
    print 'the average results: '
    print '{gmean:%s recallP:%s recallN:%s} {precP:%s precN:%s fP:%s fN:%s} acc:%s' %(accSum['gmean']/fold,accSum['recallP']/fold,accSum['recallN']/fold,accSum['precP']/fold,accSum['precN']/fold,accSum['fP']/fold,accSum['fN']/fold,accSum['acc']/fold)
        
def underSampling(posTrains,negTrains,tests,classify=me_classify):
    trains=negTrains+posTrains[:len(negTrains)]
    classify(trains,tests)
    
def underSampling_average(posTrains,negTrains,tests,classify=me_classify):
    resultsList=[]
    times=len(posTrains)//len(negTrains)
    print times
    accSum={'gmean':0,'recallP':0,'recallN':0,'precP':0,'precN':0,'fP':0,'fN':0,'acc':0}
    for i in range(times):
        trains=negTrains+posTrains[i*len(negTrains):(i+1)*len(negTrains)]
        acc,results=classify(trains,tests)
        for key in accSum.keys():
            accSum[key]+=acc[key]
    
    print 'the average results: '
    print '{gmean:%s recallP:%s recallN:%s} {precP:%s precN:%s fP:%s fN:%s} acc:%s' %(accSum['gmean']/times,accSum['recallP']/times,accSum['recallN']/times,accSum['precP']/times,accSum['precN']/times,accSum['fP']/times,accSum['fN']/times,accSum['acc']/times)
        

def underSampling_combined(posTrains,negTrains,tests,classify=me_classify):
    resultsList=[]
    times=len(posTrains)//len(negTrains)
    print times
    for i in range(times):
        trains=negTrains+posTrains[i*len(negTrains):(i+1)*len(negTrains)]
        resultsList.append(classify(trains,tests)[1])
    classify_combined(tests,resultsList)
    

def underSampling_combined_random(posTrains,negTrains,tests,classify=me_classify):
    fold=10
    accSum={'gmean':0,'recallP':0,'recallN':0,'precP':0,'precN':0,'fP':0,'fN':0,'acc':0}
    
    
    for j in range(fold):
        resultsList=[]
        times=len(posTrains)//len(negTrains)
        print times
        for i in range(times):
            trains=negTrains+posTrains[i*len(negTrains):(i+1)*len(negTrains)]
            
            features=[]
            for document in trains:
                features+=document.words.keys()
            features=set(features)  
            features0=[];features1=[]
            for feature in features:
                if random.random()<0.5:
                    features0.append(feature)
                else:
                    features1.append(feature)
            features0=set(features0)
            features1=set(features1)
            
            resultsList.append(classify_feature(trains,tests,features0)[1])
            resultsList.append(classify_feature(trains,tests,features1)[1])
            #resultsList.append(classify(trains,tests)[1])
        acc=classify_combined(tests,resultsList)[0]
        for key in accSum.keys():
            accSum[key]+=acc[key]
    print 'the average results: '
    print '{gmean:%s recallP:%s recallN:%s} {precP:%s precN:%s fP:%s fN:%s} acc:%s' %(accSum['gmean']/fold,accSum['recallP']/fold,accSum['recallN']/fold,accSum['precP']/fold,accSum['precN']/fold,accSum['fP']/fold,accSum['fN']/fold,accSum['acc']/fold)


def underSampling_combined_classifies(posTrains,negTrains,tests):
    resultsList=[]
    times=len(posTrains)//len(negTrains)
    classifies=[lambda trains,tests:me_classify(trains,tests),lambda trains,tests:nb_classify(trains,tests),lambda trains,tests:svm_classify(trains,tests)]
    print times
    for i in range(times):
        trains=negTrains+posTrains[i*len(negTrains):(i+1)*len(negTrains)]
        resultsList.append(classifies[i%3](trains,tests)[1])
    classify_combined(tests,resultsList)
    
#def underSampling_combined_random_classifies(posTrains,negTrains,tests,classify=me_classify):
#    fold=10
#    accSum={'gmean':0,'recallP':0,'recallN':0,'precP':0,'precN':0,'fP':0,'fN':0,'acc':0}
#    classifies=[lambda trains,tests:me_classify(trains,tests),lambda trains,tests:nb_classify(trains,tests),lambda trains,tests:svm_classify(trains,tests)]
#    
#    for j in range(fold):
#        resultsList=[]
#        times=len(posTrains)//len(negTrains)
#        print times
#        k=0
#        for i in range(times):
#            trains=negTrains+posTrains[i*len(negTrains):(i+1)*len(negTrains)]
#            
#            features=[]
#            for document in trains:
#                features+=document.words.keys()
#            features=set(features)  
#            features0=[];features1=[]
#            for feature in features:
#                if random.random()<0.5:
#                    features0.append(feature)
#                else:
#                    features1.append(feature)
#            features0=set(features0)
#            features1=set(features1)
#            
#            resultsList.append(classify_feature(trains,tests,features0,classify=classifies[k%3])[1])
#            k+=1
#            resultsList.append(classify_feature(trains,tests,features1,classify=classifies[k%3])[1])
#            k+=1
#            #resultsList.append(classify(trains,tests)[1])
#        acc=classify_combined(tests,resultsList)[0]
#        for key in accSum.keys():
#            accSum[key]+=acc[key]
#    print 'the average results: '
#    print '{gmean:%s recallP:%s recallN:%s} {precP:%s precN:%s fP:%s fN:%s} acc:%s' %(accSum['gmean']/fold,accSum['recallP']/fold,accSum['recallN']/fold,accSum['precP']/fold,accSum['precN']/fold,accSum['fP']/fold,accSum['fN']/fold,accSum['acc']/fold)


def underSampling_combined_random_classifies(posTrains,negTrains,tests,classify=me_classify):
    fold=5
    accSum={'gmean':0,'recallP':0,'recallN':0,'precP':0,'precN':0,'fP':0,'fN':0,'acc':0}
    classifies=[lambda trains,tests:me_classify(trains,tests),lambda trains,tests:nb_classify(trains,tests),lambda trains,tests:svm_classify(trains,tests)]
    
    for j in range(fold):
        resultsList=[]
        times=10
        print times
        k=0
        for i in range(times):
            #trains=negTrains+posTrains[i*len(negTrains):(i+1)*len(negTrains)]
            trains=[]
            for k in range(len(negTrains)):
                index=random.randint(0,len(posTrains)-1)
                trains.append(posTrains[index])
            trains+=negTrains
            
            features=[]
            for document in trains:
                features+=document.words.keys()
            features=set(features)  
            features0=[];features1=[]
            for feature in features:
                if random.random()<0.5:
                    features0.append(feature)
                else:
                    features1.append(feature)
            features0=set(features0)
            features1=set(features1)
            
            resultsList.append(classify_feature(trains,tests,features0,classify=classifies[k%3])[1])
            k+=1
            resultsList.append(classify_feature(trains,tests,features1,classify=classifies[k%3])[1])
            k+=1
            #resultsList.append(classify(trains,tests)[1])
        acc=classify_combined(tests,resultsList)[0]
        for key in accSum.keys():
            accSum[key]+=acc[key]
    print 'the average results: '
    print '{gmean:%s recallP:%s recallN:%s} {precP:%s precN:%s fP:%s fN:%s} acc:%s' %(accSum['gmean']/fold,accSum['recallP']/fold,accSum['recallN']/fold,accSum['precP']/fold,accSum['precN']/fold,accSum['fP']/fold,accSum['fN']/fold,accSum['acc']/fold)


def overSampling_feature_combined(posTrains,negTrains,tests,classify=me_classify):
    trains=[]
    for j in range(len(posTrains)):
        index=int(random.random()*len(negTrains))
        trains.append(negTrains[index])
    trains+=posTrains
    
    pFeatures=[]
    for document in posTrains:
        pFeatures+=document.words.keys()
    pFeatures=[feature for feature in set(pFeatures)]
    
    nFeatures=[]
    for document in negTrains:
        nFeatures+=document.words.keys()
    nFeatures=[feature for feature in set(nFeatures)]
    
    print len(pFeatures),len(nFeatures)
    
#    resultsList=[]
#    for i in range(10):
#        random.shuffle(pFeatures)
#        random.shuffle(nFeatures)
#        #features=set(pFeatures[:len(nFeatures)]+nFeatures)
#        features=set(pFeatures[:3000]+nFeatures[:3000])
#        resultsList.append(classify_feature(trains,tests,features)[1])
#    
#    classify_combined(tests,resultsList)
        
    
    #classify(trains,tests)
    
