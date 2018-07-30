#!/usr/bin/python
import os
import sys
import re
import argparse
import subprocess

##### intruction from fermilab
### https://uscms.org/uscms_at_work/physics/computing/setup/batch_systems.shtml
#####
## helper for files on dCache/EOS (LPC)
def useInputDir(inputDir):
    theInputFiles = []
    for d in range(len(inputDir)):
        my_dir = inputDir[d]
        if not os.path.isdir(my_dir):
            print "ERROR: This is not a valid directory: ", my_dir
            if d==len(inputDir)-1:
                print "ERROR: No input files were selected"
                exit()
            continue
        ls = os.listdir(my_dir)
	theInputFiles.extend([my_dir[:] + x for x in ls if x.endswith('root')])
    return theInputFiles
#allfiles = useInputDir(inputdir)
#inputdir = ['/eos/uscms/store/group/lpcgem/SingleMuon_Run2017G_v1_RECO/']

	    

parser = argparse.ArgumentParser(description='Prepare and submit ntupling jobs')
parser.add_argument("-c", "--config", dest="config", default="runSliceTestAnalysis_condor.py", help="Configuration file to be run using cmsRun to run. [Default: runSliceTestAnalysis_condor.py]")
parser.add_argument("-j", "--jobdir", dest="jobdir", default="jobs", help="Directory for job files. [Default: jobs]")
parser.add_argument("-o", "--outdir", dest="outdir", default="/eos/uscms/store/user/${USER}/13TeV/ntuples", help="Output directory for ntuples. [Default: \"/eos/uscms/store/user/${USER}/13TeV/ntuples\"]")
parser.add_argument("-i", "--indir", dest="indir", default="/eos/uscms/store/user/${USER}/13TeV/ntuples", help="Input directory for ntuples. [Default: \"/eos/uscms/store/user/${USER}/13TeV/ntuples\"]")


args = parser.parse_args()

script = "produceAnaNtuples.sh"
workdir_cmssw = "/uscms_data/d3/tahuang/GEMCSCBending/"
eosdir = "/eos/uscms/store/user/tahuang/"

allfiles = useInputDir([args.indir])

os.system("mkdir -p %s" % args.jobdir)
os.system("mkdir -p %s/logs" % args.jobdir)
if args.outdir.startswith("/eos/cms/store/user") or args.outdir.startswith("/store/user") :
	os.system("%s mkdir -p %s" % (eos, args.outdir))
else :
	os.system("mkdir -p %s" % args.outdir)


#for ijob in range(args.numjobs) :
for ijob in range(len(allfiles)):
        inputfile = allfiles[ijob]
	inputfilename = inputfile.split('/')[-1]
	inputdir = inputfile.replace(inputfilename, '') ## should be args.indir
	#print "inputfile ",inputfile," infilename ", inputfilename," inputdir ",inputdir
	outfile = "out_ana_{0}.root".format(ijob)
	jobscript = open("{0}/submit_{1}.sh".format(args.jobdir, ijob), "w")
	jobscript.write("""
cat > submit_{num}.cmd <<EOF
universe                = vanilla
Requirements            = (Arch == "X86_64") && (OpSys == "LINUX")
request_disk            = 10000000
Executable              = {runscript}
Arguments               = {cfg} {infilename} {inputdir} {outputdir} {outputname} {maxevents} {cmssw_version} {username}
Output                  = logs/out_{num}.out
Error                   = logs/out_{num}.err
Log                     = logs/out_{num}.log
use_x509userproxy       = true
x509userproxy           = $X509_USER_PROXY
initialdir              = {jobdir}
Should_Transfer_Files   = YES
transfer_input_files    = {workdir}/{cfg}
WhenToTransferOutput    = ON_EXIT
Queue
EOF

condor_submit submit_{num}.cmd;
rm submit_{num}.cmd""".format(
			runscript=script, cfg=args.config, workdir="${CMSSW_BASE}", num=ijob, jobdir=args.jobdir, outputdir=args.outdir, outputname=outfile, maxevents=-1, infilename=inputfilename, inputdir=inputdir, cmssw_version="${CMSSW_VERSION}", username="${USER}"
			))
	jobscript.close()
	os.system("chmod +x %s/submit_%d.sh" % (args.jobdir, ijob))
submitall = "submitall%s.sh"%args.jobdir
subscript = open(submitall, "w")	
subscript.write("""	
#!/bin/bash
currentpath=`pwd`
cd {workdir}
tar --exclude-caches-all --exclude-vcs -zcf $CMSSW_VERSION.tar.gz -C $CMSSW_VERSION/.. $CMSSW_VERSION --exclude=tmp
cp $CMSSW_VERSION.tar.gz  {eosdir}
cd  $currentpath
""".format(workdir = workdir_cmssw, eosdir = eosdir))


for ijob in range(len(allfiles)) :
	subscript.write("""
./{jobdir}/submit_{num}.sh
sleep 0.1
""".format(jobdir=args.jobdir,num=ijob)
	)

subscript.close()
os.system("chmod +x "+submitall)
#os.system("source "+submitall)
