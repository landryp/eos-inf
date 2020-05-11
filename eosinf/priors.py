#!/usr/bin/python

import numpy as np
import numpy.random
import scipy.stats

def randnum(lb,ub,size=1):

	floats = (ub-lb)*np.random.random_sample(size)+lb

	return floats

# PROBABILITY DISTRIBUTIONS

def flat(size=1,lb=0.,ub=1.):

	return scipy.stats.uniform.rvs(loc=lb,scale=ub-lb,size=int(size))

def normal(size=1,med=0.,std=1.):

	return scipy.stats.norm.rvs(loc=med,scale=std,size=int(size))

distrs = {'flat': flat, 'norm': normal}

# PRIOR DISTRIBUTION SAMPLERS

def samplemassprior(size=1,distr='flat',params=None):

	distrib = distrs[distr]
	if params is None: msamps = distrib(size)
	else: msamps = distrib(size,*params)

	return msamps

def samplebinarymassprior(size=1,distr='flat',params=None):

	distrib = distrs[distr]
	if params is None: msamps = distrib(2*size)
	else: msamps = distrib(2*size,*params)

	m1samps = [max(msamps[i],msamps[i+1]) for i in range(0,2*size,2)]
	m2samps = [min(msamps[i],msamps[i+1]) for i in range(0,2*size,2)]

	return zip(m1samps,m2samps)
