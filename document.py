from __future__ import division

class Document:
    def __init__(self,polarity,words):
        self.polarity=polarity
        self.words=words

class Domain:
    def __init__(self,posTrains,negTrains,tests):
        self.posTrains=posTrains
        self.negTrains=negTrains
        self.tests=tests
        
        documents=self.posTrains+self.negTrains
        df={}
        for document in documents:
            for word in document.words:
                if word not in df:df[word]=0
                df[word]+=1
        
        for document in documents+self.tests:
            for word in document.words.keys():
                if word in df and df[word]<3:
                    del document.words[word]
    def getTrains(self):
        return self.posTrains+self.negTrains

def readFromFile(path,polarity):
    input=open(path,'rb')
    documents=[]
    for line in input:
        pieces=line.split()
        words={}
        for i,piece in enumerate(pieces):
            word=piece.lower()
            if word not in words: words[word]=1
        if len(words)>0:
            documents.append(Document(polarity,words))
    return documents

def createDomain(domain):
    neg=readFromFile(r'corpus\%s\negative.review' % domain,False)
    pos=readFromFile(r'corpus\%s\positive.review' % domain,True)

    #return Domain(pos[200:],neg[200:400],pos[:200]+neg[:200])
    
    rate=len(pos)/len(neg)
    return Domain(pos[200:200+int(1000*rate)],neg[200:1200],pos[:200]+neg[:200])



