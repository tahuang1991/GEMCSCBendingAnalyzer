#!/bin/bash



echo `hostname`
echo "${_CONDOR_SCRATCH_DIR}"
echo "scramdir: $scramdir"
echo "workdir: $workdir"
#ls -l
#export X509_USER_PROXY=/tmp/x509up_u48645
#cp $HOME/x509up_u48645 ${_CONDOR_SCRATCH_DIR}
#export X509_USER_PROXY=${_CONDOR_SCRATCH_DIR}/x509up_u48645
ls -l
#ls /tmp
#cat x509up_u48645
voms-proxy-info -all

destinationdir=/eos/uscms/store/user/mkhurana/2018C_data_files/

#destinationdir=/eos/uscms/store/group/lpcgem/SingleMuon_Run2018C_v1_RECO/
#file_to_transfer=root://cms-xrdr.sdfarm.kr:1094//xrd/store/user/jlee/SingleMuon/Run2017G-v1/RECOv2/step3_000.root
Nstart=$1
Nend=$2

echo "destination: "$destinationdir
for i in $(seq -f "%03g" $Nstart $Nend)
do 
    file_to_transfer=root://cms-xrdr.sdfarm.kr:1094//xrd/store/user/jlee/SingleMuon/Run2018C-v1/RECOv2/step3_$i.root
    echo "To transfer file: "$file_to_transfer
    xrdcp -d 1 -f $file_to_transfer root://cmseos:1094/$destinationdir
#echo $i
done

#echo "copy it to local"
#xrdcp -d 1 -f $file_to_transfer .


#echo "command xrdcp -d 1 -f $file_to_transfer $destinationdir"

#xrdcp -d 1 -f $file_to_transfer root://cmseos:1094/$destinationdir


status=`echo $?`
echo "Status = $status"
exit $status
