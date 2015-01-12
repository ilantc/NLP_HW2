import model
import math

def main():
    numTrain = 5000
    offset = 0
    trainIterNum = 100
    testOffset = numTrain
    numTest = 1000
    modelFileName = "../models/model_nTrain_" + str(numTrain) + "_trainIterNum_" + str(trainIterNum) + ".model"
    resFileName = "./res_nTtain_" + str(numTrain) + "_trainIterNum_" + str(trainIterNum) + "nTest_" + str(numTest) + ".csv"
    
#     dependencyTreeModel = model.mstModel()
#     dependencyTreeModel.allSentences = dependencyTreeModel.readFile(numTrain,offset)
#     dependencyTreeModel.buildFeatureMapping()    
#     print "num features =",dependencyTreeModel.featuresNum
#     dependencyTreeModel.train(trainIterNum)
#     dependencyTreeModel.save(modelFileName)
#     print "sumW =", sum(dependencyTreeModel.w_f)
#     print "normW =", dependencyTreeModel.getWNorm()
#     allSentences = dependencyTreeModel.readFile(1,offset)
#     (optHeads,_,G) = dependencyTreeModel.chuLiuEdmondsWrapper(allSentences[0])
#     print dependencyTreeModel.calcFeatureVectorPerSentence(allSentences[0], allSentences[0].goldHeads)
#     print dependencyTreeModel.calcFeatureVectorPerSentence(allSentences[0], optHeads)
    
#     print optHeads
#     print "optVal =", dependencyTreeModel.treeVal(G, optHeads)
#     print allSentences[0].goldHeads
#     print "goldVal =", dependencyTreeModel.treeVal(G, allSentences[0].goldHeads)
    
    
    dependencyTreeModel2 = model.mstModel()
    dependencyTreeModel2.load(modelFileName)
    testSentences = dependencyTreeModel2.readFile(numTest, testOffset)
    dependencyTreeModel2.test(testSentences, resFileName)


if __name__ == '__main__':
    main()