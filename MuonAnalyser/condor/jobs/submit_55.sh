
cat > submit_55.cmd <<EOF
universe                = vanilla
Requirements            = (Arch == "X86_64") && (OpSys == "LINUX")
request_disk            = 10000000
Executable              = produceAnaNtuples.sh
Arguments               = runSliceTestAnalysis_condor.py step3_055.root /eos/uscms/store/group/lpcgem/SingleMuon_Run2017G_v1_RECO/ /eos/uscms/store/user/mkhurana/GEMCSCBending_2017G/ out_ana_55.root -1 ${CMSSW_VERSION} ${USER}
Output                  = logs/out_55.out
Error                   = logs/out_55.err
Log                     = logs/out_55.log
use_x509userproxy       = true
x509userproxy           = $X509_USER_PROXY
initialdir              = jobs
Should_Transfer_Files   = YES
transfer_input_files    = ${CMSSW_BASE}/runSliceTestAnalysis_condor.py
WhenToTransferOutput    = ON_EXIT
Queue
EOF

condor_submit submit_55.cmd;
rm submit_55.cmd