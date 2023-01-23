import pandas as pd
import numpy as np
from random import shuffle
def get_data():
    file_path = 'dataset\dreastcancer.data'
    #Define attribute names for dataframe column
    attributes = ['ID', 'Clump_Thickness','Uniformity','Cell_Shape','Marginal_Adhesion','Epithelial','BareNuclei','Chromatin',
         'Normal_Nucleoli','Mitoses','class']
    
    cancerdata = pd.read_csv(file_path, names= attributes)
    cancerdata.columns = attributes
    cancerdata = cancerdata.drop(['ID'], axis = 1) 
    #replacing missing values with null for making probability distribution easier
    data = cancerdata.replace('?', np.NaN)
    data = probability_distribution_by_column(data)     #call function to replace missing values with P.D
    data['BareNuclei'] = data['BareNuclei'].astype(int) #make datatype int for easy calculaton
    data['class'] = data['class'].map({2:0 , 4:1})  #replace class value label with int starting from 0 (mapping)
    return data

def probability_distribution_by_column(data):
    #only one feature has missing values. apply P.D to generate missing values
    #normalize frequency of unique values in the feature column. e.g. 1: 0.23, 2: 0.33
    p_values = data['BareNuclei'].value_counts(normalize= True)
    #find the missing location in a column
    missing_values = data['BareNuclei'].isnull()
    #generate values equal to the # of missing values with probabily obtained in p_values
    data.loc[missing_values, 'BareNuclei'] = np.random.choice(
            p_values.index, size= len(data[missing_values]), p= p_values.values)
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
