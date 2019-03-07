# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --runUnscheduled --conditions auto:phase2_realistic --era Phase2 -s RAW2DIGI,RECO --datatier GEN-SIM-DIGI-RAW-RECO -n 10 --eventcontent FEVTDEBUGHLT --beamspot HLLHC14TeV --geometry Extended2023D17 --filein file:step2.root --fileout file:step3.root
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO',eras.Phase2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/eos/uscms/store/user/tahuang/SingleMuon_Pt30_Eta1p0To2p5_Extended2023D17_phase2_realistic_50k/SingleMu_Pt30_MC_DIGI_L1_DIGI2RAW_phase2_20190227/190228_181259/0000/step2_1.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW-RECO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:step3_skimed.root'),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    #SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('GEMRecHitSkim')),
    splitLevel = cms.untracked.int32(0)
)

process.FEVTDEBUGHLToutput.outputCommands.append('drop *_hgcal*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_simEcal*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_simHcal*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_simHGcal*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_HGC*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_simHGC*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_hfreco*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_hfprereco*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_towerMaker*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_simCal*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_ecal*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *_hcal*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop recoPF*_*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop *recoJet*_*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop PCaloHits*_*_*_*')
#process.FEVTDEBUGHLToutput.outputCommands.append('drop recoTrackExtras*_*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop TrackingRecHitsOwned_*_*_*')
process.FEVTDEBUGHLToutput.outputCommands.append('drop FEDRawDataCollection_rawDataCollector__DIGI2RAW')
"""
"""
# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step,process.endjob_step,process.FEVTDEBUGHLToutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)


# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
