# eos-inf
Code for performing equation of state inference with data from observations of neutron stars.

How to run remotely:

1. Set writedag and writesubs locally as desired
2. Navigate to eos-inf on cluster, pull repo (git pull) and install code (python setup.py install --prefix ../opt/); delete contents of remote/ subdirectory
3. Navigate to /home/philippe.landry on cluster and run . install_codes.sh; create (or delete contents of) target directory and subsidiary log/ directory, and link with ln -s /full/path/to/target public_html/linkname
4. Run writedag and writesubs
5. Submit jobs with condor_submit_dag $PWD/eos-inf/remote/*.dag; monitor with condor_q -dag and tail -f $PWD/eos-inf/remote/*.dagman.out
6. Make diagnostic plots with kde-corner-samples, plot-process
7. Access data at https://ldas-jobs.ligo-wa.caltech.edu/~philippe.landry/

How to run remotely on the head node without disconnecting:

nohup command 1> nohup.out 2> nohup.err &
