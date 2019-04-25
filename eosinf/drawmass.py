#!/usr/bin/python

import numpy as np

# Random draws from uniform prior in each component mass, with m2 < m1

def drawmass_uniform(mrange): #=[1.16,1.36,1.36,1.60]):

	m1i, m1f, m2i, m2f = mrange # specify prior ranges
	
	m2 = (m2f-m2i)*np.random.random_sample()+m2i
	m1 = (m1f-m1i)*np.random.random_sample()+m1i
	
	m1out = max(m1,m2)
	m2out = min(m1,m2) # enforce m2 < m1

	return m1out, m2out
