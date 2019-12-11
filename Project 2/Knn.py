import numpy as np
from statistics import mean, mode, StatisticsError 
import Metrics

# function parameters: trainng dataset, test point, number of neighbors k, classification/regression T/F
class Knn:
    @staticmethod
    def knn(trainSet, testPoint, k, classification):
        # store indices and distances in 2D array
        distances = np.zeros(shape=(len(trainSet), 2))

        # loop through training set to find distances between test point and each training set point
        for i in range(len(trainSet)):    
            # update to use our own distance metric
            #curDist = np.linalg.norm(testPoint[:-1]-trainSet[i,:-1])
            curDist = Metrics.Metrics().euclideanDistance(testPoint, trainSet[i], (len(testPoint) - 1))
            distances[i][0] = i
            distances[i][1] = curDist
   
        # sort by distance and subset to k neighbors' response values
        sortedDist = sorted(distances, key=lambda x: x[1])
        neighbors = np.zeros(k)
        for i in range(k):
            neighbors[i] = trainSet[int(sortedDist[i][0])][-1]
        
        # return predicted class or regression value
        return Knn.predict(neighbors, classification, trainSet, testPoint, k)

    # predict response variable from neighbors
    def predict(neighbors, classification, trainSet, testPoint, k):
        # choose most popular class for classification
        if classification:
            # in case of tie, repeatedly run knn with k-1 until most popular class is found
            try:
                return int(mode(neighbors))
            except StatisticsError:
                return Knn.knn(trainSet, testPoint, k-1, True)

        # find average of neighbors for regression
        else:
            return mean(neighbors)
    def fit(self, trainset, testset, k, classification):
            predicted = []
            for index, x in testset.iterrows():
                    predicted.append(Knn.knn(trainset, x, k, classification))
            return predicted

# testing data
#testClass = np.array([[1, 2, 0], [2, 3, 1], [7, 8, 2], [6, 5, 1]])
#testClassPoint = np.array([7, 7, 0])
#testReg = np.array([[3.1, 2.1, 9.3], [1.1, 1.1, 0], [9.1, 8.1, 9.7], [7.1, 5.1, 3.3]])
#testRegPoint = np.array([9.1, 9.1, 0])

#print(Knn.knn(testClass, testClassPoint, 4, True))
#print(Knn.knn(testReg, testRegPoint, 3, False))
#k = 2
#tempTrain = np.array([[2, 3, 1], [1, 2, 0], [6, 5, 1]])
#knnTestPoint = [6, 5, 1] 
#print(Knn.knn(tempTrain, knnTestPoint, k, True))