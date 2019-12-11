# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 15:09:33 2019

@author: asadc
"""
import LoadDataset as ld
import Knn
import EditedNN
import Kmeans
import PAM
import cnn
import Metrics
import pandas as pd
class Main:
        def __init__(self):
                #define variable to use inside class which may need tuning
                self.splitlength = 0.75
                self.editedNN_k_value = 3
                self.knn_k_values = [3, 5 , 7]
                
                self.alldataset = ld.LoadDataset().load_data()          #load all dataset
                #check dataset is classification
                self.IsClassificationDict = ld.LoadDataset().IsClassificationDict() 
                #define dataframe to store all the results
                self.allresults = pd.DataFrame(columns=['dataset', 'isClassification', 'k', 'method',
                                                        'accuracy', 'precision', 'recall', 'RMSE'])
                
        def main(self):
                for dataset in self.alldataset:         #for each dataset call each algorithm
                        print('current dataset ::: {0} \n'.format(dataset))
                        data = self.alldataset.get(dataset)
                        isClassification = self.IsClassificationDict.get(dataset)
                        k_for_cluster = 0                       #define k value for cluster                        
                        for k in self.knn_k_values:
                                trainset, testset = self.testtrainsplit(data, self.splitlength)
                                #call knn
                                predicted, labels = self.knn(trainset, testset, k, isClassification)
                                self.performance_measure(predicted, labels, dataset, isClassification, k, 'KNN')
                                #call edited_nn
                                if isClassification:                                        
                                        k_for_cluster, predicted, labels = self.edited_nn(
                                                        trainset, testset, k, isClassification)
                                        self.performance_measure(predicted, labels, dataset, isClassification, k, 'E-NN')
                                        #call CNN
                                        predicted, labels = self.condensed_nn(trainset, testset, k, isClassification)
                                        self.performance_measure(predicted, labels, dataset, isClassification, k, 'C-NN')
                                else:
                                        k_for_cluster = int(len(trainset) / 4)  #regression 1/4 n as k
                                #call Kmeans
                                predicted, labels = self.kmeans(trainset, testset, k, k_for_cluster, isClassification)
                                self.performance_measure(predicted, labels, dataset, isClassification, k, 'Kmeans')
                                #call PAM
                                predicted, labels = self.pam(trainset, testset, k, k_for_cluster, isClassification)
                                self.performance_measure(predicted, labels, dataset, isClassification, k, 'PAM')
                                
                return self.allresults
        
        def testtrainsplit(self, data, foldlen):
                data = data.sample(frac=1)                   #randomize the rows to avoid sorted data
                testlen = int(len(data) * foldlen)           #split according to fold lenth
                testset = data[testlen:]
                trainset = data[:testlen]
                return trainset, testset
        
        def knn(self, trainset, testset, k, isClassification):
                predicted = Knn.Knn().fit(trainset.values, testset, k, isClassification)
                return predicted, testset.iloc[:, -1]   #return predicted and actual labels
        
        def edited_nn(self, trainset, testset, k, isClassification):
                #get the reduced dataset using edited nn
                reduced_dataset = EditedNN.EditedNN().eknn(trainset.values, self.editedNN_k_value)
                #call knn with the reduced train set
                predicted = Knn.Knn().fit(reduced_dataset, testset, k, isClassification)
                return len(reduced_dataset), predicted, testset.iloc[:, -1]   #return predicted and actual labels
        def condensed_nn(self, trainset, testset, k, isClassification):
                #get the reduced dataset using condensed nn
                reduced_dataset = cnn.Cnn().getReducedDataset(trainset)
                #call knn with the reduced train set
                predicted = Knn.Knn().fit(reduced_dataset.values, testset, k, isClassification)
                return predicted, testset.iloc[:, -1]   #return predicted and actual labels
        
        def kmeans(self, trainset, testset, k, k_for_cluster, isClassification):
                km = Kmeans.Kmeans(k_for_cluster, trainset)
                #centroids = km.converge()
                centroids_class = km.getClusters()
                centroids_class = centroids_class[testset.columns]
                #call knn with the reduced train set- Centroids
                predicted = Knn.Knn().fit(centroids_class.values, testset, k, isClassification)
                return predicted, testset.iloc[:, -1]   #return predicted and actual labels
        
        def pam(self, trainset, testset, k, k_for_cluster, isClassification):
                pm = PAM.PAM(k_for_cluster, trainset)
                medoids_class = pm.getClusters()
                print("medoids received")
                medoids_class = medoids_class.drop(columns=["cluster","cost"])
                medoids_class = medoids_class[testset.columns]
                predicted = Knn.Knn().fit(medoids_class.values, testset, k, isClassification)
                return predicted, testset.iloc[:, -1]
        
        def performance_measure(self, predicted, labels, dataset, isClassification, k, method):
                mtrx = Metrics.Metrics()
                if (isClassification):
                        acc, prec, recall = mtrx.confusion_matrix(labels.values, predicted)
                        self.update_result(dataset, isClassification, k, method, acc, prec, recall, 0)
                         
                else:
                        rmse = mtrx.RootMeanSquareError(labels.values, predicted)
                        self.update_result(dataset, isClassification, k, method, 0, 0, 0, rmse)
        
        def update_result(self, dataset, isClassification, k, method, acc, prec, recall, rmse):
                self.allresults = self.allresults.append({'dataset': dataset, 'isClassification': isClassification,
                                                'k': k, 'method': method, 'accuracy': acc, 'precision': prec,
                                                'recall': recall, 'RMSE': rmse}, ignore_index=True)
        
        
results = Main().main()
results.to_csv('results.csv')