import pandas as pd
import numpy as np
from random import shuffle
def get_data():
    file_path = 'dataset\glass.data'
    #Define attribute names for dataframe column
    attributes =  ['RI','Na','Mg','Al','Si','K','Ca','Ba','Fe','class']

    data = pd.read_csv(file_path, names= attributes)   
    #the dataset contains continious values
    #for each fetaures call a function to make the values discrete
    for x in range(len(attributes) - 1):
        data = get_discreate_data_by_column(data, attributes[x])
    #rename class label with int from 0 (integar mapping)
    data['class'] = data['class'].map({1:0 , 2:1, 3:2, 5:3, 6:4, 7:5})
    return data

def get_discreate_data_by_column(data, x):
    #take the feature values and find max and min number to make bins
    column_values = data[x].values
    minimum = min(column_values) - 1    # +1 and -1 so that the max and min values fall inside a bins
    maximum = max(column_values) + 1
    bins = np.linspace(minimum, maximum, num= 11)   #bins is the range from min and max with 10 equally spaced range
    lebels = np.linspace(0, 9, num= 10)     #for 10 bins assign 10 values from 0-9 
    #replace the values in feature with the label obtained from the bins. ex. 0.25 falls in 2nd bin. Replace o.25 with 1.
    data[x] = pd.cut(data[x], bins, labels= lebels)     
    data[x] = data[x].astype(int)   #make the datatype int for easy calculation
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
        column_data = data[column].values
        data = data.drop([column], axis=1)
        shuffle(column_data)
        data[column] = column_data
    return data

data = get_data_with_noise()