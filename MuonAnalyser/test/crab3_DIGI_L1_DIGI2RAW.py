from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
###2018runA  314472-318876
config.General.requestName = 'SingleMu_Pt30_MC_DIGI_L1_DIGI2RAW_phase2'
config.General.workArea = 'SingleMu_Pt30_MC_1M_20190304'#working dir 
config.General.transferOutputs = True
config.General.transferLogs = True

#section JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step2_DIGI_L1_DIGI2RAW.py'
config.JobType.maxMemoryMB = 4000
config.JobType.maxJobRuntimeMin = 1440 # 1440min = 24hours
config.JobType.numCores = 1
config.JobType.allowUndistributedCMSSW = True
#config.JobType.generator
#config.JobType.pyCfgParams
#config.JobType.inputFiles


#config.Data.inputDataset = '/SingleMuon/Run2018D-PromptReco-v2/AOD'
#config.Data.inputDataset = '/SingleMuon_Pt30_Eta1p0To2p5_Extended2023D17_phase2_realistic_50k/tahuang-SingleMu_Pt30_GEN_SIM_20190227-81a357cef3dffc8cd647539309e1b14a/USER'
config.Data.inputDataset = '/SingleMuon_Pt30_Eta0To2p5_Extended2023D17_phase2_realistic_1M/tahuang-SingleMu_Pt30_GEN_SIM_1M-13c7df0f83ac56a5a322fff97b8c6fa0/USER'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.inputDBS = 'phys03'
config.Data.unitsPerJob = 1
#config.Data.outLFNDirBase = '/store/user/tahuang/'
config.Data.outLFNDirBase = '/store/group/lpcgem/'
config.Data.publication = True
#import FWCore.PythonUtilities.LumiList as LumiList
#lumiList = LumiList.LumiList(filename = 'Cert_314472-320887_13TeV_PromptReco_Collisions18_JSON_MuonPhys.txt')
#lumiList = LumiList.LumiList(url = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-321221_13TeV_PromptReco_Collisions18_JSON_MuonPhys.txt')
#lumiList = LumiList.LumiList(url = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-321221_13TeV_PromptReco_Collisions18_JSON.txt')
#lumiList.selectRuns([321475, 321461,  321457,  321434,  321433,  321432,  321431,  321415,  321414,  321396,  321393,  321313,  321312,  321311, 321310,  321305,  321218,  321178,  321177,  321167,  321166,  321165,  321164,  321162,  321149,  321140,  321138,  321134,  321126, 321123,  321122,  321121,  321119,  321069,  321068,  321067,  321055,  321051,  320996,  320995])
#print "lumiList ",lumiList
#lumiList.writeJSON('my_lumi_mask.json')
#config.Data.lumiMask = 'my_lumi_mask.json'
#process.source.lumisToProcess = LumiList.LumiList(filename = 'goodList.json').getVLuminosityBlockRange()
#config.Data.runRange = '%d-%d'%(runstart, runend)#'315257-315270'#'278820-278820' # '193093-194075'
config.Data.outputDatasetTag = config.General.requestName
config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.ignoreGlobalBlacklist = True
#config.Site.whitelist = ["T0_CH_CERN_MSS"]
