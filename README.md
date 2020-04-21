# eos-inf

Code for inference of the neutron-star equation of state from a collection of astronomical observations of neutron stars.

DEPENDENCIES: [ns-struc](https://github.com/landryp/ns-struc)

This codebase assumes the existence of EOS prior samples in the form of tabulated pressure,energy-density,baryon-density data.

---

### Documentation

Instructions for using the code are provided in DOCS.md.

---

### Scripts

##### INFER-FROM-OBS

* INFER-FROM-OBS path/to/repo path/to/gwposterior.csv path/to/eos/database output/results/path 1000 N m2i,m2f,m1i,m1f Mci,Mcf Di,Df Mmaxobs num_eos

Weight each EoS from specified prior database according to chosen posterior, marginalizing over masses by using N pairs of mass samples per EoS drawn from a flat distribution in [m2i,m2f], [m1i,m1f] with m1>m2 and chirp mass in [Mci,Mcf]. Also marginalizes over distance [Di,Df] in Mpc.
