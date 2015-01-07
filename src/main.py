import model



def main():
    numTrain = 30
    dependencyTreeModel = model.mstModel()
    dependencyTreeModel.allSentences = dependencyTreeModel.readFile(numTrain)
    dependencyTreeModel.buildFeatureMapping()    
    trainIterNum = 2
    dependencyTreeModel.train(trainIterNum)
    
    allSentences = dependencyTreeModel.readFile(1,numTrain)
    
    (optHeads,_) = dependencyTreeModel.chuLiuEdmondsWrapper(allSentences[0])
    print "done!"
    print optHeads

if __name__ == '__main__':
    main()