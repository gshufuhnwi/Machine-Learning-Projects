# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:38:59 2019

@author: asadc
"""

import pandas as pd
import numpy as np
from random import shuffle
def get_data():
    file_path = 'dataset\soybean-small.data'
    #Define attribute names for dataframe column
    attributes = ['date', 'plant_stand', 'precip', 'temp', 'hail', 'crop-hist', 'area-damaged',
                  'severity', 'seed-tmt', 'germination', 'plant-growth', 'leaves', 
                  'leafspots-halo', 'leafspots-marg', 'leafspot-size', 'leaf-shread',
                  'leaf-malf', 'leaf-mild', 'stem', 'lodging', 'stem-cankers', 'canker-lesion',
                  'fruiting-bodies', 'external decay', 'mycelium', 'int-discolor', 'sclerotia',
                  'fruit-pods', 'fruit spots', 'seed', 'mold-growth', 'seed-discolor', 'seed-size',
                  'shriveling', 'roots', 'class' ]

    data = pd.read_csv(file_path, names= attributes)
    #rename class label with int from 0 (integar mapping)
    data = data.replace('D1', 0).replace('D2', 1).replace('D3', 2).replace('D4', 3) 
   
    return data

def get_data_with_noise():
    data = get_data()
    #this part is same as the vote dataset noise generation
    #choose 10% attributes for randomization
    no_of_feature = int(len(data.columns) * 0.1 + 1) #takes the ceiling value
    choice = np.arange(0, (len(data.columns) - 1)) #last column is the class column
    noise_features = np.random.choice(choice, size= no_of_feature)
    for x in noise_features:
        column = data.columns[x]
        column_data = data[column]
        data = data.drop([column], axis=1)
        shuffle(column_data)
        data[column] = column_data
    return data

#data = get_data_with_noise()