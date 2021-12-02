# Cluster-Analysis-and-Ranking-of-RedBus-Data
redBus is an online platform where different bus operators provide their services. These operators set 
the prices according to the demand available. These bus operators vary from single service operators 
to ones which have scores of services. But not all operators have the same level of visibility on these 
signals or the capability to price effectively. Operators who have better ability/confidence may price 
independently while some others may choose to follow the prices of such price setters.

The price data for each berth is unpacked from the seat fare column to separate columns. 
There are 4 different clusters according to the elbow method. The clusters are used to find the 
group of operators that define the price and the set of operators that follow them. The 
cluster’s leading operator is found out with the help of the centroid of the cluster and the 
confidence score of each element. An element with confidence score of 1 is set to be the 
leading operator. The confidence score of the other points in the plot with respect to the
leader points determines the cluster group it belongs to.

In this scenario, we are looking to identify specific datapoints to determine how exactly they 
fit into a cluster. This can be done using a simple technique called soft-kmeans weights 
technique. Unlike normal k-means that assigns each data point to only one cluster, soft kmeans calculates a weighting that describes how likely each data point is to belong to each 
cluster. Higher values indicate strong or confident classification and lower values suggest 
weak or unlikely classification.
