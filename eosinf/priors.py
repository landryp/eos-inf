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
	if params is None:
		msamps2 = distrib(size)
		msamps1 = distrib(size)
	else:
		params2 = [params[0],params[1]]
		params1 = [params[-2],params[-1]]
		mcrange = [params[2],params[3]]
		msamps2 = distrib(size,*params2)
		msamps1 = distrib(size,*params1)

	m1samps = []
	m2samps = []
	for m1,m2 in zip(msamps1,msamps2):
	
		chirp = (m1*m2)**0.6/(m1+m2)**0.2
	
		while m1 < m2 or chirp < mcrange[0] or chirp > mcrange[1]:
		
			m1 = distrib(1,*params1)
			m2 = distrib(1,*params2)
			chirp = (m1*m2)**0.6/(m1+m2)**0.2

		m1samps.append(m1)
		m2samps.append(m2)

	return zip(m1samps,m2samps)
