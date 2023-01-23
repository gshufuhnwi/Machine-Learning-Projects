import pandas as pd
import numpy as np
from random import shuffle
def get_data():
    file_path = 'dataset\iris.data'
    #Define attribute names for dataframe column
    attributes = ['slength', 'swidth', 'plength', 'pwidth' ,
                  'class', 'label']

    data = pd.read_csv(file_path, names= attributes)
    #drop the class with name
    data = data.drop(['class'], axis = 1)
    #assign the label column as class
    data.columns.values[4] = "class"
   
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