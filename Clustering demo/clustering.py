import os

import numpy as np
import itertools
from scipy.stats import gamma
from scipy.stats import norm
import pandas as pd
import geopandas as gpd
 
import hdbscan


from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.metrics import adjusted_rand_score
from sklearn import preprocessing

import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns


# grab the GEDI data that was unpacked into a geodataframe 
# data columns: 'shot_number','rh100','fhd_normal','cover','pai','l2b_quality_flag'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
fp = os.path.join(THIS_FOLDER, '../unpack/unpacked_files/test.shp')
ix = gpd.read_file(fp)


# The code below assumes that you have a dataframe called ix with all the data columns (PAI_5, PAI_10, …, RH100)

# Rescale rh100 so that it's in meters

ix.rh100 = ix.rh100/100.0


# Get only power beams

pbs = [u'BEAM0101', u'BEAM0110', u'BEAM1000', u'BEAM1011']

ix = ix[ix['beam'].isin(pbs)]

 

# Filter out very tall footprints

# ix = ix.loc[ix.rh100<=60,]
# attempted to fit in ix2 here, was complained as "undefined"
ix2 = ix.loc[ix.rh100<=60,]

 

# List of PAI column names

painames = ['pai_' + str(z) for z in range(5,65,5)]

 

# Define function to calculate evenness metric from PAI columns

def evenness(avec):

    avec = avec[avec!=0]

    p = avec/np.sum(avec)

    even = np.sum(p*np.log(p))*-1

    return(even)


# Calculate evenness metric that indicates whether the canopy is clumped or evenly distributed

X = ix2[painames].apply(lambda x: evenness(x), axis=1)

ix2['even'] = X/np.log(len(painames))

 

# Standardize columns for clustering

transformer = preprocessing.RobustScaler().fit(ix2[['even','pai','rh100']])

X = transformer.transform(ix2[['even','pai','rh100']])

 

# Try many different minimum cluster sizes, keeping track of the relative validity index

# This will run slow for large datasets

crv = []

ilist = []

# originally goes to 500, but that took at least an hour to compute.
# shortened just for tech demo
for i in range(3,250,1):

    clusterer = hdbscan.HDBSCAN(min_cluster_size=i, min_samples=i, gen_min_span_tree=True, allow_single_cluster=True)

    clusterer.fit(X)

    P = clusterer.labels_

    ilist.append(i)

    m = clusterer.relative_validity_

    crv.append(m)

    print(m, i)

 

# Get minimum cluster size that maximizes relative validity index

# and cluster on that

csize = ilist[crv.index(np.max(crv))]

for i in range(1,csize,1):

    clusterer = hdbscan.HDBSCAN(min_cluster_size=csize, min_samples=i, gen_min_span_tree=True, allow_single_cluster=True)

    clusterer.fit(X)

    P = clusterer.labels_

    unique, counts = np.unique(P, return_counts=True)

    ctab = np.asarray((unique, counts)).T

    print(ctab)

    print(clusterer.relative_validity_)


# TODO: revisit
# attempt at plotting for height based on cluster classes
# df = pd.DataFrame(list(zip(cluster_list, height_list)), columns = ['cluster_bin', 'height'])
# fig = sns.boxplot(x="cluster_bin", y="height", data=df)


# best attempt at a working graph for the tech demo
df = pd.DataFrame(ctab)
df.plot.box(grid='True')

plt.savefig('example.png')

plt.show()











