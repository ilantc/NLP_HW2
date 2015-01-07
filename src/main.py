import model
import math



def main():
    numTrain = 1
    dependencyTreeModel = model.mstModel()
    dependencyTreeModel.allSentences = dependencyTreeModel.readFile(numTrain)
    dependencyTreeModel.buildFeatureMapping()    
    trainIterNum = 20
    dependencyTreeModel.train(trainIterNum)
    print "sumW =", sum(dependencyTreeModel.w_f)
    print "normW =", math.sqrt(sum([w_i * w_i for w_i in dependencyTreeModel.w_f]))
    allSentences = dependencyTreeModel.readFile(1)
    
    (optHeads,_) = dependencyTreeModel.chuLiuEdmondsWrapper(allSentences[0])
    print optHeads
    print allSentences[0].goldHeads

if __name__ == '__main__':
    main()