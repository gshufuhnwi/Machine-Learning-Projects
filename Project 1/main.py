from sklearn.model_selection import train_test_split
from sklearn import metrics
from classifier import NaiveBayes
import numpy as np
import pandas as pd
import graphs
import soybean_data as sb
import vote_data as vd
import breastcancer_dataset as bsd
import iris_data as iris
import glass_data as glass

def print_both(file, printstr):         #function to both print in file and output txt
        print(printstr)
        file.write(printstr)

result_set = {}     #dict to store the 0-1 accuracy for each dataset
CF_acc_result_set = {}  #dict to store CF's accuracy, precision, score    
CF_prec_result_set = {}
CF_recall_result_set = {}
all_dataset = {}    #dict to store each dataset and dataset with noise
all_dataset.update({'Vote dataset' : vd.get_data()})
all_dataset.update({'Vote dataset with noise' : vd.get_data_with_noise()})
all_dataset.update({'Soybean dataset' : sb.get_data()})
all_dataset.update({'Soybean dataset with noise' : sb.get_data_with_noise()})
all_dataset.update({'Breast Cancer dataset' : bsd.get_data()})
all_dataset.update({'Breast Cancer dataset with noise' : bsd.get_data_with_noise()})
all_dataset.update({'Iris dataset' : iris.get_data()})
all_dataset.update({'Iris dataset with noise' : iris.get_data_with_noise()})
all_dataset.update({'Glass dataset' : glass.get_data()})
all_dataset.update({'Glass dataset with noise' : glass.get_data_with_noise()})

file=open("output.txt", "w+")           #print output to this file

#train and test naive bayes class for all dataset
for dataset in all_dataset:
    printstr = "\n\nCurrent Dataset ::: {0}".format(dataset)
    print_both(file, printstr)
    data = all_dataset[dataset]     #get single dataset
    accuracy_list = []              #list to store 0-1 accuracy for 10-fold validation
    CF_accuracy_list = []           #list to store CF accuracy
    CF_precision_list = []
    CF_recall_list = []
    #10-fold cross validation
    data = data.sample(frac=1)      #randomize the rows to avoid sorted data
    folds = np.array_split(data, 10)        #make 10 folds in the dataset
    test_set = 0                            #define test_set
    #for each folds treat one fold as test set and 9 fols at train set
    for y in range(len(folds)):
        X_train = pd.DataFrame()
        #if not test-set append fold in the train set
        for x in range(len(folds)):
            if x == test_set:
                y_test = folds[x]['class'].values
                X_test = folds[x].drop(['class'], axis=1)
            else:
                X_train = X_train.append(folds[x])
                
        y_train = X_train['class'].values
        X_train = X_train.drop(['class'], axis=1)
        nb = NaiveBayes()               #initialize Naive Bayes Classifier
        nb.fit(X_train, y_train)        #train model with train data
        y_pred = nb.predict(X_test)     #test model with test set
        #find error with respect to zero-one loss function
        error = nb.zero_one_loss_function(y_test, y_pred)
        printstr = "\nAccuracy of 0-1 loss for fold {0} ::: {1}".format( y , (1- error))
        print_both(file, printstr)
        accuracy_list.append((1- error))
        #get mean square error
        acc, precision, recall = nb.confusion_matrix(y_test, y_pred)
        printstr = "\nCF for fold {0} ::: acc:: {1} :: precision:: {2} :: recall :: {3}".format( y , acc, precision, recall)
        print_both(file, printstr)
        CF_accuracy_list.append(acc)
        CF_precision_list.append(precision)
        CF_recall_list.append(recall)
        test_set += 1                   #increment test_set to set for the next fold
    result_set.update({dataset: accuracy_list})
    CF_acc_result_set.update({dataset: CF_accuracy_list})
    CF_prec_result_set.update({dataset: CF_precision_list})
    CF_recall_result_set.update({dataset: CF_recall_list})


#express accuracy in terms of graph
result_inorder = sorted(result_set.keys())
#increment x by 2 to get the actual and noise dataset graph for each dataset
for i in range(0, (len(result_inorder) - 1), 2):               
    graphs.plot_graph(result_inorder[i], result_set[result_inorder[i]], result_set[result_inorder[i + 1]])
    
#print the average accuracy (10-fold) for each dataset
for dataset in result_set:
        printstr = '\n\nFor {0} : avg accuracy for 0-1 is :: {1}'.format(dataset, (sum(result_set[dataset]))/len(result_set[dataset]))
        print_both(file, printstr)
        #for CF count the avg value for all dataset
        avg_acc = sum(CF_acc_result_set[dataset])/len(CF_acc_result_set[dataset])
        avg_prec = sum(CF_prec_result_set[dataset])/len(CF_prec_result_set[dataset])
        avg_recall = sum(CF_recall_result_set[dataset])/len(CF_recall_result_set[dataset])
        printstr = '\nFor  {0} : CFs average accuracy :: {1} :: precision :: {2} :: recall :: {3}'.format(dataset, avg_acc, avg_prec, avg_recall)
        print_both(file, printstr)        
file.close()
    



