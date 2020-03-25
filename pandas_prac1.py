# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 23:55:31 2018

@author: sudhanshu kumar sinh
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

whisky=pd.read_csv("whiskies.txt")
whisky["Region"]=pd.read_csv("regions.txt")
flavour=whisky.iloc[:,2:14]

corr_flavour=pd.DataFrame.corr(flavour)
plt.figure(figsize=(10,10))
plt.pcolor(corr_flavour)
plt.colorbar()
plt.savefig("flavour_corr.pdf")

corr_whisky=pd.DataFrame.corr(flavour.transpose())
plt.figure(figsize=(10,10))
plt.pcolor(corr_whisky)
plt.axis("tight")
plt.colorbar()
plt.savefig("whiskey_corr.pdf")


from sklearn.cluster.bicluster import SpectralCoclustering
model = SpectralCoclustering(n_clusters=6,random_state=0)
model.fit(corr_whisky)
#print(model.rows_)

a=np.sum(model.rows_,axis=1)
b=np.sum(model.rows_,axis=0)

#print(model.row_labels_)

whisky["Group"]=pd.DataFrame(model.row_labels_,index=whisky.index)
whisky=whisky.ix[np.argsort(model.row_labels_)]
whisky=whisky.reset_index(drop=True)

correlations = pd.DataFrame.corr(whisky.iloc[:,2:14].transpose())
correlations = np.array(correlations)

plt.figure(figsize=(14,7))
plt.subplot(121)
plt.pcolor(corr_whisky)
plt.title("Original")
plt.axis("tight")

plt.subplot(122)
plt.pcolor(correlations)
plt.title("Re-arranged")
plt.axis("tight")
plt.savefig("Correlation.pdf")