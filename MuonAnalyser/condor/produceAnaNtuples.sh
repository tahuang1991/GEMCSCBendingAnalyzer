#!/bin/bash
##instruction
## https://uscms.org/uscms_at_work/physics/computing/setup/batch_systems.shtml

cfgfile=$1
inputname=$2
inputdir=$3
outputdir=$4
outputname=$5
maxevents=$6
cmssw_version=$7
username=$8

workdir=`pwd`

echo `hostname`
echo "${_CONDOR_SCRATCH_DIR}"
echo "workdir: $workdir"  ## should be the same as ${_CONDOR_SCRATCH_DIR}
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
echo "args: $*"
#xrdcp root://cmseos.fnal.gov//store/group/lpcgem/SingleMuon_Run2017G_v1_RECO/step3_000.root
xrdcp -s root://cmseos.fnal.gov//store/user/$username/${cmssw_version}.tar.gz .
tar -xf ${cmssw_version}.tar.gz
rm ${cmssw_version}.tar.gz


ls -l 

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $cmssw_version/src/
SCRAM_ARCH=slc6_amd64_gcc491
eval `scramv1 runtime -sh`
scramv1 b

cd $workdir

#### transfer intput file
if [[ "$inputdir" =~ ^/eos/uscms/.* ]]; then
   copypath=`echo ${inputdir} | sed "s:/eos/uscms::"`
   echo "copy input file from root://cmseos.fnal.gov/"$copypath/${inputname}
   xrdcp root://cmseos.fnal.gov/${copypath}/${inputname} .
else
   cp ${inputdir}/${inputname} .
fi
   

cmsRun $cfgfile print inputFiles=file:${inputname} outputFile=${outputname} nEvents=${maxevents}

status=`echo $?`
echo "Status = $status"

if [[ "$outputdir" =~ ^/eos/uscms/.* ]]; then
  copypath=`echo ${outputdir} | sed "s:/eos/uscms::"`
  xrdcp -np ${outputname} root://cmseos:1094/${copypath}/
  rm ${outputname}
else
  mv ${outputname} ${outputdir}/
fi


cd ${_CONDOR_SCRATCH_DIR}
rm -rf ${cmssw_version}
rm ${inputname}

exit $status
