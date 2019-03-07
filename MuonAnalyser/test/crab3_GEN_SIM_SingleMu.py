from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
#section general
config.General.requestName = 'SingleMu_Pt30_GEN_SIM_1M'
config.General.workArea = 'SingleMu_Pt30_MC_1M_20190304'#working dir 
config.General.transferOutputs = True
config.General.transferLogs = True

#section JobType
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'SingleMuPt100_pythia8_cfi_GEN_SIM.py'
config.JobType.maxMemoryMB = 2000
config.JobType.maxJobRuntimeMin = 1440 # 1440min = 24hours
config.JobType.numCores = 1
config.JobType.allowUndistributedCMSSW = True
#config.JobType.generator
#config.JobType.pyCfgParams
#config.JobType.inputFiles


#section Data
#config.Data.inputDataset = '/SLHC23_patch1_2023Muon_gen_sim_Pt2_50_1M/tahuang-SLHC25_patch1_2023Muon_1M_L1_PU0_Pt2_50_updategemeta-1bf93df4dfbb43dc918bd6e47dedbf79/USER'
#config.Data.inputDataset = '/SingleMuon/Run2016G-v1/RAW'
#config.Data.inputDataset = '/SingleMuon/Run2016H-v1/RAW'
#config.Data.inputDataset = '/SingleMuon/tahuang-RERECO_Run2018D_singlemuon_GEMon_320995-321475_20180917-8a1254d3d0a422ad143b7aead0544ce7/USER'
#config.Data.inputDataset = '/SingleMuon/tahuang-RERECO_Run2018D_singlemuon_GEMon_323470-324200_20181005-4201715c0f9d22f1f7baffdbca473c7b/USER'
config.Data.inputDataset = None
config.Data.splitting = 'EventBased'
#config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
#config.Data.inputDBS = 'phys03'
#config.Data.inputDBS = 'global'
config.Data.unitsPerJob = 1000
NJOBS = 1000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
#config.Data.outLFNDirBase = '/store/user/tahuang/'
config.Data.outLFNDirBase = '/store/group/lpcgem/'
config.Data.publication = True
#import FWCore.PythonUtilities.LumiList as LumiList
##lumiList = LumiList(filename='my_original_lumi_mask.json')
#lumiList = LumiList(filename='320887_13TeV_PromptReco_Collisions18_JSON_MuonPhys.txt')
#lumiList.selectRuns(runs = [321475, 321461,  321457,  321434,  321433,  321432,  321431,  321415,  321414,  321396,  321393,  321313,  321312,  321311, 321310,  321305,  321218,  321178,  321177,  321167,  321166,  321165,  321164,  321162,  321149,  321140,  321138,  321134,  321126, 321123,  321122,  321121,  321119,  321069,  321068,  321067,  321055,  321051,  320996,  320995])
#lumiList.writeJSON('my_lumi_mask.json')
#config.Data.lumiMask = 'my_lumi_mask.json'
#process.source.lumisToProcess = LumiList.LumiList(filename = 'goodList.json').getVLuminosityBlockRange()
config.Data.outputPrimaryDataset = "SingleMuon_Pt30_Eta0To2p5_Extended2023D17_phase2_realistic_1M"
config.Data.outputDatasetTag = config.General.requestName
config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.ignoreGlobalBlacklist = True
#config.Site.whitelist = ["T0_CH_CERN_MSS"]
