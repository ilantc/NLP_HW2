import re
import sentence
import networkx as nx
import math
import pickle
import sys
import time
import csv

class mstModel:
    
        
    rootSymbol = "__root__"
    rootPOS = "__rootPos__"
    
    def __init__(self):
        self.featuresNum = 0
        self.featureIndex = 0 
        self.w_f = []
        self.w_f_20 = []
        self.w_f_50 = []
        self.w_f_80 = []
        self.w_f_100 = []
        self.featureNames = []
        self.allSentences = [] 
        self.featureDict = {'pWord': {}, 'pPos' : {}, 'cWord': {}, 'cPos': {},'pWordPPos':{},\
                   'cWordCPos':{}, 'pPosCWordCPos':{},'pWordPPosCPos':{}, 'pPosCPos':{}}
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
    
    def insertToFeaturesDicts(self,pWord, pPos, cWord, cPos):
        if not self.featureDict['cWord'].has_key(cWord):
            self.featureDict['cWord'][cWord] = self.featureIndex
            self.featureNames.append("cW     = " + cWord)
            self.featureIndex += 1
        if not self.featureDict['cPos'].has_key(cPos):
            self.featureDict['cPos'][cPos] = self.featureIndex
            self.featureNames.append("cP     = " + cPos)
            self.featureIndex += 1   
        if not self.featureDict['pWord'].has_key(pWord):
            self.featureDict['pWord'][pWord] = self.featureIndex
            self.featureNames.append("pW     = " + pWord)
            self.featureIndex += 1
        if not self.featureDict['pPos'].has_key(pPos):
            self.featureDict['pPos'][pPos] = self.featureIndex
            self.featureNames.append("pP     = " + pPos)
            self.featureIndex += 1
        if not self.featureDict['pWordPPos'].has_key((pWord,pPos)):
            self.featureDict['pWordPPos'][(pWord,pPos)] = self.featureIndex
            self.featureNames.append("pWpP   = " + pWord+","+pPos)
            self.featureIndex += 1
        if not self.featureDict['cWordCPos'].has_key((cWord,cPos)):
            self.featureDict['cWordCPos'][(cWord,cPos)] = self.featureIndex
            self.featureNames.append("cWcP   = " + cWord+","+cPos)
            self.featureIndex += 1
        if not self.featureDict['pPosCWordCPos'].has_key((pPos,cWord,cPos)):
            self.featureDict['pPosCWordCPos'][(pPos,cWord,cPos)] = self.featureIndex
            self.featureNames.append("pPcWcP = " + pPos+","+cWord+","+cPos)
            self.featureIndex += 1
        if not self.featureDict['pWordPPosCPos'].has_key((pWord,pPos,cPos)):
            self.featureDict['pWordPPosCPos'][(pWord,pPos,cPos)] = self.featureIndex
            self.featureNames.append("pWpPcP = " + pWord +"," + pPos+","+cPos)
            self.featureIndex += 1
        if not self.featureDict['pPosCPos'].has_key((pPos,cPos)):
            self.featureDict['pPosCPos'][(pPos,cPos)] = self.featureIndex   
            self.featureNames.append("pPcP   = " + pPos+","+cPos) 
            self.featureIndex += 1   
        
    def buildFeatureMapping(self,oldFeatureSet=False):
        if oldFeatureSet:
            for sentence in self.allSentences:
                for childIndex in range(0,len(sentence.words)):
                    cWord = sentence.words[childIndex] 
                    cPos = sentence.poss[childIndex]
                    if sentence.goldHeads[childIndex] != 0:
                        pWord = sentence.words[sentence.goldHeads[childIndex]-1]
                        pPos = sentence.poss[sentence.goldHeads[childIndex]-1]
                    else:
                        pWord = self.rootSymbol
                        pPos = self.rootPOS
                    self.insertToFeaturesDicts(pWord, pPos, cWord, cPos)    
            self.featuresNum = self.featureIndex
        else:
            for sentence in self.allSentences:
                for parentIndex in range(0,len(sentence.words) + 1):
                    pWord = sentence.words[parentIndex - 1]
                    pPos = sentence.poss[parentIndex - 1]
                    if parentIndex == 0:
                        pWord = self.rootSymbol
                        pPos = self.rootPOS
                    for childIndex in range(1,len(sentence.words) + 1):
                        cWord = sentence.words[childIndex - 1] 
                        cPos = sentence.poss[childIndex - 1]
                        self.insertToFeaturesDicts(pWord, pPos, cWord, cPos)    
            self.featuresNum = self.featureIndex
        
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
        if self.featureDict['pWordPPosCPos'].has_key((pWord,pPos,cPos)):
            indices.append(self.featureDict['pWordPPosCPos'][(pWord,pPos,cPos)])
        if self.featureDict['pPosCPos'].has_key((pPos,cPos)):
            indices.append(self.featureDict['pPosCPos'][(pPos,cPos)])
        return indices
    
    def calcFeatureVectorPerSentence(self, sentence, heads):
        featureVectorIndices = {}
        for childIndex in range(0,len(sentence.words)):
            cWord = sentence.words[childIndex] 
            cPos = sentence.poss[childIndex]
            pWord = sentence.words[heads[childIndex]-1]
            pPos = sentence.poss[heads[childIndex]-1]
            if heads[childIndex] == 0:
                pWord = self.rootSymbol
                pPos = self.rootPOS
            
            indices = self.getEdgeFeatureIndices(pWord, pPos, cWord, cPos)
                  
            for index in indices:
                if featureVectorIndices.has_key(index):
                    featureVectorIndices[index] += 1
                else:
                    featureVectorIndices[index] = 1
        return featureVectorIndices 
    
    def calcEdgeWeight(self, pWord, pPos, cWord, cPos, w):
        try:
            indices = self.getEdgeFeatureIndices(pWord, pPos, cWord, cPos)
            w_e = 0
            for index in indices:
                w_e += w[index]*1
        except Exception as err: 
            sys.stderr.write('problem in calcEdgeWeight in words:', pWord, pPos, cWord, cPos )     
            print err.args      
            print err
        return w_e
    
    def train(self,iterNum):
        self.perceptron(iterNum)
        
    def getWNorm(self):
        return math.sqrt(sum([w_i * w_i for w_i in self.w_f]))
    
    def perceptron(self,iterNum):
        print "running perceptron for",iterNum,"iterations"
        t1 = time.clock()
        self.w_f = [0]*self.featuresNum
#         k = 0 #for the perceptron iteration
        printIter = False
        printStep = max(1,int(len(self.allSentences)/5))
        for nIter in range(0,iterNum):
            if nIter % 5 == 0:
                printIter = True
            sIndex = 0
            for sentence in self.allSentences:
                tSentence = time.clock()
                currFeatureVectorIndices = self.calcFeatureVectorPerSentence(sentence,sentence.goldHeads)
                (maxSpanningTree,maxSpanningTreeFeatureIndices,_) = self.chuLiuEdmondsWrapper(sentence)
#                 print "w norm =",self.getWNorm(),maxSpanningTree, sentence.goldHeads
#                 print self.w_f
                if maxSpanningTree != sentence.goldHeads:
                    for featureIndex in currFeatureVectorIndices.keys():
                        self.w_f[featureIndex] += currFeatureVectorIndices[featureIndex]
                    for featureIndex in maxSpanningTreeFeatureIndices.keys():
                        self.w_f[featureIndex] -= maxSpanningTreeFeatureIndices[featureIndex]
                if printIter and ((sIndex % printStep) == 0):
                    print "\tdone", sIndex + 1,"sentences out of", len(self.allSentences), "average sentence time =", (time.clock() - tSentence)/(sIndex + 1)
                sIndex += 1
            if nIter == 19:
                self.w_f_20 = self.w_f
            if nIter == 49:
                self.w_f_50 = self.w_f
            if nIter == 79:
                self.w_f_80 = self.w_f
            if nIter == 99:
                self.w_f_100 = self.w_f
            
            if printIter:
                print "iter =", nIter + 1 , "average perceptron time =", (time.clock() - t1) / (nIter + 1)
            printIter = False
        return
    
    def initGraph(self,sentence,w):
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
                w_e = self.calcEdgeWeight( pWord, pPos, cWord, cPos, w)
                G.add_edge(p, c, {'weight': w_e})
        
        return G
    
    def contract(self,G,C_edges):
        C_nodes = [u for (u,_) in C_edges]
        subgraphNodes = filter(lambda node: node not in C_nodes, G.nodes())
        Gc = G.subgraph(subgraphNodes)
        newNode = "_".join(map(lambda node: str(node),C_nodes))
        Gc.add_node(newNode)
        scoreC = sum(G[u][v]['weight'] for (u,v) in C_edges)
        for node in subgraphNodes:
            edgesFromC = [(c,node) for c in filter(lambda cNode: G.has_edge(cNode,node),C_nodes)]
            if len(edgesFromC) > 0:
                (best_c,node) = max(edgesFromC, key = lambda (u,v): G[u][v]['weight'])
                Gc.add_edge(newNode,node,{'weight': G[best_c][node]['weight'], 'origU': best_c})
            
            edgesToC = [(node,c) for c in filter(lambda cNode: G.has_edge(node,cNode),C_nodes)]
            if len(edgesToC) > 0:
                bestScore = float('Inf') * (-1)
                bestCnode = 0
                for (node,c_node) in edgesToC:
                    filtered = filter(lambda (u,v): v == c_node,C_edges)
                    (c_u,_) = filtered[0]
                    score = G[node][c_node]['weight'] - G[c_u][c_node]['weight']
                    if score > bestScore:
                        bestScore = score
                        bestCnode = c_node
                Gc.add_edge(node,newNode,{'weight': bestScore + scoreC, 'origV': bestCnode})
        return {'G':Gc, 'newnode':newNode}
    
    def chuLiuEdmondsWrapper(self, sentence, w=None):
        if not w:
            w = self.w_f
        G = self.initGraph(sentence,w)
        optG = self.chuLiuEdmonds(G)
        
        heads = [0] * len(sentence.words)
        for (p,c) in optG.edges():
            heads[c - 1] = p
        featureVec = self.calcFeatureVectorPerSentence(sentence,heads)
        return (heads,featureVec,G)
    
    def chuLiuEdmonds(self,G):
        edges = G.edges()
        bestInEdges = []
        for node in G.nodes():
            if node == 0:
                continue
            allInNodes = [u for (u,_) in filter(lambda (u,v): v == node, edges)]
            bestP = max(allInNodes, key = lambda u: G[u][node]['weight'])
            bestInEdges.append((bestP,node,G.get_edge_data(bestP,node)))
        newG = nx.DiGraph()
        newG.add_nodes_from(G.nodes())
        newG.add_edges_from(bestInEdges)
        
        # get the first cycle in newG
        cs = list(nx.simple_cycles(newG))
        if len(cs) == 0:
            return newG
        c = max(cs, key = lambda circle: len(circle))
        C_edges = []
        for c_node_index in range(len(c) - 1):
            C_edges.append((c[c_node_index],c[c_node_index + 1]))
        C_edges.append((c[-1],c[0]))
        contractOutput = self.contract(G, C_edges)
        Gc = contractOutput['G']
        newNode = contractOutput['newnode']
        Gopt = self.chuLiuEdmonds(Gc)
        
        # now we need to take care of the new graph:
        # 1) remove the dummy node that was contracted
        newNodeInEdge = filter(lambda (u,v): v == newNode,Gopt.edges())
        if len(newNodeInEdge)==0:
            print "oh no"
        newNodeInEdgeU = newNodeInEdge[0][0]
        newNodeInEdgeV = newNodeInEdge[0][1]
        newNodeInEdgeData = Gc.get_edge_data(newNodeInEdgeU,newNodeInEdgeV)
        
        newNodeOutEdges = filter(lambda (u,v): u == newNode,Gopt.edges())
        edgesToAdd = []
        for i in range(len(newNodeOutEdges)):
            newNodeOutEdgeU = newNodeOutEdges[i][0]
            newNodeOutEdgeV = newNodeOutEdges[i][1]
            newNodeOutEdgeData = Gc.get_edge_data(newNodeOutEdgeU,newNodeOutEdgeV)
            edgesToAdd.append({'u':newNodeOutEdgeU, 'v':newNodeOutEdgeV, 'data': newNodeOutEdgeData})
        
        Gopt.remove_node(newNode)
        
        # 2) add the edges from C
        for (u,v) in C_edges:
            Gopt.add_edge(u,v,G.get_edge_data(u,v))
        
        # 3) remove the edge from C that cones just before the entry point to C in the 
        # contracted graph, 
        uToRemove = c[c.index(newNodeInEdgeData['origV']) - 1]
        Gopt.remove_edge(uToRemove,newNodeInEdgeData['origV'])
        
        # 4) add the incoming edge to the contracted node back to the graph
        Gopt.add_edge(newNodeInEdgeU, newNodeInEdgeData['origV'], G.get_edge_data(newNodeInEdgeU, newNodeInEdgeData['origV']))
        
        # 5) if there was an outgoing edge from the contracted node, add it as well
        for edgeToAdd in edgesToAdd:
            Gopt.add_edge(edgeToAdd['data']['origU'], edgeToAdd['v'], G.get_edge_data(edgeToAdd['data']['origU'], edgeToAdd['v']))
        
        return Gopt
    
    def treeVal(self,G,heads):
        score = 0
        for v in range(len(heads)):
            u = heads[v]
            score += G[u][v + 1]['weight']
        return score
    
    def save(self,fileName):
        """ save the model to file"""
        with open(fileName, 'wb') as output:
            pickler = pickle.Pickler(output, -1)
            pickler.dump(self)
    
    def load(self, filename):
        """ load a model from file """ 
        print "loading model..."
        t1 = time.clock()
        with open(filename, 'rb') as inputFile:
            modelData = pickle.load(inputFile)
            self.w_f_20 = modelData.w_f_20
            self.w_f_50 = modelData.w_f_50
            self.w_f_80 = modelData.w_f_80
            self.w_f_100 = modelData.w_f_100
            self.w_f = modelData.w_f

            self.allSentences = modelData.allSentences
            self.featuresNum = modelData.featuresNum 
            self.featureDict = modelData.featureDict

            self.featureNames = modelData.featureNames
        t2 = time.clock()
        print "time to load raw data =",t2 - t1
    
    def test(self,sentences,outputFileName):
        csvfile = open(outputFileName, 'w')
        fieldnames = ["sentenceIndex","w_20","w_50","w_80","w_100","n"] 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        sentenceIndex = 1
        for sentence in sentences:
            (optHeads_20,_,_) = self.chuLiuEdmondsWrapper(sentence,self.w_f_20)
            allCorrect_20 = filter(lambda (g,p): g == p, zip(sentence.goldHeads,optHeads_20))
            
            (optHeads_50,_,_) = self.chuLiuEdmondsWrapper(sentence,self.w_f_50)
            allCorrect_50 = filter(lambda (g,p): g == p, zip(sentence.goldHeads,optHeads_50))
            
            (optHeads_80,_,_) = self.chuLiuEdmondsWrapper(sentence,self.w_f_80)
            allCorrect_80 = filter(lambda (g,p): g == p, zip(sentence.goldHeads,optHeads_80))
            
            (optHeads_100,_,_) = self.chuLiuEdmondsWrapper(sentence,self.w_f_100)
            allCorrect_100 = filter(lambda (g,p): g == p, zip(sentence.goldHeads,optHeads_100))
            
            line = {"sentenceIndex": sentenceIndex,"w_20": len(allCorrect_20),"w_50": len(allCorrect_50),\
                    "w_80": len(allCorrect_80),"w_100": len(allCorrect_100), "n": len(sentence.words)}
            print "sentence", sentenceIndex , "out of" , len(sentences), ":"
            print "gold Heads    =", sentence.goldHeads
            print "opt Heads_20  =", optHeads_20
            print "opt Heads_50  =", optHeads_50
            print "opt Heads_80  =", optHeads_80
            print "opt Heads_100 =", optHeads_100, "\n"
            
            writer.writerow(line)
            sentenceIndex += 1
        
        csvfile.close 
        return
    
    