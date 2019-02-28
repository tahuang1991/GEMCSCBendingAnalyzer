import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

#process = cms.Process('SliceTestAnalysis',eras.Run2_2017,eras.run3_GEM)
process = cms.Process('SliceTestAnalysis',eras.Phase2)

process.load("FWCore.MessageService.MessageLogger_cfi")
#process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D17_cff')
process.load('RecoMuon.TrackingTools.MuonServiceProxy_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '101X_dataRun2_Prompt_v10', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, '103X_dataRun2_Prompt_v1', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic','')
#process.MessageLogger.cerr.FwkReport.reportEvery = 5000
process.MessageLogger.cerr.FwkReport.reportEvery = 5000

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.register ('nEvents',
                      -1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Number of events")
options.parseArguments()


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.nEvents)
)
process.maxEvents.input = cms.untracked.int32(5000)

#process.gemSkim = cms.EDFilter("GEMSkim",gemRecHits = cms.InputTag("gemRecHits"))
#process.GEMRecHitSkim = cms.Path(process.gemSkim)
# Input source
process.source = cms.Source("PoolSource", 
                            fileNames = cms.untracked.vstring(options.inputFiles),
                            inputCommands = cms.untracked.vstring(
		"keep *",
                "drop TotemTimingDigiedmDetSetVector_totemTimingRawToDigi_TotemTiming_reRECO",
                "drop TotemTimingRecHitedmDetSetVector_totemTimingRecHits__reRECO"
                )
                            )
#process.source.skipEvents = cms.untracked.uint32(17601)
#file:/eos/uscms/store/group/lpcgem/SingleMuon_Run2017G_v1_RECO/            #directory on LPC where all 555 files are placed
#process.source.fileNames.append('file:/eos/uscms/store/group/lpcgem/SingleMuon_Run2018C_v1_RECO/step3_001.root')
#process.source.fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW-RECO/ZMu-PromptReco-v2/000/320/500/00000/9AC95BCF-8C95-E811-A24D-FA163E67426E.root')
#process.source.fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/AOD/PromptReco-v2/000/320/500/00000/FE2B5583-8C95-E811-B8F8-FA163ED06560.root')
#process.source.fileNames = cms.untracked.vstring('root://cmsxrootd-site.fnal.gov//store/data/Run2018D/SingleMuon/AOD/PromptReco-v2/000/321/051/00000/4E64F14D-9A9D-E811-9C5C-FA163E2B2370.root')
#process.source.fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/MINIAOD/PromptReco-v2/000/321/475/00000/AA10A5A1-77A6-E811-B57C-FA163EF0320D.root')
#process.source.fileNames.append('file:/eos/uscms/store/user/lpcgem/SingleMuon/RERECO_Run2018D_singlemuon_GEMon_323470-324200_20181005/181008_152602/0000/step3_283.root')
process.source.fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/relval/CMSSW_10_3_0_pre4/RelValSingleMuPt15Eta1p7_2p7/GEN-SIM-RECO/103X_upgrade2023_realistic_v2_2023D17noPUEA1000-v1/20000/5A534D0E-4003-ED43-AE4C-8D30015B49B7.root')

#fname = 'singleMuon.txt'
#f = open(fname)
#for line in f:
#    process.source.fileNames.append(line)

process.options = cms.untracked.PSet()

#process.TFileService = cms.Service("TFileService",fileName =cms.string(options.outputFile))
process.TFileService = cms.Service("TFileService",fileName =cms.string("out_ana.root"))


process.SliceTestAnalysis = cms.EDAnalyzer('SliceTestAnalysis',
    process.MuonServiceProxy,
    gemRecHits = cms.InputTag("gemRecHits"),
    cscRecHits = cms.InputTag("csc2DRecHits"),
    csclcts = cms.InputTag("muonCSCDigis", "MuonCSCCorrelatedLCTDigi"),
    cscSegments = cms.InputTag("cscSegments"),
    muons = cms.InputTag("muons"),
    vertexCollection = cms.InputTag("offlinePrimaryVertices"),
    matchMuonwithLCT = cms.untracked.bool(False),
    matchMuonwithCSCRechit = cms.untracked.bool(False),
    applyGEMalignment = cms.untracked.bool(False),
    GEM_alginment_deltaX = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    #GEM_alginment_deltaX = cms.vdouble(-0.16968, -0.1421, 0.1139,  0.1242,  -0.30713,  -0.33472, 0.37761, 0.36531),
    #GEM_alginment_deltaX = cms.vdouble(-0.152, -0.145, 0.1382, 0.1345, -0.2737, -0.2939, 0.387, 0.377),

    #runs = cms.vint32(321475, 321461,  321457,  321434,  321433,  321432,  321431,  321415,  321414,  321396,  321393,  321313,  321312,  321311, 321310,  321305,  321218,  321178,  321177,  321167,  321166,  321165,  321164,  321162,  321149,  321140,  321138,  321134,  321126, 321123,  321122,  321121,  321119,  321069,  321068,  321067,  321055,  321051,  320996,  320995),
    
)

process.p = cms.EndPath(process.SliceTestAnalysis)

