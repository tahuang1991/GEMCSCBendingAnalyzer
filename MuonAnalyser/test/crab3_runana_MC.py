from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
###2018runA  314472-318876
#section general
config.General.requestName = 'GEMCSCAan_crab_SingleMuPt30_MC_50k_20190304v2'
config.General.workArea = 'GEMCSCAna_crab_SingleMuPt30_RECO_GEMon_MC'#working dir 
config.General.transferOutputs = True
config.General.transferLogs = True

#section JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'runSliceTestAnalysis_MC.py'
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
#config.Data.inputDataset = '/RelValSingleMuPt15Eta1p7_2p7/CMSSW_10_3_0_pre4-103X_upgrade2023_realistic_v2_2023D17noPUEA1000-v1/GEN-SIM-RECO'
#config.Data.inputDataset = '/SingleMuon/Run2018D-ZMu-PromptReco-v2/RAW-RECO'
config.Data.inputDataset = '/SingleMuon_Pt30_Eta1p0To2p5_Extended2023D17_phase2_realistic_50k/tahuang-SingleMu_Pt30_MC_RAW2DIGI_RECO_phase2_20190227-b2cf3352cf25f5bc56c1d440af858916/USER'
config.Data.inputDBS = 'phys03'
#config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/tahuang/'
#config.Data.outLFNDirBase = '/store/group/lpcgem/'
config.Data.publication = False
#import FWCore.PythonUtilities.LumiList as LumiList
##lumiList = LumiList(filename='my_original_lumi_mask.json')
#lumiList = LumiList(filename='320887_13TeV_PromptReco_Collisions18_JSON_MuonPhys.txt')
#lumiList.selectRuns(runs = [321475, 321461,  321457,  321434,  321433,  321432,  321431,  321415,  321414,  321396,  321393,  321313,  321312,  321311, 321310,  321305,  321218,  321178,  321177,  321167,  321166,  321165,  321164,  321162,  321149,  321140,  321138,  321134,  321126, 321123,  321122,  321121,  321119,  321069,  321068,  321067,  321055,  321051,  320996,  320995])
#lumiList.writeJSON('my_lumi_mask.json')
#config.Data.lumiMask = 'my_lumi_mask.json'
#process.source.lumisToProcess = LumiList.LumiList(filename = 'goodList.json').getVLuminosityBlockRange()
#config.Data.runRange = '%d-%d'%(runstart, runend)#'315257-315270'#'278820-278820' # '193093-194075'
config.Data.outputDatasetTag = config.General.requestName
config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.ignoreGlobalBlacklist = True
#config.Site.whitelist = ["T0_CH_CERN_MSS"]
