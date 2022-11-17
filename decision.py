from math import log
from collections import defaultdict

def calculateEntropy(dataset):
    counter= defaultdict(int)
    for record in dataset:      
        label = record[-1] 
        counter[label] += 1
    entropy = 0.0
    for key in counter:
        probability = counter[key]/len(dataset) 
        entropy -= probability * log(probability,2)
    return entropy

def splitDataset(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataset):
    baseEntropy = calculateEntropy(dataset)
    bestInfoGain = 0.0; bestFeature = -1
    
    numFeat = len(dataset[0]) - 1   
    for indx in range(numFeat):
        featValues = {record[indx] for record in dataset}
        featEntropy = 0.0
        for value in featValues:
            subDataset = splitDataset(dataset, indx, value)
            probability = len(subDataset)/float(len(dataset))
            featEntropy += probability * calculateEntropy(subDataset)

        infoGain = baseEntropy - featEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = indx
    return bestFeature


def createTree(dataset, features):
    labels = [record[-1] for record in dataset]
    
    if labels.count(labels[0]) == len(labels):
        return labels[0]
    if len(dataset[0]) == 1:
        mjcount = max(labels,key=labels.count)
        return (mjcount) 
    
    bestFeat = chooseBestFeatureToSplit(dataset)
    bestFeatLabel = features[bestFeat]
    featValues = {record[bestFeat] for record in dataset}
    subLabels = features[:]
    del(subLabels[bestFeat])
    
    myTree = {bestFeatLabel:{}}
    for value in featValues:
        subDataset = splitDataset(dataset, bestFeat, value)
        subTree = createTree(subDataset, subLabels)
        myTree[bestFeatLabel].update({value: subTree})
    return myTree                            


def predict(inputTree, features, testVec):
    
    def classify (inputTree, testDict):
        (key, subtree), = inputTree.items()
        testValue = testDict.pop(key)
        if len(testDict) == 0:
            return subtree[testValue]
        else:
            return classify(subtree[testValue], testDict)
            
    testDict = dict(zip(features, testVec))
    return classify(inputTree, testDict)