import pandas as pd
import numpy as np
from random import shuffle

def get_data():
    file_path = 'dataset\house-votes-84.data'
    #Define attribute names for dataframe column
    attributes = ['class', 'handicapped-infants', 'water-project-cost-sharing',
                  'adoption-of-the-budget-resolution', 'physician-fee-freeze',
                  'el-salvador-aid', 'religious-groups-in-schools', 
                  'anti-satellite-test-ban', 'aid-to-nicaraguan-contras', 'mx-missile',
                  'immigration', 'synfuels-corporation-cutback', 'education-spending', 
                  'superfund-right-to-sue', 'crime', 'duty-free-exports', 
                  'export-administration-act-south-africa']
    data = pd.read_csv(file_path, names= attributes)
    #make dataset numerical with class name 'democrat':1 and 'Republican': 0
    #also replace the '?' sign value with another interger type 2 as they do not represent missing values
    data = data.replace('y', 1).replace('n' , 0).replace('?', 2).replace('democrat', 1).replace('republican', 0)
    return data


def get_data_with_noise():
    data = get_data()
    #choose 10% attributes for randomization
    no_of_feature = int(len(data.columns) * 0.1 + 1) #takes the ceiling value
    choice = np.arange(1, len(data.columns)) #0 is the class column
    noise_features = np.random.choice(choice, size= no_of_feature) #random choose #feature for data randomization
    for x in noise_features:    #for each feature shuffle the data in that feature 
        column = data.columns[x]
        column_data = data[column]
        data = data.drop([column], axis=1) #drop the origial feature and append shuffled feature
        shuffle(column_data)
        data[column] = column_data
    return data


    