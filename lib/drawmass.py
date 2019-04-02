#!/usr/bin/python

import numpy as np

# Random draws from uniform prior in each component mass, with m2 < m1

drawmass_uniform(mrange=[1.16,1.36,1.36,1.60]):

	m1i, m1f, m2i, m2f = mrange # specify prior ranges
	
	m2 = (m2f-m2i)*np.random.random_sample()+m2i
	m1i = max(m1i,m2) # enforce m2 < m1
	m1 = (m1f-m1i)*np.random.random_sample()+m1i

	return m1, m2
