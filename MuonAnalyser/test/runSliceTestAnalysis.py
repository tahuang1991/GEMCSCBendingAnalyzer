import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process('SliceTestAnalysis',eras.Run2_2017,eras.run3_GEM)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('RecoMuon.TrackingTools.MuonServiceProxy_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '101X_dataRun2_Prompt_v10', '')
#process.MessageLogger.cerr.FwkReport.reportEvery = 5000

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.maxEvents.input = cms.untracked.int32(10)
# Input source
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())
#process.source.skipEvents = cms.untracked.uint32(17601)

#process.source.fileNames.append('/store/data/Run2018B/Cosmics/AOD/PromptReco-v1/000/317/428/00000/E4BC1D7B-3F6A-E811-9E05-FA163E57A064.root')
process.source.fileNames.append('file:/eos/uscms/store/group/lpcgem/SingleMuon_Run2017G_v1_RECO/step3_313.root')

#fname = 'singleMuon.txt'
#f = open(fname)
#for line in f:
#    process.source.fileNames.append(line)

process.options = cms.untracked.PSet()

process.TFileService = cms.Service("TFileService",fileName = cms.string("histo.root"))

process.SliceTestAnalysis = cms.EDAnalyzer('SliceTestAnalysis',
    process.MuonServiceProxy,
    gemRecHits = cms.InputTag("gemRecHits"),
    cscRecHits = cms.InputTag("csc2DRecHits"),
    muons = cms.InputTag("muons"),
    vertexCollection = cms.InputTag("offlinePrimaryVertices"),
)
process.p = cms.Path(process.SliceTestAnalysis)
