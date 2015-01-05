import model



def main():
    dependencyTreeModel = model.mstModel()
    
    dependencyTreeModel.allSentences = dependencyTreeModel.readFile(1)
    dependencyTreeModel.buildFeatureMapping()    
    trainIterNum = 1
    dependencyTreeModel.train(trainIterNum)

if __name__ == '__main__':
    main()