import FWCore.ParameterSet.Config as cms

demo = cms.EDAnalyzer('MuonAnalyser'
     ,tracks = cms.untracked.InputTag('ctfWithMaterialTracks')
)
