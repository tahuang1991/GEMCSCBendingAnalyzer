
cat > submit_92.cmd <<EOF
universe                = vanilla
Requirements            = (Arch == "X86_64") && (OpSys == "LINUX")
request_disk            = 10000000
Executable              = produceAnaNtuples.sh
Arguments               = runSliceTestAnalysis_condor.py step3_092.root /eos/uscms/store/group/lpcgem/SingleMuon_Run2017G_v1_RECO/ /eos/uscms/store/user/mkhurana/GEMCSCBending_2017G/ out_ana_92.root -1 ${CMSSW_VERSION} ${USER}
Output                  = logs/out_92.out
Error                   = logs/out_92.err
Log                     = logs/out_92.log
use_x509userproxy       = true
x509userproxy           = $X509_USER_PROXY
initialdir              = jobs
Should_Transfer_Files   = YES
transfer_input_files    = ${CMSSW_BASE}/runSliceTestAnalysis_condor.py , /uscms_data/d3/mkhurana/CMSSW_10_1_5/src/GEMCSCBendingAnalyzer/MuonAnalyser/plugins/SliceTestAnalysis.cc
WhenToTransferOutput    = ON_EXIT
Queue
EOF

condor_submit submit_92.cmd;
rm submit_92.cmd