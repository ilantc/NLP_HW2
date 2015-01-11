import model
import math

def main():
    numTrain = 5000
    offset = 0
    trainIterNum = 100
    modelFileName = "./model_nTrain_" + str(numTrain) + "_trainIterNum_" + str(trainIterNum) + ".model"
     
    dependencyTreeModel = model.mstModel()
    dependencyTreeModel.allSentences = dependencyTreeModel.readFile(numTrain,offset)
    dependencyTreeModel.buildFeatureMapping()    
    print "num features =",dependencyTreeModel.featuresNum
    dependencyTreeModel.train(trainIterNum)
    dependencyTreeModel.save(modelFileName)
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
    
    dependencyTreeModel2 = model.mstModel()
    dependencyTreeModel2.load(modelFileName)
    (optHeads,_,G) = dependencyTreeModel2.chuLiuEdmondsWrapper(allSentences[0])
    
    print optHeads

if __name__ == '__main__':
    main()