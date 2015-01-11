import model
import math

def main():
    numTrain = 1000
    offset = 1
    dependencyTreeModel = model.mstModel()
    dependencyTreeModel.allSentences = dependencyTreeModel.readFile(numTrain,offset)
    dependencyTreeModel.buildFeatureMapping()    
    trainIterNum = 80
    print "num features =",dependencyTreeModel.featuresNum
    dependencyTreeModel.train(trainIterNum)
    print "sumW =", sum(dependencyTreeModel.w_f)
    print "normW =", dependencyTreeModel.getWNorm()
    allSentences = dependencyTreeModel.readFile(1,offset)
    (optHeads,_,G) = dependencyTreeModel.chuLiuEdmondsWrapper(allSentences[0])
    print dependencyTreeModel.calcFeatureVectorPerSentence(allSentences[0], allSentences[0].goldHeads)
    print dependencyTreeModel.calcFeatureVectorPerSentence(allSentences[0], optHeads)
    
    print optHeads
    print "optVal =", dependencyTreeModel.treeVal(G, optHeads)
    print allSentences[0].goldHeads
    print "goldVal =", dependencyTreeModel.treeVal(G, allSentences[0].goldHeads)
    

if __name__ == '__main__':
    main()