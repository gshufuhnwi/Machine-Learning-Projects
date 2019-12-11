# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 12:00:05 2019

@author: asadc
"""

import matplotlib.pylab as plt

def plot_graph(title, accuracy, noisy_accuracy):
    plt.figure()
    plt.plot(accuracy, label= "w/o noise")
    plt.plot(noisy_accuracy, label= "w noise")
    
    plt.legend(loc= 'lower left')
    
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel("Number of folds")
    plt.ylabel("Accuracy")
    plt.savefig('result/zero_one/' + title + '.png')
    #plt.show()
    #plt.close()
    