# eos-inf documentation

Documentation for the eos-inf module for inference of the neutron-star equation of state from a collection of astronomical observations of neutron stars.

The basic workflow proceeds as follows. An astronomical observation, in the form of discrete likelihood samples in stellar mass, radius, etc., is given a smooth representation as a KDE. An EOS is drawn from the prior, which is defined by a discrete set of EOSs. A stellar mass sample is drawn from a specified mass prior. Then a lookup is performed to determine the radius, tidal deformability, etc. that correspond to that mass for the given EOS sample. The value of the likelihood for those properties is assigned as a posterior weight to the EOS. An iteration over EOS samples and mass samples is performed within a Monte Carlo algorithm to calculate the posterior weight for every EOS in the prior, marginalizing over the mass uncertainty in the likelihood.

A detailed description of this inference scheme is provided in Landry, Essick + Chatziioannou PRD 101 123007 (2020) [arXiv:2003.04880](https://arxiv.org/abs/2003.04880) and references therein.

---

# Installation

The [eos-inf]((https://github.com/landryp/eos-inf)) module is available on github.

git clone https://github.com/landryp/eos-inf

It can be installed with the standard setup.py script that is provided.

python setup.py install --prefix path/to/opt/

The path and python path variables should be updated to point to the install directory, e.g.

export PATH=path/to/opt/bin:$PATH
export PYTHONPATH=path/to/opt/lib/python2.7/site-packages:/path/to/opt/lib64/python2.7/site-packages:$PYTHONPATH

The same install instructions apply to the [universality](https://github.com/reedessick/universality) module, upon which eos-inf depends.

git clone https://github.com/reedessick/universality

---

# Setup

The inference assumes the existence of a collection of tabulated EOSs in the required format, such that they define the discrete prior distribution over EOSs. A bank of nonparametric EOSs is stored at

LHO:/home/philippe.landry/gpr-eos-stacking/EoS/mrgagn/
CIT:/home/philippe.landry/nseos/eos/gp/mrgan/

and a metadata file for this EOS bank is located at

LHO:/home/philippe.landry/eos-inf/eosbank.in
CIT:/home/philippe.landry/eos-inf/eosbank.in

The code supports four kinds of astronomical observations: compact binary coalescences ("cbc"), pulsar mass and radius measurements ("xmr"), pulsar mass measurements ("psr") and pulsar moment of inertia measurements ("moi"). Likelihood samples in csv format must be provided for each observation. The fields expected for each observation type are as follows:

cbc: m1,m2,Lambda1,Lambda2,Prior
xmr: m,R,Prior
psr: m,Prior
moi: m,I,Prior

The likelihoods to be analyzed should be recorded in an observations metadata file ("obs.in") that contains the observation paths and types, i.e.

path/to/likelihood1.csv,cbc
path/to/likelihood2.csv,psr
etc.

With these preliminaries satisfied, the inference code can be run.

---

# Instructions

1. Determine the optimal bandwidth for the KDE representations of the likelihoods.

writedag-scan-likelihoods path/to/eos-inf/ path/to/rundir/ path/to/obs.in

The paths to the likelihood data are sourced from the observation metadata file obs.in (described above). The run directory stores logs associated with the condor jobs. The path to the eos-inf repo is needed to source the script parse-likelihood-samples that interprets the likelihood data; a script investigate-bandwidth from universality is used to search for the optimal KDE bandwidth. For each likelihood, an output .bw file is saved to the same directory as the likelihood. The first line of that file is the optimal bandwidth.

2. Sample in EOSs and masses, then analyze the likelihoods to calculate the EOS posterior for each observation.

writedag-calc-eos-posterior path/to/eos-inf/ path/to/rundir/ path/to/obs.in path/to/eosbank.in numeos nummass

The observation metadata and run directory are provided as above. The eosbank metadata file (described above) indicates which EOSs to sample. The path to the eos-inf repo is needed to source the script sample-priors that draws the EOSs and masses; scripts weigh-samples and marginalize-samples from universality are used to calculate the EOS posterior weights and marginalize over the masses. The integer parameters numeos and nummass set the number of EOS draws and the number of masses drawn per EOS, respectively. Larger numbers give better resolution of the EOS posterior; numeous should be at least 500k and nummass should be at least 50.

3. Combine the EOS posteriors from the individual observations into a joint posterior, representing the inferred distribution over EOSs from all the available observational data.

combine-obs path/to/obs.in path/to/output.csv

This script calls collate-samples from universality and calc-total-weight from eos-inf to concatenate all the individual-event EOS weights and total them, giving the joint posterior weight. The observation metadata file tells it which observations to combine. The final join posterior weights get written to the specified output file.

4. Do some basic post-processing to make pressure-density, mass-radius, etc. plots and plots of the posterior distributions on the radius, tidal deformability, etc. of a 1.4 solar mass NS.

*under construction*

