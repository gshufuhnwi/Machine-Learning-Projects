
"""

1: medoids are randomly selected from dataSet in initMedoids()
2: eachPoint in the data set is assigned to a medoid in the generateClusters() using the euclideanDistance()
3: the total distance for each medoid to the rest of the points in the cluster is set in setInitialDistances()
4: medoids are updated by "swapping" each point in the cluster and calculating the total distance in updateMedoids()
    if the cost is lower, the new point will be remembered. This is repeated for each point and the point with the lowest
    cost becomes the new medoid.
5: generateClusters() and updateMedoids() are called repeatedly until convergence or stopping condition
"""
import numpy as np
import pandas as pd
import sys
import Metrics

class PAM:

    def __init__(self, k, dataSet):
        self.k = k
        self.original_dataset = dataSet
        self.dataSet = dataSet
        #self.dataSet = dataSet.drop(dataSet.columns[-1], axis = 1)
        self.dataSet["cluster"] = -1
        self.dataSet["cost"] = -1
        self.medoids = pd.DataFrame(columns=self.dataSet.columns)
        self.initMedoids(self.k)
        self.generateClusters()
        self.setInitialDistances()
        self.updateMedoids()
        print("update finished")
    
    def initMedoids(self, k):
        for i in range(k): # init k medoids
            row = np.random.randint(0, len(self.dataSet))
            medoids = self.medoids
            medoid = self.dataSet.iloc[row,:]
            medoid["cluster"] = i
            medoid["cost"] = sys.maxsize 
            self.medoids = self.medoids.append(medoid)
            self.medoids.reset_index(inplace=True, drop=True)
            self.dataSet = self.dataSet.drop(self.dataSet.index[row])
            self.dataSet.reset_index(inplace=True, drop=True)
        medoids = self.medoids
        print(medoids.head(3))

    def generateClusters(self): #euclidean distance will be used to initially assign each point to its cluster and medoid
        medoids = self.medoids
        for i in range(len(self.dataSet)):   #iterate through each point in the data set
            row = self.dataSet.iloc[i, :]   #get row at index i
            distance = sys.maxsize
            for index, medoid in self.medoids.iterrows(): #compare the distance of each point to each of the centroid
                print("point " + str(i) + " medoid : " + str(index))
                new_distance = Metrics.Metrics().euclideanDistance(row, medoid, (len(medoid) - 3))
                if new_distance < distance :    #if new distance is shorter, put row in the new cluster
                    row["cluster"] = medoid["cluster"]
                    distance = new_distance #update the distance for next comparison
            self.dataSet.loc[self.dataSet.index[i], "cluster"] = row["cluster"]
         
    def setInitialDistances(self):
        for medoid_index, medoid in self.medoids.iterrows():
            cluster = self.dataSet.loc[self.dataSet["cluster"] == medoid_index]
            if len(cluster) > 0: #make sure there is at least one point in the cluster, otherwise distance will remain sys.maxsize
                distance = 0
                for cluster_index, row in cluster.iterrows():
                    print(cluster_index)
                    distance += self.sumOfSquares(medoid,row)
                self.totalCost(cluster,medoid,len(cluster)  +1 )
                distance = distance / len(cluster)
                medoid["cost"] = distance

    def updateMedoids(self):
        new_medoids = pd.DataFrame()
        for medoid_index, medoid in self.medoids.iterrows(): #get the index and medoid from the medoids data frame 
            cluster = self.dataSet.loc[self.dataSet["cluster"] == medoid_index ] #get all points in cluster from the data set
            print("current cluster : " + str(medoid_index))
            if len(cluster) > 0: #ensure there are points in the cluster
                self.dataSet = self.dataSet[self.dataSet.cluster != medoid_index] #cluster must be dropped from data set for comparison. will be re-added 
                cluster.reset_index(inplace=True, drop=True) #reset index since rows grabbed might not have been sequential
                shortest_index = -1
                shortest_distance = medoid["cost"] #save existing medoid total distance as shortest distance
                for cluster_index, row in cluster.iterrows():
                    print("current cluster row : " + str(cluster_index))
                    new_distance = self.sumOfSquares(row, medoid) #start by getting distance to medoid
                    new_distance += self.totalCost(cluster, row, cluster_index)
                    new_distance = new_distance / (len(cluster) + 1) #divide distance by the cluster length plus medoid since medoid will be a point
                    if new_distance < shortest_distance:
                        shortest_index = cluster_index
                        shortest_distance = new_distance
                #update cluster and new medoids
                if shortest_index != -1: #ensure new medoid is not current medoid
                    new_medoid = cluster.iloc[shortest_index, :]
                    cluster = cluster.drop(cluster.index[shortest_index])
                    new_medoid["cost"] = shortest_distance
                    new_medoids = new_medoids.append(new_medoid)
                    cluster = cluster.append(medoid)
                else:
                    new_medoids = new_medoids.append(medoid) #keep old medoid if no other points had a shorter distance
                self.dataSet = self.dataSet.append(cluster)
                self.dataSet.reset_index(inplace=True,drop=True)
            else: #keep old medoid if there were no points in cluster
                new_medoids = new_medoids.append(medoid)
        self.medoids = new_medoids
        self.dataSet["cost"] = -1
        self.medoids.reset_index(inplace=True,drop=True)

    def converge(self):
        previous_cluster_assignment = self.dataSet["cluster"]
        # imitate do while loop
        count = 0
        while True:
            self.updateMedoids()
            print("updating clusters") #medoids need to be updated for new cluster assignments
            self.generateClusters()
            if(previous_cluster_assignment.equals(self.dataSet["cluster"]) or count == 3): #check to see if assignments have changed
                break
            else:
                previous_cluster_assignment = self.dataSet["cluster"] #previous cluster assignments become current if cluster assignments were updated
                count += 1
                print(count)
        return self.medoids
    
    def sumOfSquares(self, point1, point2):
        distance = 0
        for i in range(len(point1) - 3): #subtract 2 so that "cost" and "cluster" are not used in distance calculation
            distance += np.power((point1[i] - point2[i]),(2))
        return distance
    
    def totalCost(self, cluster, row, row_index):
        distance = 0
        for i in range(len(cluster)): #calculate distance of current row against all other points in the cluster.
            print(i)
            if i != row_index:
                distance += self.sumOfSquares(row,cluster.iloc[i,:])
        return distance
    
    def getClusters(self):
        self.converge()
        return self.medoids
            