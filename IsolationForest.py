# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 01:05:36 2020

@author: Gerard
"""
##from keras.utils import to_categorical
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score

columns = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land"
           ,"wrong_fragment","urgent","hot","num_failed_logins","logged_in",
           "num_compromised","root_shell","su_attempted","num_root","num_file_creation",
           "num_shells","num_access_files","num_outbound_cmds","is_host_login",
           "is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
           "rerror_rate","srv_rerror_rate",
           "same_srv_rate","diff_host_rate","srv_diff_host_rate","dst_host_count",
           "dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
           "dst_host_same_src__port_rate","dst_host_srv_diff_host_rate",
           "dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate",
           "dst_host_srv_rerror_rate","label"]

df = pd.read_csv("kddcup.data.corrected", names = columns, index_col=None)
df = df[df["service"] =="http"]

df = df.drop("service", axis = 1)

df["label"].value_counts()

df["label"].value_counts().plot(kind = "bar", rot = 45)

print(df.dtypes)

for col in df.columns:
    if df[col].dtype == "object":
        encoded = LabelEncoder()
        df[col] = encoded.fit_transform(df[col])
        #df[col] =  to_categorical(df[col])


for i in range(0, 3):
    
    df = df.iloc[np.random.permutation(len(df))]
df1 = df[:500000]
df_validate = df[500000:]
labels = df1["label"]

## Split data

x_train, x_test, y_train, y_test = train_test_split(df1, labels, test_size = 0.2,random_state=42)

x_val, y_val = df_validate, df_validate["label"]


## Fit Model

Isolation_forest = IsolationForest(n_estimators=100, max_samples = 256, contamination=0.04, random_state=42)

Isolation_forest.fit(x_train)

### Calculating Anomaly score

anomaly_scores = Isolation_forest.decision_function(x_val)
plt.figure(figsize=(15, 10))
plt.hist(anomaly_scores, bins = 100)
plt.xlabel('Average Path Lengths', fontsize=14)
plt.ylabel('Number of Data Points', fontsize = 14)
plt.show()

### AUC

anomalies = anomaly_scores>-0.19

matches = y_val == list(encoded.classes_).index("normal.")

auc = roc_auc_score(anomalies, matches)

print("AUC: {:.2%}".format(auc))

## Test Set

anomaly_scores_test = Isolation_forest.decision_function(x_test)
plt.figure(figsize=(15, 10))
plt.hist(anomaly_scores_test, bins = 100)
plt.xlabel('Average Path Lengths', fontsize=14)
plt.ylabel('Number of Data Points', fontsize = 14)
plt.show()

anomalies_test = anomaly_scores_test>-0.19

matches = y_test == list(encoded.classes_).index("normal.")

auc_test = roc_auc_score(anomalies_test, matches)

print("AUC: {:.2%}".format(auc_test))


## Selecting Smtp

df = pd.read_csv("kddcup.data.corrected", names = columns, index_col=None)

df2 = df[df["service"] =="smtp"]
df2 = df.drop("service", axis = 1)
df2.head(5)
df2["label"].value_counts()

df2["label"].value_counts().plot(kind = "bar", rot = 45)


