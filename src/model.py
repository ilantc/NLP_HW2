import re
import sentence
import networkx as nx

class mstModel:
    
    w = []
    featureDict = {'pWord': {}, 'pPos' : {}, 'cWord': {}, 'cPos': {},'pWordPPos':{},\
                   'cWordCPos':{}, 'pPosCWordCPos':{}, 'pPosCPos':{}}
    allSentences = []
    featuresNum = 0 
    
    rootSymbol = "__root__"
    rootPOS = "__rootPos__"
    
    def __init__(self):
        self.featuresNum = 0
        self.w = []
        return
    
    def readFile(self,numSentences,offset = 0,inputFile = "../data/wsj_gold_dependency"):
        """ read input file """
        f = open(inputFile,'rt')
        allSentences = []
        # iterate until offset is passed
        currSentenceIndex = 0
        while currSentenceIndex < offset:
            line = f.readline()
            # empty line means a sentence had just ended
            if re.match("^\s*$",line):
                currSentenceIndex += 1
        
        # read the required sentences
        stopIndex = numSentences + offset
        words = []
        poss = []
        goldHeads = []
        while currSentenceIndex < stopIndex:
            line = f.readline()
            # if we are in an empty line - reset all params and save sentence
            if re.match("^\s*$",line):
                currSentenceIndex += 1
                s = sentence.sentence(words,poss,goldHeads)
                allSentences.append(s)
                words = []
                poss = []
                goldHeads = []
            else:
                fields = line.split()
                words.append(fields[1])
                poss.append(fields[3])
                goldHeads.append(int(fields[6]))
        return allSentences
    
    # TODO - Liora
    
    def buildFeatureMapping(self):
        featureIndex = 0
        for sentence in self.allSentences:
            for wordIndex in range(0,len(sentence.words)):
                if not self.featureDict['cWord'].has_key(sentence.words[wordIndex]):
                    self.featureDict['cWord'][sentence.words[wordIndex]] = featureIndex
                    featureIndex += 1
                if not self.featureDict['cPos'].has_key(sentence.poss[wordIndex]):
                    self.featureDict['cPos'][sentence.poss[wordIndex]] = featureIndex
                    featureIndex += 1   
                if not self.featureDict['pWord'].has_key(sentence.words[sentence.goldHeads[wordIndex]-1]):
                    self.featureDict['pWord'][sentence.words[sentence.goldHeads[wordIndex]-1]] = featureIndex
                    featureIndex += 1
                if not self.featureDict['pPos'].has_key(sentence.poss[sentence.goldHeads[wordIndex]-1]):
                    self.featureDict['pPos'][sentence.poss[sentence.goldHeads[wordIndex]-1]] = featureIndex
                    featureIndex += 1
                if not self.featureDict['pWordPPos'].has_key((sentence.words[sentence.goldHeads[wordIndex]-1],sentence.poss[sentence.goldHeads[wordIndex]-1])):
                    self.featureDict['pWordPPos'][(sentence.words[sentence.goldHeads[wordIndex]-1],sentence.poss[sentence.goldHeads[wordIndex]-1])] = featureIndex
                    featureIndex += 1
                if not self.featureDict['cWordCPos'].has_key((sentence.words[wordIndex],sentence.poss[wordIndex])):
                    self.featureDict['cWordCPos'][(sentence.words[wordIndex],sentence.poss[wordIndex])] = featureIndex
                    featureIndex += 1
                if not self.featureDict['pPosCWordCPos'].has_key((sentence.poss[sentence.goldHeads[wordIndex]-1],sentence.words[wordIndex],sentence.poss[wordIndex])):
                    self.featureDict['pPosCWordCPos'][(sentence.poss[sentence.goldHeads[wordIndex]-1],sentence.words[wordIndex],sentence.poss[wordIndex])] = featureIndex
                    featureIndex += 1
                if not self.featureDict['pPosCPos'].has_key((sentence.poss[sentence.goldHeads[wordIndex]-1],sentence.poss[wordIndex])):
                    self.featureDict['pPosCPos'][(sentence.poss[sentence.goldHeads[wordIndex]-1],sentence.poss[wordIndex])] = featureIndex    
                    featureIndex += 1               
        self.featuresNum = featureIndex
    
    def getEdgeFeatureIndices(self,pWord, pPos, cWord, cPos):
        indices = []
        if self.featureDict['cWord'].has_key(cWord):
            indices.append(self.featureDict['cWord'][cWord])
        if self.featureDict['cPos'].has_key(cPos):
            indices.append(self.featureDict['cPos'][cPos])
        if self.featureDict['pWord'].has_key(pWord):
            indices.append(self.featureDict['pWord'][pWord])
        if self.featureDict['pPos'].has_key(pPos):
            indices.append(self.featureDict['pPos'][pPos])
        if self.featureDict['pWordPPos'].has_key((pWord,pPos)):
            indices.append(self.featureDict['pWordPPos'][(pWord,pPos)])
        if self.featureDict['cWordCPos'].has_key((cWord,cPos)):
            indices.append(self.featureDict['cWordCPos'][(cWord,cPos)])
        if self.featureDict['pPosCWordCPos'].has_key((pPos,cWord,cPos)):
            indices.append(self.featureDict['pPosCWordCPos'][(pPos,cWord,cPos)])
        if self.featureDict['pPosCPos'].has_key((pPos,cPos)):
            indices.append(self.featureDict['pPosCPos'][(pPos,cPos)])
        return indices
    
    
    # TODO - Liora
    
    def calcEdgeWeight(self,w, pWord, pPos, cWord, cPos):
        indices = self.getEdgeFeatureIndices(pWord, pPos, cWord, cPos)
        for index in indices:
            w[index] = w[index]*1
        return w
    
    
    # TODO - Liora
    
    def train(self,iterNum):
        self.w = self.perceptron(iterNum)
        
    
    # TODO - Liora
    
    def perceptron(self,iterNum):
        print "running perceptron for",iterNum," iterations"
        w = [0]*self.featuresNum
#         k = 0 #for the perceptron iteration
        for iter in range(0,iterNum):
            for sentence in self.allSentences:
                currFeatureVectorIndices = {}
                for wordIndex in range(0,len(sentence.words)):
                        indices = self.getEdgeFeatureIndices(sentence.words[sentence.goldHeads[wordIndex]-1],\
                                            sentence.poss[sentence.goldHeads[wordIndex]-1],\
                                            sentence.words[wordIndex],\
                                            sentence.poss[wordIndex])
                        for index in indices:
                            if currFeatureVectorIndices.has_key(index):
                                currFeatureVectorIndices[index] += 1
                            else:
                                currFeatureVectorIndices[index] = 1       
                (maxSpanningTree,maxSpanningTreeFeatureIndices) = self.ciuLiuEdmonds(sentence,w)
                diffFeatureIndices = {}
                if maxSpanningTree != sentence.goldHeads: #TODO....
                    for featureIndex in currFeatureVectorIndices.keys():
                        if featureIndex in maxSpanningTreeFeatureIndices.keys():
                            diffFeatureIndices[featureIndex] -= 1
                    w = w + diffFeatureIndices
        return w
    
    def initGraph(self,n,w):
        G = nx.DiGraph()
        n = len(sentence.words)
        
        # add all nodes and edges
        G.add_nodes_from(range(n + 1)) 
        
        # add edges and weights
        for p in range(0,n + 1):
            if p == 0:
                pWord = self.rootSymbol
                pPos = self.rootPOS
            else:
                pWord = sentence.words[p - 1]
                pWord = sentence.poss[p - 1]
            for c in range(1,n + 1):
                if p == c: 
                    continue
                cWord = sentence.words[c - 1]
                cPos = sentence.poss[c - 1]
                w_e = self.calcEdgeWeight(w, pWord, pPos, cWord, cPos)
                G.add_edge(p, c, {'weight': w_e})
        
        return G
    
    # TODO - Ilan
    
    def ciuLiuEdmonds(self, sentence, w):
        n = len(sentence.words)
        G = self.initGraph(n,w)

        
        return
    
    # TODO - Ilan
    def test(self):
        return
    
    