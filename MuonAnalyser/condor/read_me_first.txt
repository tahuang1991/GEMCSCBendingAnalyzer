step1: initialize your grid certificate by grid-proxy-init -debug -verify

step2: run following command to create the scripts to submit condor jobs
python  produceSample.py -i /eos/uscms/store/group/lpcgem/SingleMuon_Run2017G_v1_RECO/ -o  /eos/uscms/store/user/mkhurana/GEMCSCBending_2017G/


step3:  run submitalljobs.sh




to test the configuration
cmsRun runSliceTestAnalysis_condor.py inputFiles=file:/eos/uscms/store/group/lpcgem/SingleMuon_Run2017G_v1_RECO/step3_313.root outputFile=/eos/uscms/store/user/tahuang/GEMCSCBending_2017G/out_ana_0.root
