# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:54:22 2019

@author: asadc
"""
'''
Stacked Auto-encoder (SAE) class takes a network architecure 
as a list (e.g. [19, 15, 10, 15, 7] : number represents nodes in each layer)
and uses MLP class to train each hidden layer with unsupervised learning(where 
input layer and output layer are the same). Finally used the individual training 
weight of each layer to test the performance of the whole network.
'''
import numpy as np
import MLP
import Metrics as mt


class SAE:
        
        def __init__(self, architecture_list):
                self.architecture = architecture_list
                self.number_of_layer = len(architecture_list)
                self.biases = []
                self.weights = []
                
        def train(self, x_train, x_label, epoch, batch_size, eta, isClassification= True, smoothing= False):
                #train input and first hidden layer with unsupervised learning
                network = MLP.MLP([self.architecture[0], self.architecture[1], self.architecture[0]])
                epoc, result = network.train(x_train, x_train, epoch, batch_size, eta)
                #store the trained weights and biases of the first layer
                self.weights.append(network.getWeights()[0])
                self.biases.append(network.getBiases()[0])
                #train each hidden layer using unsupervised learning
                for x in range(self.number_of_layer - 3):
                        network = MLP.MLP([self.architecture[x+1], self.architecture[x+2], self.architecture[x+1]])
                        hidden_nodes = np.asarray([network.feed_forward(x, self.biases, self.weights) for x in x_train])
                        epoc, result = network.train(hidden_nodes, hidden_nodes, epoch, batch_size, eta)
                        #store trained weights and biases of each hidden layer
                        self.weights.append(network.getWeights()[0])
                        self.biases.append(network.getBiases()[0])                        
                #train prediced output layer by taking the last hidden layer and
                #use supervised learning(input layer and output layer is different)
                hidden_nodes = np.asarray([network.feed_forward(x, self.biases, self.weights) for x in x_train])
                network1 = MLP.MLP([self.architecture[-2], self.architecture[-1]])
                epoc1, result1 = network1.train(hidden_nodes, x_label, epoch, batch_size, eta)
                #store trained weights and biases of predicted layer
                self.weights.append(network1.getWeights()[0])
                self.biases.append(network1.getBiases()[0])
                
                #smoothing the whole trained network with backpropagation if smooting 
                #parameter is set to true to see if it generates better results
                if smoothing:
                        network = MLP.MLP(self.architecture)
                        network.setBiases(self.biases)
                        network.setWeights(self.weights)
                        #uses minimal number of epoch to reduce vanishing gradient 
                        #descent problem
                        network.train(x_train, x_label, 50, batch_size, eta)
                        self.biases = network.getBiases()
                        self.weights = network.getWeights()
                        
        
        def test(self, x_test, isClassification= True):
                #test the model with test set and return predicted output for classification or regression.
                network = MLP.MLP(self.architecture)
                #set weights and biases based on SAE weights and biases
                network.setBiases(self.biases)
                network.setWeights(self.weights)
                return network.test(x_test, isClassification)
        
        
        
