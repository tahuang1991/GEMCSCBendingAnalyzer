
cat > submit_292.cmd <<EOF
universe                = vanilla
Requirements            = (Arch == "X86_64") && (OpSys == "LINUX")
request_disk            = 10000000
Executable              = produceAnaNtuples.sh
Arguments               = runSliceTestAnalysis_condor.py step3_292.root /eos/uscms/store/group/lpcgem/SingleMuon_Run2017G_v1_RECO/ /eos/uscms/store/user/mkhurana/GEMCSCBending_2017G/ out_ana_292.root -1 ${CMSSW_VERSION} ${USER}
Output                  = logs/out_292.out
Error                   = logs/out_292.err
Log                     = logs/out_292.log
use_x509userproxy       = true
x509userproxy           = $X509_USER_PROXY
initialdir              = jobs
Should_Transfer_Files   = YES
transfer_input_files    = ${CMSSW_BASE}/runSliceTestAnalysis_condor.py
WhenToTransferOutput    = ON_EXIT
Queue
EOF

condor_submit submit_292.cmd;
rm submit_292.cmd