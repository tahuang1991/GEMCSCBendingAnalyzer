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
#process.maxEvents.input = cms.untracked.int32(100)
# Input source
process.source = cms.Source("PoolSource", 
	#fileNames = cms.untracked.vstring()
	fileNames = cms.untracked.vstring(options.inputFiles)
	)
#process.source.skipEvents = cms.untracked.uint32(17601)
#fname = 'singleMuon.txt'
#f = open(fname)
#for line in f:
#    process.source.fileNames.append(line)


process.TFileService = cms.Service("TFileService",
	#fileName = cms.string("histo.root")
	fileName = cms.string(options.outputFile)
	)

process.SliceTestAnalysis = cms.EDAnalyzer('SliceTestAnalysis',
    process.MuonServiceProxy,
    gemRecHits = cms.InputTag("gemRecHits"),
    cscRecHits = cms.InputTag("csc2DRecHits"),
    csclcts = cms.InputTag("muonCSCDigis", "MuonCSCCorrelatedLCTDigi"),
    cscSegments = cms.InputTag("cscSegments"),
    muons = cms.InputTag("muons"),
    vertexCollection = cms.InputTag("offlinePrimaryVertices"),
    matchMuonwithLCT = cms.untracked.bool(False),
)
process.p = cms.Path(process.SliceTestAnalysis)