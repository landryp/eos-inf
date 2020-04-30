#!/usr/bin/python

import numpy as np
import numpy.random
import glob
from scipy.interpolate import interp1d

# EOS BANK NAVIGATION

def nameeossubdir(idn,mod=1e3,basename='DRAWmod',delim='-'):

	modidn = int(idn)/int(mod)
	modidn = str(modidn).zfill(6)
	mod = str(int(mod))
	eossubdir = basename+mod+delim+modidn

	return eossubdir

def namemacrodir(idn,basename='MACROdraw',delim='-'):

	idn = str(int(idn)).zfill(6)
	eosmacrodir = basename+delim+idn

	return eosmacrodir

def nameeostable(idn,basename='eos-draw',delim='-',ext='csv'):

	idn = str(int(idn)).zfill(6)
	eostable = basename+delim+idn+'.'+ext

	return eostable

def geteosbanksize(eosdir,mod=1e3,subdirname='DRAWmod',tablename='eos-draw',delim='-',ext='csv'):

	eossubdirs = glob.glob(eosdir+'/'+subdirname+'*'+delim+'*')
	eostables = glob.glob(eossubdirs[-1]+'/'+tablename+delim+'*.'+ext)
	lastidn = (eostables[-1].split(delim)[-1]).split('.')[0]
	eosbanksize = int(lastidn)+1

	return eosbanksize

def geteospaths(eosdir,eosbanksize,mod=1e3,subdirname='DRAWmod',tablename='eos-draw',delim='-',ext='csv'):

	eosbanksize = int(eosbanksize)

	eospaths = [eosdir+'/'+nameeossubdir(idn,mod,subdirname,delim)+'/'+nameeostable(idn,tablename,delim,ext) for idn in range(eosbanksize)]

	return eospaths

def getgprpaths(eosdir,eosbanksize,mod=1e3,subdirname='DRAWmod',tablename='draw-gpr',delim='-',ext='csv'):

	eosbanksize = int(eosbanksize)

	gprpaths = [eosdir+'/'+nameeossubdir(idn,mod,subdirname,delim)+'/'+nameeostable(idn,tablename,delim,ext) for idn in range(eosbanksize)]

	return gprpaths

def getmacropaths(eosdir,eosbanksize,mod=1e3,subdirname='DRAWmod',macrodirname='MACROdraw',delim='-',ext='csv'):

	eosbanksize = int(eosbanksize)

	macropaths = [glob.glob(eosdir+'/'+nameeossubdir(idn,mod,subdirname,delim)+'/'+namemacrodir(idn,macrodirname,delim)+'/'+macrodirname+delim+str(idn).zfill(6)+'-*.'+ext) for idn in range(eosbanksize)]

	return macropaths

# INTERPOLATION OF EOS PROPERTIES

M_key = 'M'
R_key = 'R'

def getpropnames(macropath):

	macrodat = np.genfromtxt(macropath,names=True,delimiter=',',dtype=None)
	props = list(macrodat.dtype.names)
	props.remove(M_key)
	props = [str(prop) for prop in props]

	return props

def interprels(macrodat):

	props = list(macrodat.dtype.names)
	props.remove(M_key)
	Ms = macrodat[M_key]

	rels = [interp1d(Ms,macrodat[prop],kind='linear',bounds_error=False,fill_value=0) for prop in props]

	return rels

def getrels(macropaths):

	macrorels = []
	for macropath in macropaths:

		macrodat = np.genfromtxt(macropath,names=True,delimiter=',',dtype=None)
		rels = interprels(macrodat)
		macrorels.append(rels)

	return macrorels

def getmacroprops(rels,mbranches,bhrels,M):

	numprops = len(rels[0])
	branch, minm, maxm = findbranch(mbranches,M)

	macros = [float(rels[branch][i](M)) if M >= minm and M <= maxm else float(bhrels[i](M)) for i in range(numprops)]
	np.append(macros,M)	

	return macros

def findbranch(mbranches,M):

	minms, maxms = mbranches
	numbranches = len(minms)
	branchtests = [1 if M >= minms[i] and M <= maxms[i] else 0 for i in range(numbranches)]

	branches = []
	for i in range(numbranches):
		if branchtests[i] == 1:
			branches.append((i,minms[i],maxms[i]))

	numbranches = len(branches)
	if numbranches == 0: 
		branch = (0,0.,0.)
	else:
		randbranch = np.random.randint(0,numbranches)	
		branch = branches[randbranch]

	return branch

def getmassseq(macropaths):

	minms = []
	maxms = []
	for macropath in macropaths:

		macrodat = np.genfromtxt(macropath,names=True,delimiter=',',dtype=None)
		Ms = macrodat[M_key]
		minms.append(np.min(Ms))
		maxms.append(np.max(Ms))

	minm = np.min(minms)
	maxm = np.max(maxms)

	return (minm,maxm)

def getmassbranch(macropaths):

	minms = []
	maxms = []
	for macropath in macropaths:

		macrodat = np.genfromtxt(macropath,names=True,delimiter=',',dtype=None)
		Ms = macrodat[M_key]
		minms.append(np.min(Ms))
		maxms.append(np.max(Ms))

	return (minms,maxms)

def testmassseq(massseq,mrange):

	boole = 0
	minm, maxm = massseq
	if minm <= mrange[0] and maxm >= mrange[1]: boole = 1

	return boole

def testr(mbranches,macropaths):

	boole = 1
	numbranches = len(mbranches[0])
	for i in range(numbranches):	
		minm = mbranches[0][i]
		maxm = mbranches[1][i]
		
		macrodat = np.genfromtxt(macropaths[i],names=True,delimiter=',',dtype=None)
		Ms, Rs = macrodat[M_key], macrodat[R_key]
		pts = len(Rs)

		rbranch = []
		for j in range(pts):
			if Ms[j] >= minm and Ms[j] <= maxm:
				rbranch.append(Rs[j])

		if len(rbranch) != pts:
			boole = 0
			break

	return boole

def removeosfails(idns,macros,mseqs,mtests):

	eosfails = []
	idns_tmp = []
	macros_tmp = []
	mseqs_tmp = []
	for i in range(len(idns)):
		if mtests[i] == 1:
			idns_tmp.append(idns[i])		
			macros_tmp.append(macros[i])
			mseqs_tmp.append(mseqs[i])
		else: eosfails.append(idns[i])

	return idns_tmp, macros_tmp, mseqs_tmp, eosfails

# BLACK HOLE PROPERTIES

def bhrhoc(m):

	return 0.

def bhradius(m):

	G = 6.67408e-8
	Msun = 1.3271244e26/G
	c = 2.99792458e10

	return 1e-5*2.*G*m*Msun/c**2

def bhlambda(m):

	return 0.

def bhmoi(m):

	G = 6.67408e-8
	Msun = 1.3271244e26/G
	c = 2.99792458e10

	return 1e-45*m*Msun*(2.*G*m*Msun/c**2)**2

def bhmb(m):

	return m

bhprops = {'rhoc': bhrhoc,'R': bhradius,'Lambda': bhlambda,'I': bhmoi,'Mb': bhmb}

def getbhrels(macropath):

	macrodat = np.genfromtxt(macropath,names=True,delimiter=',',dtype=None)
	props = list(macrodat.dtype.names)
	props.remove(M_key)

	bhrels = [bhprops[prop] for prop in props]

	return bhrels
