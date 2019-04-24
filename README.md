# eos-inf

Code for performing equation of state inference with data from observations of neutron stars.

---

### Meta-scripts

###### EoS inference (local)

* INFEREOS startjobnum numjobs jobsperdir massesperjob gwfile gpfile outdir

###### EoS inference (remote)

* writedag (writes dag for condor)
* writesubs (writes subs for condor)

---

### Scripts

###### Synthetic EoS generation

* draweos startjobnum numjobs jobsperdir gpfile outdir

---

### Remote instructions

1. Set writedag and writesubs locally as desired
2. Log in to cluster and from /home/philippe.landry run . install_codes.sh; ; create (or delete contents of) target directory and subsidiary log/, remote/ directory, and link with ln -s /full/path/to/target public_html/linkname
3. Navigate to eos-inf on cluster, pull repo (git pull) and install code (python setup.py install --prefix ../opt/)
4. Run writedag and writesubs
5. Submit jobs with condor_submit_dag $PWD/eos-inf/remote/*.dag; monitor with condor_q -dag and tail -f $PWD/eos-inf/remote/*.dagman.out
6. Make diagnostic plots with kde-corner-samples, plot-process (prevent hangup with nohup command 1> nohup.out 2> nohup.err &)
7. Access data at https://ldas-jobs.ligo-wa.caltech.edu/~philippe.landry/

