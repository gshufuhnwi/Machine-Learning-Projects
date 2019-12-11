# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 20:53:30 2019

@author: asadc
"""

import numpy as np
import pandas as pd

#class defined for implementing Naive Bayes algorithm
class NaiveBayes:
    data = 'check'
    def __init__(self):
        #variables to store data respective to classes in the training session and use it in testing
        self.class_list = []                #list with each class instances 
        self.feature_probability = []       #feature probabily list for each class
        self.class_probability = []         #class probability list for each class
        
    #populate the training model with X_train = training features and y_train= class labels for training
    def fit(self, X_train, Y_train):
        test_data = X_train
        #append class as a column to get the subset of data respective to each class
        test_data['class'] = Y_train
        labels = test_data['class'].unique()    #get unique class labels
        labels = np.sort(labels)                #sort labels for easy indexing
        #for each label seperate data belongs to that label and append to class_list
        for x in labels:
            self.class_list.append(test_data[test_data['class'] == x])
        #for each class instances, find the feature and class probability
        for x in self.class_list:
            x = x.drop(['class'], axis = 1)     #drop class column as you don't need it anymore
            count = x.apply(pd.value_counts)    #count all unique values in the class dataset 
                                                #with the unique value as index of count dataset
            count = count.fillna(0)             #fill the null values with 0's in case of no instances of that value
            #apply the probability rule  from the assignment description for each features of class x
            count = (count + 1) / (len(x) + len(x.columns))
            self.feature_probability.append(count)  #save the feature probability dataset of class x
            self.class_probability.append(len(x) / len(test_data))  #save the class probability of class x
            
    def predict(self, X_test):
        predicted_class = []
        #for each row in the testing set find probability for each classes
        for index, row in X_test.iterrows():
            probability_count_list = []     #list of probability count for each classes
            probability_count = 1
            #for each class find the probability of test row
            for x in range(len(self.class_probability)):
                #probability count is set to class probability and will append with each feature probability 
                probability_count = self.class_probability[x]  
                #for each feature, find the probability value of row.feature
                for y in range(len(X_test.columns)):
                    z = row[X_test.columns[y]]      #get the feature value of test row
                    #find the probability of the feature value z from the feature probability dataset of class x 
                    if self.feature_probability[x].index.isin([z]).any(): 
                        #if z is found in the feature probability dataset than multiply with probability count
                        probability_count *= self.feature_probability[x].loc[z][y]
                    else:
                        #if index not found that put the 0 probability means 1 / (class_length + attributes)
                        probability_count *= (1/(len(self.class_list[x]) + len(X_test.columns)))    
                #append the calculated probability for each class
                probability_count_list.append(probability_count)
            #append predicted class with the maximum probaibility count class
            predicted_class.append(probability_count_list.index(max(probability_count_list)))
            
        return predicted_class
        
    def getClasses(self):
        return self.feature_probability
    
    def zero_one_loss_function(self, y_test , y_pred):
        error_count = 0
        for i in range(len(y_test)):
            if y_test[i] != y_pred[i]:          #check if predict matches with original and for 
                                                #nonmatches increment the error count
                error_count +=1
                
        return (error_count/len(y_test))


    def confusion_matrix(self, y_test, y_pred):
        #set to 0.0000001 to protect division by zero. Soybean dataset is very small 
        #and with 10 fold there are only 3 to 5 values which may produce zero division.
        TP = 0.0000001
        TN = 0.0000001
        FP = 0.0000001
        FN = 0.0000001
        #find unique class label for test and pred
        test_label = np.unique(np.array(y_test))
        pred_label = np.unique(np.array(y_pred))
        
        #work with max labels from test and pred
        if len(test_label) >= len(pred_label):
           labels = test_label
        else:
           labels = pred_label
        #find the confusion matrix values   
        for x in labels:
            for y in range(len(y_test)):
                if y_test[y] == y_pred[y] == x:                 
                    TP += 1
                if y_pred[y]== x and y_test[y] != y_pred[y]:
                    FP += 1
                if y_test[y] == y_pred[y] != x:
                    TN += 1
                if y_pred[y] != x and y_test[y] != y_pred[y]:
                    FN += 1
                    
        accuracy = ((TP + TN)/ (TP + TN + FP + FN))
        precision = TP/(FP + TP)
        recall = TP/(FN + TP)
        return accuracy, precision, recall         
        
        
 
