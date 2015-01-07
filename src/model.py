import re
import sentence
import networkx as nx
import math
import sys

class mstModel:
    
    w_f = []
    featureDict = {'pWord': {}, 'pPos' : {}, 'cWord': {}, 'cPos': {},'pWordPPos':{},\
                   'cWordCPos':{}, 'pPosCWordCPos':{}, 'pPosCPos':{}}
    allSentences = []
    featuresNum = 0 
    
    rootSymbol = "__root__"
    rootPOS = "__rootPos__"
    
    def __init__(self):
        self.featuresNum = 0
        self.featureIndex = 0 
        self.w_f = []
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
            self.featureIndex += 1
        if not self.featureDict['cPos'].has_key(cPos):
            self.featureDict['cPos'][cPos] = self.featureIndex
            self.featureIndex += 1   
        if not self.featureDict['pWord'].has_key(pWord):
            self.featureDict['pWord'][pWord] = self.featureIndex
            self.featureIndex += 1
        if not self.featureDict['pPos'].has_key(pPos):
            self.featureDict['pPos'][pPos] = self.featureIndex
            self.featureIndex += 1
        if not self.featureDict['pWordPPos'].has_key((pWord,pPos)):
            self.featureDict['pWordPPos'][(pWord,pPos)] = self.featureIndex
            self.featureIndex += 1
        if not self.featureDict['cWordCPos'].has_key((cWord,cPos)):
            self.featureDict['cWordCPos'][(cWord,cPos)] = self.featureIndex
            self.featureIndex += 1
        if not self.featureDict['pPosCWordCPos'].has_key((pPos,cWord,cPos)):
            self.featureDict['pPosCWordCPos'][(pPos,cWord,cPos)] = self.featureIndex
            self.featureIndex += 1
        if not self.featureDict['pPosCPos'].has_key((pPos,cPos)):
            self.featureDict['pPosCPos'][(pPos,cPos)] = self.featureIndex    
            self.featureIndex += 1   
    
    def buildFeatureMapping(self):
#         featureIndex = 0
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
    
    def calcFeatureVectorPerSentence(self, sentence, heads):
        featureVectorIndices = {}
        for childIndex in range(0,len(sentence.words)):
            cWord = sentence.words[childIndex] 
            cPos = sentence.poss[childIndex]
            if heads[childIndex] != 0:
                pWord = sentence.words[heads[childIndex]-1]
                pPos = sentence.poss[heads[childIndex]-1]
            else:
                pWord = self.rootSymbol
                pPos = self.rootPOS
            
            indices = self.getEdgeFeatureIndices(pWord, pPos, cWord, cPos)
                  
            for index in indices:
                if featureVectorIndices.has_key(index):
                    featureVectorIndices[index] += 1
                else:
                    featureVectorIndices[index] = 1
        return featureVectorIndices 
    # TODO - Liora
    
    def calcEdgeWeight(self, pWord, pPos, cWord, cPos):
        try:
            indices = self.getEdgeFeatureIndices(pWord, pPos, cWord, cPos)
            w_e = 0
            for index in indices:
                w_e += self.w_f[index]*1
        except Exception as err: 
            sys.stderr.write('problem in calcEdgeWeight in words:', pWord, pPos, cWord, cPos )     
            print err.args      
            print err
        return w_e
    
    # TODO - Liora
    
    def train(self,iterNum):
        self.perceptron(iterNum)
        
    
    # TODO - Liora
    
    def perceptron(self,iterNum):
        print "running perceptron for",iterNum," iterations"
        self.w_f = [0]*self.featuresNum
#         k = 0 #for the perceptron iteration
        for _ in range(0,iterNum):
            for sentence in self.allSentences:
                currFeatureVectorIndices = self.calcFeatureVectorPerSentence(sentence,sentence.goldHeads)
                (maxSpanningTree,maxSpanningTreeFeatureIndices) = self.chuLiuEdmondsWrapper(sentence)
                if maxSpanningTree != sentence.goldHeads:
                    for featureIndex in currFeatureVectorIndices.keys():
                        self.w_f[featureIndex] += currFeatureVectorIndices[featureIndex]
                    for featureIndex in maxSpanningTreeFeatureIndices.keys():
                        self.w_f[featureIndex] -= maxSpanningTreeFeatureIndices[featureIndex]
        return
    
    def initGraph(self,sentence):
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
                w_e = self.calcEdgeWeight( pWord, pPos, cWord, cPos)
                G.add_edge(p, c, {'weight': w_e})
        
        return G
    
    # TODO - Ilan
    
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
    
    def chuLiuEdmondsWrapper(self, sentence):
        G = self.initGraph(sentence)
        optG = self.chuLiuEdmonds(G)
        
        heads = [0] * len(sentence.words)
        for (p,c) in optG.edges():
            heads[c - 1] = p
        featureVec = self.calcFeatureVectorPerSentence(sentence,heads)
        return (heads,featureVec)
    
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
        try:
            c = nx.simple_cycles(newG).next()
        except StopIteration:
            return newG
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
#         if len(newNodeOutEdge) > 0:
#             Gopt.add_edge(newNodeOutEdgeData['origU'],newNodeOutEdgeV, G.get_edge_data(newNodeOutEdgeData['origU'],newNodeOutEdgeV))
        for edgeToAdd in edgesToAdd:
            Gopt.add_edge(edgeToAdd['data']['origU'],edgeToAdd['v'], G.get_edge_data(edgeToAdd['data']['origU'],edgeToAdd['v']))
        
        
        return Gopt
    
    # TODO - Ilan
    
    def test(self):
        return
    
    