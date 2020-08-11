#!/usr/bin/python

from optparse import OptionParser
import numpy as np
import scipy.stats
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import seaborn as sns

# PLOTTING FUNCTIONS

def pplot(array,weights,path_to_output,xlims,axis_label=None,color=sns.color_palette()[0],num_bins=None,reflect=False,ylims=False):

    weights = weights/np.sum(weights)
    
    if reflect:
        array = array + [-pt for pt in array]
        weights = weights + weights
        
    equal_weight_post = equalize_sample_weights(array,weights)
    
    prior_kde = gaussian_kde(array)
    post_kde = gaussian_kde(equal_weight_post)
#    post_kde = gaussian_kde(array,weights=weights)
    
    xmin, xmax = xlims
    grid = np.linspace(xmin,xmax,1000)
    
    sns.rugplot(weighted_quantile(array,weights), height=0.03, color=color, lw=1.5, zorder=100)
    
    plt.plot(grid,prior_kde(grid),color='0.3',linestyle=':',label='prior')
    plt.plot(grid,post_kde(grid),color=color)
    plt.fill_between(grid,post_kde(grid),0.,color=color,alpha=0.3)
    #sns.distplot(array, bins=num_bins, hist_kws={"weights":weights,"density":True}, kde=False, label='post', color=color)
    
    plt.xlabel(axis_label)
    plt.xlim(xmin,xmax)
    if ylims:
        ymin, ymax = ylims
        plt.ylim(ymin,ymax)
    sns.despine(left=True, offset=10, trim=True)
    plt.yticks([], [])
    plt.legend(frameon=False)
    
    plt.savefig(path_to_output)
    
    return None

def equalize_sample_weights(array,weights,res=int(1e3)):

    equal_weight_array = np.random.choice(array,size=res,p=weights/np.sum(weights)) # draw equal-weight samples
    
    return equal_weight_array

def weighted_quantile(array,weights,qs=[0.05,0.5,0.95],res=10000):
    
    equal_weight_array = np.random.choice(array,size=res,p=weights/np.sum(weights))
    
    return np.percentile(equal_weight_array,qs*100)
