from Knn import Knn
import numpy as np
from sklearn.model_selection import train_test_split

class EditedNN:
    def eknn(self, trainSet, k):

        # separate into training and validation sets
        ennSet, val = train_test_split(trainSet, test_size = 0.2, random_state = 0)

        # repeat until performance stops improving on validation set
        prevPerformance = 0.0
        perfImprove = True
        loopCount = len(ennSet)
        while(perfImprove):
            # copy previous enn set
            prevTrain = ennSet.copy()
            
            # loop through training set
            i = 0
            while(i < loopCount):
                # remove ith point from training set b/c it will be test point for knn
                knnTestPoint = ennSet[i]
                tempTrain = np.delete(ennSet, i, 0)   
                # perform knn
                predicted = Knn.knn(tempTrain, knnTestPoint, k, True)
                # check if predicted class and actual class match
                result = self.checkPrediction(predicted, knnTestPoint[-1])
                # if not equal then keep set with removed point
                if result == 0:
                    ennSet = tempTrain
                    loopCount-=1
                else:
                    i+=1
            
            # check performance and only continue if not degrading
            curPerformance = self.checkPerformance(val, tempTrain, k)
            if curPerformance > prevPerformance:
                prevPerformance = curPerformance
            else:
                ennSet = prevTrain
                perfImprove = False
            
        # return edited-nn set
        return ennSet 
   
    # check if predicted class and actual class match
    def checkPrediction(self, predicted, actual):
        if predicted == actual:
            return 1
        else:
            return 0
        
    # check performance on validation set
    def checkPerformance(self, valSet, trainSet, k):
        result = 0
        for i in range(len(valSet)):
            # perform knn
            predicted = Knn.knn(trainSet, valSet[i], k, True)
            # check if predicted class and actual class match
            result += self.checkPrediction(predicted, valSet[i][-1])
        # return percent correctly predicted
        return result/len(valSet)   
    
# testing data
#testClass = np.array([[1, 2, 1], [2, 3, 0], [7, 8, 1], [4, 5, 0], [6, 6, 1], 
#                      [6, 5, 1], [0, 1, 0], [1, 1, 0], [2, 2, 0], [3, 7, 1],
#                      [3, 1, 1], [9, 7, 1], [1, 5, 0], [7, 2, 1], [5, 5, 0]])

#editednn = EditedNN()        
#print(editednn.eknn(testClass, 3))