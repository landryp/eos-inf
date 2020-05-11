# eos-inf

Code for inference of the neutron-star equation of state from a collection of astronomical observations of neutron stars.

DEPENDENCIES: [universality](https://github.com/reedessick/universality)

This codebase assumes the existence of EOS prior samples in the form of tabulated pressure,energy-density,baryon-density data.

---

### Documentation

Instructions for using the code are provided in DOCS.md.

---

### Scripts

##### calc-eos-posterior

* calc-eos-posterior path/to/obs.in path/to/eosbank.in numeos nummass

Analyze observed likelihood to obtain KDE bandwidth and prior bounds; sample from EOS and mass priors; calculate EOS posterior.
