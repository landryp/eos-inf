# eos-inf

Code for performing equation of state inference with data from observations of neutron stars.

---

### Meta-scripts

###### EoS inference (local)

* INFEREOS startjobnum numjobs jobsperdir massesperjob gwfile gpfile outdir mrng Mcrng Mobs

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

1. Navigate to remote run directory and run ``. install _codes.sh''; create/clear target directory and link with ``ln -s $PWD/target/path public_html/linkname''
2. Navigate to remote repo and adjust run parameters in in/writedags.in; install code with ``python setup.py install --prefix ../opt/''
3. From run directory, run ``writedags $(cat $PWD/repo/in/writedags.in)''
4. Submit jobs to condor with ``condor_submit_dag $PWD/target/remote/DAGNAME.dag'' for EOSPRIOR.dag, followed by INFEREOS.dag and POSTPLOTS.dag once complete; monitor with ``condor_q -dag'' and ``tail -f $PWD/target/remote/DAGNAME*.dagman.out''
5. Access data via softlink at https://ldas-jobs.ligo-wa.caltech.edu/~philippe.landry/

Note: if running on head node, prevent hangup with ``nohup command 1> nohup.out 2> nohup.err &''

Reed's remote gpr-eos-gw170817 repo: https://ldas-jobs.ligo-wa.caltech.edu/~reed.essick/BNS_tides/gpr-eos-gw170817
