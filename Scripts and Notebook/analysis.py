# -*- coding: utf-8 -*-
"""dlw9383-bandofthehawk-output.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/154b5GvPxORu_mhpHDIsNlWvyBxMIwEw2
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc={'figure.figsize':(15,10)})
pd.set_option("precision", 10)
import os

train=pd.read_csv("/content/PricingData.csv")

train.shape


train.isnull().sum()

train.info()

train = pd.concat([train, train['Seat Fare Type 1'].str.split(',', expand=True)], axis=1)

train.columns = train.columns.map(str)

train = train.rename({'0': 'berth1_1','1': 'berth2_1', '2': 'berth3_1','3': 'berth4_1', '4': 'berth5_1','5': 'berth6_1', '6': 'berth7_1'},axis='columns')

train.update(train[['berth1_1','berth2_1','berth3_1','berth4_1', 'berth5_1', 'berth6_1','berth7_1']].fillna(0))



train = pd.concat([train, train['Seat Fare Type 2'].str.split(',', expand=True)], axis=1)

train.columns = train.columns.map(str)

train = train.rename({'0': 'berth1_2','1': 'berth2_2', '2': 'berth3_2','3': 'berth4_2'},axis='columns')

train.update(train[['berth1_2','berth2_2','berth3_2','berth4_2']].fillna(0))



train.drop(['Seat Fare Type 1', 'Seat Fare Type 2','Service Date','RecordedAt'], axis=1, inplace=True)



train[train.columns[1:]] = train[train.columns[1:]].astype(float)

train.drop_duplicates(keep='first', inplace=True)

id = train["Bus"]
train.drop(['Bus'], axis=1, inplace=True)
reduced_data = train.values

from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
reduced_data = min_max_scaler.fit_transform(reduced_data)

from sklearn.cluster import KMeans
data_frame = reduced_data
Sum_of_squared_distances = []
K = range(1,10)
for num_clusters in K :
 kmeans = KMeans(n_clusters=num_clusters)
 kmeans.fit(data_frame)
 Sum_of_squared_distances.append(kmeans.inertia_)
plt.plot(K,Sum_of_squared_distances,'bx-')
plt.xlabel('Values of K') 
plt.ylabel('Sum of squared distances/Inertia') 
plt.title('Elbow Method For Optimal k')
plt.show()

from sklearn.decomposition import PCA
reduced_data = PCA(n_components=2).fit_transform(train)
results = pd.DataFrame(reduced_data,columns=['pca1','pca2'])

kmeansmodel = KMeans(n_clusters=4, init='k-means++', random_state=0)
y_kmeans= kmeansmodel.fit_predict(reduced_data)

y_k=pd.DataFrame(y_kmeans, columns=['Clusters']) 
train["Clusters"]=y_k

sns.scatterplot(x="pca1", y="pca2", hue=train['Clusters'], data=results)
centers = np.array(kmeansmodel.cluster_centers_)
plt.scatter(centers[:,0], centers[:,1], marker="x", color='r')
plt.title('K-means Clustering with 2 dimensions')
plt.show()

import numpy.matlib
def soft_clustering_weights(data, cluster_centres, **kwargs):
    
    """
    Function to calculate the weights from soft k-means
    data: Array of data. Features arranged across the columns with each row being a different data point
    cluster_centres: array of cluster centres. Input kmeans.cluster_centres_ directly.
    param: m - keyword argument, fuzziness of the clustering. Default 2
    """

    m = 2
    if 'm' in kwargs:
        m = kwargs['m']
    
    Nclusters = cluster_centres.shape[0]
    Ndp = data.shape[0]
    Nfeatures = data.shape[1]

    EuclidDist = np.zeros((Ndp, Nclusters))
    for i in range(Nclusters):
        EuclidDist[:,i] = np.sum((data-np.matlib.repmat(cluster_centres[i], Ndp, 1))**2,axis=1)
    

    
    invWeight = EuclidDist**(2/(m-1))*np.matlib.repmat(np.sum((1./EuclidDist)**(2/(m-1)),axis=1).reshape(-1,1),1,Nclusters)
    Weight = 1./invWeight
    
    return Weight

for i in range(4):
    train['p' + str(i)] = 0
    
train[['p0', 'p1', 'p2','p3']] = soft_clustering_weights(reduced_data, kmeansmodel.cluster_centers_)

train['confidence'] = np.max(train[['p0', 'p1', 'p2','p3']].values, axis = 1)



train.confidence.describe()

train["Leader Group ID"]=train[["p0","p1","p2","p3"]].idxmax(axis=1)


train.reset_index(inplace = True,drop=True)

def closest_leader(x):
    for ele in train[train["Leader Group ID"][x]].sort_values(ascending=True):
        if(ele>train[train["Leader Group ID"][x]][x]):
            element = ele
            pos = train[train[train["Leader Group ID"][x]] == ele].index[0]
            break
        elif(ele==train[train["Leader Group ID"][x]][x]):
            element = ele
            pos = train[train[train["Leader Group ID"][x]] == ele].index[0]
    return element,pos
def closest_follower(x):
    for ele in train[train["Leader Group ID"][x]].sort_values(ascending=False):
        if(ele<train[train["Leader Group ID"][x]][x]):
            return ele, train[train[train["Leader Group ID"][x]] == ele].index[0]
            break

leadcon=[]
for i in range(len(train)):
    leadcon.append(closest_leader(i))
train["sample_lead"]=leadcon

leadfol=[]
for i in range(len(train)):
    leadfol.append(closest_follower(i))
train["sample_follow"]=leadfol

train[['leadscore', 'leadpos']] = pd.DataFrame(train['sample_lead'].tolist(), index=train.index)

train[['folscore', 'folpos']] = pd.DataFrame(train['sample_follow'].tolist(), index=train.index)

train.drop(['sample_lead', 'sample_follow'], axis=1, inplace=True)

id.reset_index(inplace = True, drop = True)


train = pd.concat([train,id],axis=1)



train["leadpos"]=train["leadpos"].astype(int)
follows=[]
for i in train["leadpos"]:
    follows.append(train["Bus"][i])

train["Follows"]=follows

followedby=[]
for i in train["folpos"]:
    followedby.append(train["Bus"][i])

train["Is followed by"]=followedby

train.drop(['berth1_1', 'berth2_1', 'berth3_1', 'berth4_1', 'berth5_1', 'berth6_1',
       'berth7_1', 'berth1_2', 'berth2_2', 'berth3_2', 'berth4_2', 'Clusters',
       'p0', 'p1', 'p2', 'p3', 'confidence','Leader Group ID','leadpos','folpos'], axis=1, inplace=True)



train = train[['Bus','Follows','leadscore','Is followed by','folscore']]



train.rename({'leadscore': 'Confidence Score (0 to 1)', 'folscore': 'Confidence Score (0 to 1)'}, axis=1, inplace=True)



train.to_csv('DLW9383_BandoftheHawk_output.csv',index=False)
