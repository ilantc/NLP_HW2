import re
import sentence

class mstModel:
    
    w = []
    featureDict = {'pWord': {}, 'pPos' : {}, 'cWord': {}, 'cPos': {}}
    
    
    def __init__(self):
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
                goldHeads.append(fields[6])
        return allSentences
    
    # TODO - Liora
    def buildFeatureMapping(self):
        return
    
    # TODO - Liora
    def calcEdgeWeight(self, w, pWord, pPos, cWord, cPos):
        return 0
    
    # TODO - Liora
    def train(self):
        return
    
    # TODO - Liora
    def perceptron(self):
        return
    
    # TODO - Ilan
    def ciuLiuEdmonds(self):
        return
    
    # TODO - Ilan
    def test(self):
        return
    
    