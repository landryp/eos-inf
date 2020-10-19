# eos-inf

Code for inference of the neutron-star equation of state from a collection of astronomical observations of neutron stars.

DEPENDENCIES: [universality](https://github.com/reedessick/universality)

This codebase assumes the existence of EOS prior samples in the form of tabulated pressure,energy-density,baryon-density data.

---

### Documentation

Instructions for using the code are provided in DOCS.md (*under construction*).

---

### Scripts

##### scan-likelihoods

* scan-likelihoods path/to/obs.in

Analyze observed likelihood to obtain KDE bandwidth and prior bounds.

* writedag-scan-likelihoods path/to/eos-inf/ path/to/rundir/ path/to/obs.in

Same as above, but uses parallel condor jobs for a batch of likelihoods.

##### calc-eos-posterior

* calc-eos-posterior path/to/obs.in path/to/eosbank.in numeos nummass

Sample from EOS and mass priors; calculate EOS posterior based on likelihood.

* writedag-calc-eos-posterior path/to/eos-inf/ path/to/rundir/ path/to/obs.in path/to/eosbank.in numeos nummass

Same as above, but uses parallel condor jobs for a batch of likelihoods.

##### combine-obs

* combine-obs path/to/obs.in path/to/output.csv

Combine individual-event posteriors into joint EOS posterior.
