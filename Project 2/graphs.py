# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 12:00:05 2019

@author: asadc
"""

import matplotlib.pylab as plt


def plot_graph(title, metric, k, isClassification):
    plt.figure()
    for item in metric:
            
            plt.plot(k, metric.get(item), label= item)
    
    plt.legend(loc= 'lower left')
    
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel("Number of K")
    if isClassification:
            plt.ylabel("Accuracy")
    else:
            plt.ylabel("N-RMSE")
                    
    #plt.savefig('graphs/' + title + '.png')
    plt.show()
    plt.close()
    
    
def process_result(results):
        algorithms = results.method.unique()
        metric_reg = {}
        metric_cla = {}
        for item in algorithms:
                list_c = []
                list_r = []
                result = results[results['method'] == item]
                for index, row in result.iterrows():
                        if row['isClassification']:
                                
                                metric_cla[row['dataset']] = row['accuracy']
                        else:
                                metric_reg[row['dataset']] = row['RMSE']
                                
                plot_graph(item, metric_cla, [3,5,7], True)
                plot_graph(item, metric_reg, [3,5,7], False)
                        
                        
import pandas as pd

result = pd.read_csv('results.csv')                     
    
                        
                        
import pandas as pd

result = pd.read_csv('results.csv') 
process_result(result)                    
    