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

###### TOV+ integration

* getprops startjobnum numjobs jobsperdir outdir

###### Binary system generation

* getbins massesperjob outdir (remote)
* getbinaries massesperjob (local)

###### Construction of prior

* collectbins outdir (remote)
* collectbinaries (local)

###### Reweighting of observational likelihood

* weighsamps gwfile sampfile weightsfile

---

### Remote instructions

1. Adjust run parameters through writedag and writesubs in local repo bin/ subdirectory; ``git push'' updates to repo
2. Navigate to cluster base directory and run ``. install _codes.sh''; create/clear target directory and link with ``ln -s $PWD/target/path public_html/linkname''
3. From repo on cluster, ``git pull'' repo and install code with ``python setup.py install --prefix ../opt/''
4. From base directory, run ``writedag'' and ``writesubs''
5. Submit jobs with ``condor_submit_dag $PWD/target/path/remote/*.dag''; monitor with ``condor_q -dag'' and ``tail -f $PWD/target/path/remote/*.dagman.out''
6. Once jobs completed, make diagnostic plots with kde-corner-samples, plot-process (prevent hangup with ``nohup command 1> nohup.out 2> nohup.err &'')
7. Access data via softlink at https://ldas-jobs.ligo-wa.caltech.edu/~philippe.landry/

