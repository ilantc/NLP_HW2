import model
import math

def main():
    numTrain = 1
    offset = 5
    dependencyTreeModel = model.mstModel()
    dependencyTreeModel.allSentences = dependencyTreeModel.readFile(numTrain,offset)
    dependencyTreeModel.buildFeatureMapping()    
    trainIterNum = 100
    dependencyTreeModel.train(trainIterNum)
    print "sumW =", sum(dependencyTreeModel.w_f)
    print "normW =", math.sqrt(sum([w_i * w_i for w_i in dependencyTreeModel.w_f]))
    allSentences = dependencyTreeModel.readFile(1,offset)
    
    (optHeads,_,G) = dependencyTreeModel.chuLiuEdmondsWrapper(allSentences[0])
    print optHeads
    print "optVal =", dependencyTreeModel.treeVal(G, optHeads)
    print allSentences[0].goldHeads
    print "goldVal =", dependencyTreeModel.treeVal(G, allSentences[0].goldHeads)
    

if __name__ == '__main__':
    main()