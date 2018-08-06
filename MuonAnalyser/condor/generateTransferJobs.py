#!/usr/bin/python
import os
import sys
import re
import argparse
import subprocess

## helper for files on dCache/EOS (LPC)
#def useInputDir(inputDir):
#    theInputFiles = []
#    for d in range(len(inputDir)):
#        my_dir = inputDir[d]
#        if not os.path.isdir(my_dir):
#            print "ERROR: This is not a valid directory: ", my_dir
#            if d==len(inputDir)-1:
#                print "ERROR: No input files were selected"
#                exit()
#            continue
#        ls = os.listdir(my_dir)
#	theInputFiles.extend([my_dir[:] + x for x in ls if x.endswith('root')])
#    return theInputFiles
#inputdir = ['/eos/uscms/store/user/lpcgem/DarkSUSY_MH-125_MGammaD-20000_ctau100_14TeV_madgraph-pythia6-tauola/DarkSUSY_mH_125_mGammaD_20000_cT_100_14TeV_PU140_FakePad_v1/170517_201120/0000/']
#inputdir = ['/eos/uscms/store/user/lpcgem/DarkSUSY_MH-125_MGammaD-20000_ctau1000_14TeV_madgraph-pythia6-tauola/DarkSUSY_mH_125_mGammaD_20000_cT_1000_14TeV_PU140_FakePad_v1/170517_201245/0000/']
#allfiles = useInputDir(inputdir)


parser = argparse.ArgumentParser(description='Prepare and submit ntupling jobs')
parser.add_argument("-j", "--jobdir", dest="jobdir", default="jobs", help="Directory for job files. [Default: jobs]")
#parser.add_argument("-o", "--outdir", dest="outdir", default="/eos/uscms/store/user/${USER}/13TeV/ntuples", help="Output directory for ntuples. [Default: \"/eos/uscms/store/user/${USER}/13TeV/ntuples\"]")
#parser.add_argument("-i", "--indir", dest="indir", default="/eos/uscms/store/user/${USER}/13TeV/ntuples", help="Input directory for ntuples. [Default: \"/eos/uscms/store/user/${USER}/13TeV/ntuples\"]")

args = parser.parse_args()

script = "transferSample.sh"

#allfiles = useInputDir([args.indir])

os.system("mkdir -p %s" % args.jobdir)
os.system("mkdir -p %s/logs" % args.jobdir)
#if (args.outdir.startswith("/eos/cms/store/user") or args.outdir.startswith("/store/user") ) and not(os.path.isdir(args.ourdir)):
#	os.system("%s mkdir -p %s" % (eos, args.outdir))
#else :
#	os.system("mkdir -p %s" % args.outdir)
file_per_job = 1
Jobid_start = 0
Jobid_end = 642
NJobs = (Jobid_end-Jobid_start)/file_per_job + 1
print "Nstart ",Jobid_start, " end ", Jobid_end, " Total jobs ",NJobs
#for ijob in range(args.numjobs) :
for ijob in range(NJobs):
    	Nstart = Jobid_start + file_per_job * ijob
	Nend = Jobid_start + file_per_job * (ijob + 1 ) -1
	if Nend > Jobid_end:
	    Nend = Jobid_end

	jobscript = open("{0}/submit_{1}.sh".format(args.jobdir, ijob), "w")
	jobscript.write("""
cat > submit_{num}.cmd <<EOF
universe                = vanilla
Requirements            = (Arch == "X86_64") && (OpSys == "LINUX")
request_disk            = 10000000
Executable              = {runscript}
Arguments               = {Nstart} {Nend}
Output                  = {jobdir}/logs/out_{num}.out
Error                   = {jobdir}/logs/out_{num}.err
Log                     = {jobdir}/logs/out_{num}.log
use_x509userproxy       = true
x509userproxy           = $X509_USER_PROXY
Should_Transfer_Files   = YES
WhenToTransferOutput    = ON_EXIT
Queue
EOF

condor_submit submit_{num}.cmd;
rm submit_{num}.cmd""".format(
			runscript=script, Nstart = Nstart, Nend = Nend, num = ijob, jobdir = args.jobdir
			))
	jobscript.close()
	os.system("chmod +x %s/submit_%d.sh" % (args.jobdir, ijob))
submitall = "submitall%s.sh"%args.jobdir
subscript = open(submitall, "w")	
subscript.write("""	
#!/bin/bash
""")

for ijob in range(NJobs) :
	subscript.write("""
./{jobdir}/submit_{num}.sh
sleep 0.1
""".format(jobdir=args.jobdir,num=ijob)
	)

subscript.close()
os.system("chmod +x "+submitall)
#os.system("source "+submitall)
