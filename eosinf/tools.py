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

def geteospath(idn,eos_parsing_data):

	path_to_eos_dir, mod, subdir_name, eos_table_name, macrodir_name, delim, ext = eos_parsing_data

	eos_path = path_to_eos_dir+'/'+nameeossubdir(idn,mod,subdir_name,delim)+'/'+nameeostable(idn,eos_table_name,delim,ext)

	return eos_path

def getgprpath(idn,eos_parsing_data):

	path_to_eos_dir, mod, subdir_name, eos_table_name, macrodir_name, delim, ext = eos_parsing_data

	gpr_path = path_to_eos_dir+'/'+nameeossubdir(idn,mod,subdir_name,delim)+'/'+nameeostable(idn,eos_table_name,delim,ext)

	return gpr_path

def getmacropaths(idn,eos_parsing_data):

	path_to_eos_dir, mod, subdir_name, eos_table_name, macrodir_name, delim, ext = eos_parsing_data

	macro_paths = glob.glob(path_to_eos_dir+'/'+nameeossubdir(idn,mod,subdir_name,delim)+'/'+namemacrodir(idn,macrodir_name,delim)+'/'+macrodir_name+delim+str(idn).zfill(6)+'-*.'+ext)

	return macro_paths

# INTERPOLATION OF EOS PROPERTIES

M_key = 'M'
R_key = 'R'
rhoc_key = 'rhoc'

def getpropnames(macropath,obstype):

	macrodat = np.genfromtxt(macropath,names=True,delimiter=',',dtype=None)
	props = list(macrodat.dtype.names)
	props.remove(M_key)
	props = [str(prop) for prop in props]

	return props

def interprels(macrodat,obstype):

	props = [prop for prop in obstype]
	props[:] = [prop for prop in props if prop != 'm']
	Ms = macrodat['m']

	rels = [interp1d(Ms,macrodat[prop],kind='linear',bounds_error=False,fill_value=0) for prop in props]

	return rels

def getrels(macrodats,obstype):

	macrorels = []
	for macrodat in macrodats:
		rels = interprels(macrodat,obstype)
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

def getmassseqs(macrodats):

	minms = []
	maxms = []
	for macrodat in macrodats:

		Ms = macrodat['m']
		minms.append(np.min(Ms))
		maxms.append(np.max(Ms))

	return (minms,maxms)

def getmacrodats(macropaths,obsprops):

	props = [prop for prop in obsprops if prop != 'm']
	if 'R' not in props: props.append('R')
	if 'rhoc' not in props: props.append('rhoc')

	macrodats = []
	for macropath in macropaths:

		macrodat_tmp = {}
		macrodat = np.genfromtxt(macropath,names=True,delimiter=',',dtype=None)
		macrodat_tmp['m'] = macrodat[M_key]
		
		for prop in props:
			macrodat_tmp[prop] = macrodat[prop]

		macrodats.append(macrodat_tmp)	

	return macrodats

def testmassseq(massseq,mrange):

	boole = 0
	minm, maxm = massseq
	if minm <= mrange[0] and maxm >= mrange[1]: boole = 1

	return boole

def testrhoc(mbranches,macrodats,fail_mass=1.,start_rhoc=2.24e14):

	boole = 1
	numbranches = len(mbranches[0])
	if numbranches < 1: boole = 0

	minMs, minrhocs = [], []
	for i in range(numbranches):	
		minm = mbranches[0][i]
		
		macrodat = macrodats[i]
		Ms, rhocs = macrodat['m'], macrodat[rhoc_key]
		minM, minrhoc = Ms[0], rhocs[0]
		minMs.append(minM)
		minrhocs.append(minrhoc)

	if numbranches >= 1:
		firstrhoc = np.min(np.array(minrhocs))
		first_index = minrhocs.index(firstrhoc)
		firstM = minMs[first_index]

		if firstrhoc <= start_rhoc and firstM > fail_mass:
			boole = 0

	return boole

def testr(mbranches,macrodats,fail_radius=30,mass_prior_bounds=[0.,4.]):

	boole = 1
	numbranches = len(mbranches[0])
	if numbranches < 1: boole = 0

	for i in range(numbranches):	
		minm = mbranches[0][i]
		maxm = mbranches[1][i]
		
		macrodat = macrodats[i]
		Ms, Rs = macrodat['m'], macrodat[R_key]
		pts = len(Rs)

		rbranch = []
		for j in range(pts):

			if Ms[j] < mass_prior_bounds[0] or Ms[j] > mass_prior_bounds[1]:
				rbranch.append(Rs[j])

			elif Ms[j] < minm or Ms[j] > maxm:
				rbranch.append(Rs[j])

			elif Ms[j] >= minm and Ms[j] <= maxm and abs(Rs[j]-fail_radius) > 1e-6:
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

def mergecomps(numcomps,numeoslist,idnslist,macroslist,mbrancheslist,eosfailslist):
	
	numeos = np.min(numeoslist)
	idns, eosfails, eosspares, macros, mbranches = [], [], [], [], []
	
	for i in range(numcomps):
		idns.extend(idnslist[i][:numeos])
		macros.extend(macroslist[i][:numeos])
		mbranches.extend(mbrancheslist[i][:numeos])

		spareidns = idnslist[i][numeos:]
		failidns = eosfailslist[i]
		if len(failidns) > 0: eosfails.extend(failidns)
		if len(spareidns) > 0: eosspares.extend(spareidns)

	return idns, macros, mbranches, eosfails, eosspares

# BLACK HOLE PROPERTIES

def bhrhoc(m):

	return 0.

def bhradius(m):
	
	G = 6.67408e-8
	Msun = 1.3271244e26/G
	c = 2.99792458e10
	
	return 1e-5*2.*G*float(m)*Msun/c**2

def bhlambda(m):

	return 0.

def bhmoi(m):

	G = 6.67408e-8
	Msun = 1.3271244e26/G
	c = 2.99792458e10

	return 1e-45*m*Msun*(2.*G*float(m)*Msun/c**2)**2

def bhmb(m):

	return m

bhprops = {'rhoc': bhrhoc,'R': bhradius,'Lambda': bhlambda,'I': bhmoi,'Mb': bhmb}

def getbhrels(obstype):

	props =  [prop for prop in obstype]
	props[:] = [prop for prop in props if prop != 'm']

	bhrels = [bhprops[prop] for prop in props]

	return bhrels
