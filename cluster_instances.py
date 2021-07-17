import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def show_graph(cluster_distribution, cluster_c):
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    clusters = []
    for i in range(cluster_c):
        clusters.append(i)
    ax.bar(clusters,cluster_distribution)
    ax.set_ylabel('Number of Instances')
    ax.set_xlabel('Instance Cluster')
    ax.set_title('K-Cluster Distributions')
    plt.show()
    return

def make_distribution(labels, cluster_c):
    # takes array of labels, returns a list for sending to graphing function
    # dist: array where each index denotes a cluster, and the value at each
    #       index is the number of problem instances in that cluster
    dist = [0]*cluster_c
    for i in range(len(labels)):
        dist[labels[i]] += 1
    return dist

def main(cluster_c=20):
    # returns an array for use in subset_finder.py
    
    df=pd.read_csv('instance_features_sat2018.csv', sep=',', index_col=0,header=1)
    kmeans = KMeans(n_clusters=cluster_c, random_state=0).fit(df)
    
    allocations = make_distribution(kmeans.labels_, cluster_c)
    #show_graph(allocations, cluster_c) #make sure solver_c > 1
    
    answer = []
    
    for i in range(cluster_c):
        answer_i = []
        for e in range(len(kmeans.labels_)):
            if kmeans.labels_[e] == i:
                answer_i.append(e)
        answer.append(answer_i)
    return answer