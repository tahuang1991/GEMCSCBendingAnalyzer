// system include files
#include <assert.h> 
#include <memory>
#include <cmath>
#include <iostream>
#include <sstream>
#include <boost/foreach.hpp>
#define foreach BOOST_FOREACH


// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

//#include "RecoMuon/TrackingTools/interface/MuonSegmentMatcher.h"
#include "RecoMuon/TrackingTools/interface/MuonServiceProxy.h"
#include "TrackingTools/GeomPropagators/interface/Propagator.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackPropagation/SteppingHelixPropagator/interface/SteppingHelixPropagator.h"
#include "MagneticField/Engine/interface/MagneticField.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/TrackReco/interface/Track.h"

#include "DataFormats/CSCRecHit/interface/CSCRecHit2D.h"
#include "DataFormats/CSCRecHit/interface/CSCSegmentCollection.h"
#include <DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h>
#include <DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigi.h>
#include "Geometry/CSCGeometry/interface/CSCGeometry.h"

#include "DataFormats/GEMRecHit/interface/GEMRecHitCollection.h"
#include "Geometry/GEMGeometry/interface/GEMGeometry.h"
#include "Geometry/GEMGeometry/interface/GEMEtaPartitionSpecs.h"

#include "Geometry/Records/interface/MuonGeometryRecord.h"
#include "Geometry/CommonTopologies/interface/StripTopology.h"

#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "TTree.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TGraphAsymmErrors.h"
#include "TLorentzVector.h"

using namespace std;
using namespace edm;

// struct with relevant data
struct MuonData
{
  void init(); // initialize to default values
  TTree* book(TTree *t);

  Int_t lumi;
  Int_t run;
  Int_t event;

  float muonPx, muonPy, muonPz;
  float muondxy, muondz;
  int muon_ntrackhit, muon_chi2, muon_nChamber;
  float muonpt, muoneta, muonphi;
  int muoncharge;
  int muonendcap;
  float muonPFIso, muonTkIso;
  
  

  bool has_TightID;
  bool has_MediumID;
  bool has_LooseID;
  
  bool hasGEMdata;
  bool has_ME11[6];
  bool has_GE11[2];

  //Muon position at ME11
  float rechit_phi_ME11[6];//phi at each layer, from CSC rechit
  float rechit_eta_ME11[6];
  float rechit_x_ME11[6];
  float rechit_y_ME11[6];
  float rechit_localx_ME11[6];
  float rechit_localy_ME11[6];
  float rechit_r_ME11[6];
  bool rechit_used_ME11[6];
  int rechit_hitWire_ME11[6];
  int rechit_centralStrip_ME11[6];
  unsigned int rechit_nStrips_ME11[6]; 
  int rechit_halfstrip_ME11[6]; //-1
  int rechit_WG_ME11[6]; // -1
  float rechit_L1eta_ME11[6];// -9
  float rechit_L1phi_ME11[6]; //-9
  
      
  int nrechit_ME11;

  bool has_propME11[6];
  float prop_phi_ME11[6];//projected position in ME11
  float prop_eta_ME11[6];//projected position in ME11
  float prop_x_ME11[6];//projected position in ME11
  float prop_y_ME11[6];
  float prop_localx_ME11[6];//projected position in ME11
  float prop_localy_ME11[6];
  float prop_r_ME11[6];
  float propgt_x_ME11[6];//projected position in ME11
  float propgt_y_ME11[6];
  float propgt_eta_ME11[6];//projected position in ME11
  float propgt_phi_ME11[6];
  float propgt_r_ME11[6];
  float propinner_x_ME11[6];//projected position in ME11
  float propinner_y_ME11[6];
  float propinner_eta_ME11[6];//projected position in ME11
  float propinner_phi_ME11[6];
  float propinner_r_ME11[6];
  float rechit_prop_dR_ME11[6];
  float rechit_prop_dphi_ME11[6];
  int chamber_ME11[6];
  int ring_ME11[6];
  int chamber_propME11[6];
  int ring_propME11[6];

  bool has_prop_st[4];
  float prop_phi_st[4];
  float prop_eta_st[4];
  int  prop_chamber_st[4];
  int  prop_ring_st[4];
  float prop_x_st[4];
  float prop_y_st[4];
  float prop_r_st[4];

  //CSC segment matched to recoMuon
  bool has_cscseg_st[4];
  float cscseg_phi_st[4];
  float cscseg_eta_st[4];
  float cscseg_x_st[4];
  float cscseg_y_st[4];
  float cscseg_r_st[4];
  float cscseg_prop_dR_st[4];
  float cscseg_prop_dphi_st[4];
  int cscseg_chamber_st[4];
  int cscseg_ring_st[4];
  int ncscseg;
  //match LCT to recoMuon by projection
  bool has_csclct_st[4];
  float csclct_phi_st[4];
  float csclct_eta_st[4];
  float csclct_x_st[4];
  float csclct_y_st[4];
  float csclct_r_st[4];
  float csclct_prop_dR_st[4];
  float csclct_prop_dphi_st[4];
  int    csclct_chamber_st[4];
  int    csclct_ring_st[4];
  int    csclct_keyStrip_st[4];
  int    csclct_keyWG_st[4];
  int    csclct_matchWin_st[4];
  int    csclct_pattern_st[4];
  int ncscLct;

  //Muon position at GE11

  //Muon position at GE11
  bool isGood_GE11[2];
  int roll_GE11[2];
  int chamber_GE11[2];
  float rechit_phi_GE11[2];//phi,eta from GE11 rechits
  float rechit_alignedphi_GE11[2];//phi,eta from GE11 rechits
  float rechit_eta_GE11[2];
  float rechit_x_GE11[2];//rechit position in GE11
  float rechit_y_GE11[2];
  float rechit_r_GE11[2];
  float rechit_localx_GE11[2];//rechit position in GE11
  float rechit_alignedlocalx_GE11[2];//rechit position in GE11
  float rechit_localy_GE11[2];
  bool rechit_used_GE11[2];
  int rechit_BX_GE11[2];//-1
  int rechit_firstClusterStrip_GE11[2];//-1
  int rechit_clusterSize_GE11[2];//-1
  int nrechit_GE11;

  bool has_propGE11[2];
  int roll_propGE11[2];
  int chamber_propGE11[2];
  float prop_phi_GE11[2];//phi,eta from GE11 rechits
  float prop_eta_GE11[2];
  float prop_x_GE11[2];//projected position in GE11
  float prop_y_GE11[2];
  float prop_r_GE11[2];
  float prop_localx_GE11[2];//projected position in GE11
  float prop_localy_GE11[2];
  float prop_localx_center_GE11[2];//projected position in GE11

  float propgt_phi_GE11[2];//phi,eta from GE11 rechits
  float propgt_eta_GE11[2];
  float propgt_x_GE11[2];//projected position in GE11
  float propgt_y_GE11[2];
  float propgt_r_GE11[2];
  float propgt_localx_GE11[2];//projected position in GE11
  float propgt_localy_GE11[2];
  float propgt_localx_center_GE11[2];//projected position in GE11
  float propinner_phi_GE11[2];//phi,eta from GE11 rechits
  float propinner_eta_GE11[2];
  float propinner_x_GE11[2];//projected position in GE11
  float propinner_y_GE11[2];
  float propinner_r_GE11[2];
  float propinner_localx_GE11[2];//projected position in GE11
  float propinner_localy_GE11[2];
  float propinner_localx_center_GE11[2];//projected position in GE11

  float prop_strip_GE11[2];//projected position in GE11
  float rechit_prop_dR_GE11[2];
  float rechit_prop_dX_GE11[2]; // 99999
  float rechit_prop_aligneddX_GE11[2]; // 99999
  float rechit_prop_dphi_GE11[2];
  float rechit_prop_aligneddphi_GE11[2];
  float rechit_flippedStrip_GE11[2];
  
  //online
  float dphi_CSCL1_GE11L1[2];//average CSC phi - GEM phi for each GEM layer
  float dphi_fitCSCL1_GE11L1[2];// CSC phi from fit - GEM phi for each GEM layer
  //offline
  float dphi_CSCSeg_GE11Rechit[2];//average CSC phi - GEM phi for each GEM layer
  float dphi_keyCSCRechit_GE11Rechit[2];// CSC phi in key layer - GEM phi for each GEM layer
  float dphi_keyCSCRechitL1_GE11Rechit[2];// CSC phi in key layer - GEM phi for each GEM layer
  float dphi_CSCRechits_GE11Rechit[2];// CSC phi from fit - GEM phi for each GEM layer

  float dphi_CSCSeg_alignedGE11Rechit[2];//average CSC phi - GEM phi for each GEM layer
  float dphi_keyCSCRechit_alignedGE11Rechit[2];// CSC phi in key layer - GEM phi for each GEM layer
  float dphi_keyCSCRechitL1_alignedGE11Rechit[2];// CSC phi in key layer - GEM phi for each GEM layer
  
  //propagation
  float dphi_propCSC_propGE11[2];//average CSC phi - GEM phi for each GEM layer
  
};

void MuonData::init()
{
  lumi = -99;
  run = -99;
  event = -99;

  muonPx = -999999;
  muonPy = -999999;
  muonPz = -999999;
  muondxy = -1;
  muondz = -99999;
  muon_ntrackhit = 0;
  muon_nChamber = 0;
  muon_chi2 = 0;
  muonpt = 0.;
  muoneta = -9.;
  muonphi = -9.;
  muoncharge = -9;
  muonendcap = -9;
  muonPFIso = -999999;
  muonTkIso = -999999;


  has_TightID = 0;
  has_MediumID = 0;
  has_LooseID = 0;
   
  hasGEMdata = false;

  nrechit_GE11 = 0;
  nrechit_ME11 = 0;
  ncscseg = 0;
  ncscLct = 0;

  for (int i=0; i<2; ++i){
    has_GE11[i] = 0;
    has_propGE11[i] = false;
    rechit_phi_GE11[i] = -9;
    rechit_alignedphi_GE11[i] = -9;
    rechit_eta_GE11[i] = -9;
    rechit_x_GE11[i] = 99999.0;
    rechit_y_GE11[i] = 99999.0;
    rechit_localx_GE11[i] = 99999.0;
    rechit_localy_GE11[i] = 99999.0;
    rechit_r_GE11[i] = 99999.0;
    isGood_GE11[i] = 0;
    roll_GE11[i] = 0;
    chamber_GE11[i] = 0;
    prop_phi_GE11[i] = -9.0;
    prop_eta_GE11[i] = -9.0;
    prop_x_GE11[i] = 999999.0;
    prop_y_GE11[i] = 999999.0;
    prop_localx_GE11[i] = 999999.0;
    prop_localy_GE11[i] = 999999.0;
    prop_r_GE11[i] = 999999.0;
    prop_localx_center_GE11[i]=999999.0;
    prop_strip_GE11[i]=-1;
    propgt_phi_GE11[i] = -9.0;
    propgt_eta_GE11[i] = -9.0;
    propgt_x_GE11[i] = 999999.0;
    propgt_y_GE11[i] = 999999.0;
    propgt_r_GE11[i] = 999999.0;
    propgt_localx_GE11[i] = 999999.0;
    propgt_localy_GE11[i] = 999999.0;
    propgt_localx_center_GE11[i]=999999.0;
    propinner_phi_GE11[i] = -9.0;
    propinner_eta_GE11[i] = -9.0;
    propinner_x_GE11[i] = 999999.0;
    propinner_y_GE11[i] = 999999.0;
    propinner_r_GE11[i] = 999999.0;
    propinner_localx_GE11[i] = 999999.0;
    propinner_localy_GE11[i] = 999999.0;
    propinner_localx_center_GE11[i]=999999.0;
    rechit_prop_dR_GE11[i] = 9999;
    rechit_prop_dX_GE11[i] = 9999;
    rechit_prop_aligneddX_GE11[i] = 9999;
    rechit_prop_dphi_GE11[i] = -9;
    rechit_prop_aligneddphi_GE11[i] = -9;
    rechit_flippedStrip_GE11[i] = -1.0;
    //dphi_CSC_GE11[i] = -9;
    //dphi_keyCSC_GE11[i] = -9;
    //dphi_fitCSC_GE11[i] =-9;
    rechit_used_GE11[i] = false;
    rechit_BX_GE11[i] = false;//-1
    rechit_firstClusterStrip_GE11[i] = false;//-1
    rechit_clusterSize_GE11[i] = false;//-1

    roll_propGE11[i] = -1;
    chamber_propGE11[i] = -1;
    dphi_CSCL1_GE11L1[i] = -9.0;
    dphi_fitCSCL1_GE11L1[i] = -9.;
    dphi_CSCSeg_GE11Rechit[i] = -9.;
    dphi_keyCSCRechit_GE11Rechit[i] = -9.0;
    dphi_CSCRechits_GE11Rechit[i] = -9.;
    dphi_propCSC_propGE11[i] = -9.0;
    dphi_keyCSCRechitL1_GE11Rechit[i] = -9.0;

    dphi_CSCSeg_alignedGE11Rechit[i] = -9.;
    dphi_keyCSCRechit_alignedGE11Rechit[i] = -9.0;
    dphi_keyCSCRechitL1_alignedGE11Rechit[i] = -9.0;
    
  }
  for (int i=0; i<6; ++i){
    has_ME11[i] = 0;
    rechit_phi_ME11[i]=-9;
    rechit_eta_ME11[i] = -9;
    rechit_x_ME11[i] = 999999.0;
    rechit_y_ME11[i] = 999999.0;
    rechit_localx_ME11[i] = 999999.0;
    rechit_localy_ME11[i] = 999999.0;
    rechit_r_ME11[i] = 999999.0;

    rechit_prop_dphi_ME11[i]=-9;


    prop_phi_ME11[i] = -9.0;
    prop_eta_ME11[i] = -9.0;
    prop_x_ME11[i] = 99999.0;
    prop_y_ME11[i] = 99999.0;
    prop_localx_ME11[i] = 99999.0;
    prop_localy_ME11[i] = 99999.0;
    prop_r_ME11[i] = 99999.0;
    propgt_x_ME11[i] = 99999.0;
    propgt_y_ME11[i] = 99999.0;
    propgt_phi_ME11[i] = 99999.0;
    propgt_eta_ME11[i] = 99999.0;
    propgt_r_ME11[i] = 99999.0;
    propinner_x_ME11[i] = 99999.0;
    propinner_y_ME11[i] = 99999.0;
    propinner_phi_ME11[i] = 99999.0;
    propinner_eta_ME11[i] = 99999.0;
    propinner_r_ME11[i] = 99999.0;
    rechit_prop_dR_ME11[i] = 9999;
    chamber_ME11[i] = -1;
    has_propME11[i] = false;
    ring_ME11[i] = -1;
    chamber_propME11[i] = -1;
    ring_propME11[i] = -1;
    rechit_used_ME11[i] = false;
    rechit_hitWire_ME11[i] = -1;
    rechit_centralStrip_ME11[i] = -1;
    rechit_nStrips_ME11[i] = 0; 
    rechit_halfstrip_ME11[i] = -1; //-1
    rechit_WG_ME11[i] = -1; // -1
    rechit_L1eta_ME11[i] = -9;// -9
    rechit_L1phi_ME11[i] = -9; //-9


  }

  for (int i = 0; i<4; ++i) {


    has_prop_st[i] = false;
    prop_phi_st[i] = -9;
    prop_eta_st[i] = -9;
    prop_x_st[i] = -99999.0;
    prop_y_st[i] = -99999.0;
    prop_r_st[i] = 0.0;
    prop_chamber_st[i] = -1;
    prop_ring_st[i] = -1;

    has_cscseg_st[i] = false;
    cscseg_phi_st[i] = -9;
    cscseg_eta_st[i] = -9;
    cscseg_x_st[i] = -99999.0;
    cscseg_y_st[i] = -99999.0;
    cscseg_r_st[i] = 0.0;

    cscseg_prop_dR_st[i] =  99999;
    cscseg_chamber_st[i] = -1;
    cscseg_ring_st[i] = -1;
    has_csclct_st[i] =false;
    csclct_phi_st[i] = -9.0;
    csclct_eta_st[i] = -9.0;
    csclct_x_st[i] = -99999.0;
    csclct_y_st[i] = -99999.0;
    csclct_r_st[i] = 0.0;
    csclct_prop_dR_st[i] = 9999;
    csclct_chamber_st[i] = -1;

    csclct_ring_st[i] = -1;
    csclct_keyStrip_st[i] = -1;
    csclct_keyWG_st[i] = -1;
    csclct_matchWin_st[i] = 0;
    csclct_pattern_st[i] = -1;
    
    cscseg_prop_dphi_st[i]=-9;
    csclct_prop_dphi_st[i]=-9;

  }

}

TTree* MuonData::book(TTree *t)
{
  edm::Service< TFileService > fs;
  t = fs->make<TTree>("MuonData", "MuonData");

  t->Branch("lumi", &lumi);
  t->Branch("run", &run);
  t->Branch("event", &event);

  t->Branch("muonpt", &muonpt);
  t->Branch("muoneta", &muoneta);
  t->Branch("muonphi", &muonphi);
  t->Branch("muoncharge", &muoncharge);
  t->Branch("muonendcap", &muonendcap);
  t->Branch("muonPx", &muonPx);
  t->Branch("muonPy", &muonPy);
  t->Branch("muonPz", &muonPz);
  t->Branch("muondxy", &muondxy);
  t->Branch("muondz", &muondz);
  t->Branch("muon_ntrackhit", &muon_ntrackhit);
  t->Branch("muon_chi2", &muon_chi2);
  t->Branch("muonPFIso", &muonPFIso);
  t->Branch("muonTkIso", &muonTkIso);
  t->Branch("muon_nChamber", &muon_nChamber);

  t->Branch("has_MediumID", &has_MediumID);
  t->Branch("has_LooseID", &has_LooseID);  
  t->Branch("has_TightID", &has_TightID);
  t->Branch("hasGEMdata", &hasGEMdata);


  t->Branch("has_ME11", has_ME11, "has_ME11[6]/B");
  t->Branch("chamber_ME11", chamber_ME11, "chamber_ME11[6]/I");
  t->Branch("has_propME11", has_propME11, "has_propME11[6]/B");
  t->Branch("ring_ME11", ring_ME11, "ring_ME11[6]/I");
  t->Branch("chamber_propME11", chamber_propME11, "chamber_propME11[6]/I");
  t->Branch("ring_propME11", ring_propME11, "ring_propME11[6]/I");
  t->Branch("rechit_phi_ME11", rechit_phi_ME11, "rechit_phi_ME11[6]/F");
  t->Branch("rechit_eta_ME11", rechit_eta_ME11, "rechit_eta_ME11[6]/F");
  t->Branch("rechit_x_ME11", rechit_x_ME11, "rechit_x_ME11[6]/F");
  t->Branch("rechit_y_ME11", rechit_y_ME11, "rechit_y_ME11[6]/F");
  t->Branch("rechit_r_ME11", rechit_r_ME11, "rechit_r_ME11[6]/F");
  t->Branch("rechit_localx_ME11",rechit_localx_ME11,"rechit_localx_ME11[6]/F");
  t->Branch("rechit_localy_ME11",rechit_localy_ME11,"rechit_localy_ME11[6]/F");
  t->Branch("rechit_L1eta_ME11", rechit_L1eta_ME11, "rechit_L1eta_ME11[6]/F");
  t->Branch("rechit_L1phi_ME11", rechit_L1phi_ME11, "rechit_L1phi_ME11[6]/F");
  t->Branch("rechit_hitWire_ME11", rechit_hitWire_ME11, "rechit_hitWire_ME11[6]/I");
  t->Branch("rechit_WG_ME11", rechit_WG_ME11, "rechit_WG_ME11[6]/I");
  t->Branch("rechit_nStrips_ME11", rechit_nStrips_ME11, "rechit_nStrips_ME11[6]/i");
  t->Branch("rechit_centralStrip_ME11", rechit_centralStrip_ME11, "rechit_centralStrip_ME11[6]/I");
  t->Branch("rechit_used_ME11", rechit_used_ME11, "rechit_used_ME11[6]/B");
  t->Branch("prop_eta_ME11", prop_eta_ME11, "prop_eta_ME11[6]/F");
  t->Branch("prop_phi_ME11", prop_phi_ME11, "prop_phi_ME11[6]/F");
  t->Branch("prop_x_ME11",   prop_x_ME11,   "prop_x_ME11[6]/F");
  t->Branch("prop_y_ME11",   prop_y_ME11,   "prop_y_ME11[6]/F");
  t->Branch("prop_r_ME11",   prop_r_ME11,   "prop_r_ME11[6]/F");
  t->Branch("propgt_eta_ME11", propgt_eta_ME11, "propgt_eta_ME11[6]/F");
  t->Branch("propgt_phi_ME11", propgt_phi_ME11, "propgt_phi_ME11[6]/F");
  t->Branch("propgt_x_ME11",   propgt_x_ME11,   "propgt_x_ME11[6]/F");
  t->Branch("propgt_y_ME11",   propgt_y_ME11,   "propgt_y_ME11[6]/F");
  t->Branch("propgt_r_ME11",   propgt_r_ME11,   "propgt_r_ME11[6]/F");
  t->Branch("propinner_eta_ME11", propinner_eta_ME11, "propinner_eta_ME11[6]/F");
  t->Branch("propinner_phi_ME11", propinner_phi_ME11, "propinner_phi_ME11[6]/F");
  t->Branch("propinner_x_ME11",   propinner_x_ME11,   "propinner_x_ME11[6]/F");
  t->Branch("propinner_y_ME11",   propinner_y_ME11,   "propinner_y_ME11[6]/F");
  t->Branch("propinner_r_ME11",   propinner_r_ME11,   "propinner_r_ME11[6]/F");
  t->Branch("prop_localx_ME11",prop_localx_ME11,"prop_localx_ME11[6]/F");
  t->Branch("prop_localy_ME11",prop_localy_ME11,"prop_localy_ME11[6]/F");
  t->Branch("rechit_prop_dR_ME11", rechit_prop_dR_ME11, "rechit_prop_dR_ME11[6]/F");
  t->Branch("rechit_prop_dphi_ME11", rechit_prop_dphi_ME11, "rechit_prop_dphi_ME11[6]/F");


  t->Branch("isGood_GE11", isGood_GE11, "isGood_GE11[2]/B");
  t->Branch("has_GE11", has_GE11, "has_GE11[2]/B");
  t->Branch("roll_GE11", roll_GE11, "roll_GE11[2]/I");
  t->Branch("chamber_GE11", chamber_GE11, "chamber_GE11[2]/I");
  t->Branch("rechit_phi_GE11", rechit_phi_GE11, "phi_GE11[2]/F");  // Is this right?
  t->Branch("rechit_alignedphi_GE11", rechit_alignedphi_GE11, "phi_GE11[2]/F");  // Is this right?
  t->Branch("rechit_eta_GE11", rechit_eta_GE11, "rechit_eta_GE11[2]/F");
  t->Branch("rechit_x_GE11", rechit_x_GE11, "rechit_x_GE11[2]/F");
  t->Branch("rechit_y_GE11", rechit_y_GE11, "rechit_y_GE11[2]/F");
  t->Branch("rechit_r_GE11", rechit_r_GE11, "rechit_r_GE11[2]/F");
  t->Branch("rechit_localx_GE11",rechit_localx_GE11,"rechit_localx_GE11[2]/F");
  t->Branch("rechit_alignedlocalx_GE11",rechit_alignedlocalx_GE11,"rechit_alignedlocalx_GE11[2]/F");
  t->Branch("rechit_localy_GE11",rechit_localy_GE11,"rechit_localy_GE11[2]/F");
  t->Branch("rechit_used_GE11", rechit_r_GE11, "rechit_used_GE11[2]/B");
  t->Branch("rechit_BX_GE11", rechit_BX_GE11, "rechit_BX_GE11[2]/I");
  t->Branch("rechit_firstClusterStrip_GE11", rechit_firstClusterStrip_GE11, "rechit_firstClusterStrip_GE11[2]/I");
  t->Branch("rechit_flippedStrip_GE11", rechit_flippedStrip_GE11, "rechit_flippedStrip_GE11[2]/F");
  t->Branch("rechit_clusterSize_GE11", rechit_clusterSize_GE11, "rechit_clusterSize_GE11[2]/I");
  t->Branch("has_propGE11", has_propGE11, "has_propGE11[2]/B");
  t->Branch("roll_propGE11", roll_propGE11, "roll_propGE11[2]/I");
  t->Branch("chamber_propGE11", chamber_propGE11, "chamber_propGE11[2]/I");
  t->Branch("prop_phi_GE11", prop_phi_GE11, "prop_phi_GE11[2]/F");
  t->Branch("prop_eta_GE11", prop_eta_GE11, "prop_eta_GE11[2]/F");
  t->Branch("prop_x_GE11", prop_x_GE11, "prop_x_GE11[2]/F");
  t->Branch("prop_y_GE11", prop_y_GE11, "prop_y_GE11[2]/F");
  t->Branch("prop_r_GE11", prop_r_GE11, "prop_r_GE11[2]/F");
  t->Branch("prop_localx_GE11",prop_localx_GE11,"prop_localx_GE11[2]/F");
  t->Branch("prop_localy_GE11",prop_localy_GE11,"prop_localy_GE11[2]/F");
  t->Branch("propgt_phi_GE11", propgt_phi_GE11, "propgt_phi_GE11[2]/F");
  t->Branch("propgt_eta_GE11", propgt_eta_GE11, "propgt_eta_GE11[2]/F");
  t->Branch("propgt_x_GE11",   propgt_x_GE11,   "propgt_x_GE11[2]/F");
  t->Branch("propgt_y_GE11",   propgt_y_GE11,   "propgt_y_GE11[2]/F");
  t->Branch("propgt_r_GE11",   propgt_r_GE11,   "propgt_r_GE11[2]/F");
  t->Branch("propgt_localx_GE11",propgt_localx_GE11,"propgt_localx_GE11[2]/F");
  t->Branch("propgt_localy_GE11",propgt_localy_GE11,"propgt_localy_GE11[2]/F");
  t->Branch("propinner_phi_GE11", propinner_phi_GE11, "propinner_phi_GE11[2]/F");
  t->Branch("propinner_eta_GE11", propinner_eta_GE11, "propinner_eta_GE11[2]/F");
  t->Branch("propinner_x_GE11",   propinner_x_GE11,   "propinner_x_GE11[2]/F");
  t->Branch("propinner_y_GE11",   propinner_y_GE11,   "propinner_y_GE11[2]/F");
  t->Branch("propinner_r_GE11",   propinner_r_GE11,   "propinner_r_GE11[2]/F");
  t->Branch("propinner_localx_GE11",propinner_localx_GE11,"propinner_localx_GE11[2]/F");
  t->Branch("propinner_localy_GE11",propinner_localy_GE11,"propinner_localy_GE11[2]/F");
  t->Branch("rechit_prop_dR_GE11", rechit_prop_dR_GE11, "rechit_prop_dR_GE11[2]/F");
  t->Branch("rechit_prop_dX_GE11", rechit_prop_dX_GE11, "rechit_prop_dX_GE11[2]/F");
  t->Branch("rechit_prop_aligneddX_GE11", rechit_prop_aligneddX_GE11, "rechit_prop_aligneddX_GE11[2]/F");
  t->Branch("rechit_prop_dphi_GE11", rechit_prop_dphi_GE11, "rechit_prop_dphi_GE11[2]/F");
  t->Branch("rechit_prop_aligneddphi_GE11", rechit_prop_aligneddphi_GE11, "rechit_prop_aligneddphi_GE11[2]/F");

  t->Branch("has_prop_st", has_cscseg_st, "has_prop_st[4]/B");
  t->Branch("prop_phi_st", prop_phi_st, "prop_phi_st[4]/F");
  t->Branch("prop_eta_st", prop_eta_st, "prop_eta_st[4]/F");
  t->Branch("prop_x_st", prop_x_st, "prop_x_st[4]/F");
  t->Branch("prop_y_st", prop_y_st, "prop_y_st[4]/F");
  t->Branch("prop_r_st", prop_r_st, "prop_r_st[4]/F");
  t->Branch("prop_ring_st", prop_ring_st, "prop_ring_st[4]/I");
  t->Branch("prop_chamber_st", prop_chamber_st, "prop_chamber_st[4]/I");

  t->Branch("has_cscseg_st", has_cscseg_st, "has_cscseg_st[4]/B");
  t->Branch("cscseg_phi_st", cscseg_phi_st, "cscseg_phi_st[4]/F");
  t->Branch("cscseg_eta_st", cscseg_eta_st, "cscseg_eta_st[4]/F");
  t->Branch("cscseg_x_st", cscseg_x_st, "cscseg_x_st[4]/F");
  t->Branch("cscseg_y_st", cscseg_y_st, "cscseg_y_st[4]/F");
  t->Branch("cscseg_r_st", cscseg_r_st, "cscseg_r_st[4]/F");
  t->Branch("cscseg_prop_dR_st", cscseg_prop_dR_st, "cscseg_prop_dR_st[4]/F");
  t->Branch("cscseg_prop_dphi_st", cscseg_prop_dphi_st, "cscseg_prop_dphi_st[4]/F");
  t->Branch("cscseg_chamber_st", cscseg_chamber_st, "cscseg_chamber_st[4]/I");
  t->Branch("cscseg_ring_st", cscseg_ring_st, "cscseg_ring_st[4]/I");
  t->Branch("has_csclct_st", has_csclct_st, "has_csclct_st[4]/B");
  t->Branch("csclct_phi_st", csclct_phi_st, "csclct_phi_st[4]/F");
  t->Branch("csclct_eta_st", csclct_eta_st, "csclct_eta_st[4]/F");
  t->Branch("csclct_x_st", csclct_x_st, "csclct_x_st[4]/F");
  t->Branch("csclct_y_st", csclct_y_st, "csclct_y_st[4]/F");
  t->Branch("csclct_r_st", csclct_r_st, "csclct_r_st[4]/F");
  t->Branch("csclct_chamber_st", csclct_chamber_st, "csclct_chamber_st[4]/I");
  t->Branch("csclct_ring_st", csclct_ring_st, "csclct_ring_st[4]/I");
  t->Branch("csclct_prop_dR_st", csclct_prop_dR_st, "csclct_prop_dR_st[4]/F");
  t->Branch("csclct_prop_dphi_st", csclct_prop_dphi_st, "csclct_prop_dphi_st[4]/F");
  t->Branch("csclct_keyStrip_st", csclct_keyStrip_st, "csclct_keyStrip_st[4]/I");
  t->Branch("csclct_keyWG_st", csclct_keyWG_st, "csclct_keyWG_st[4]/I");
  t->Branch("csclct_matchWin_st", csclct_matchWin_st, "csclct_matchWin_st[4]/I");
  t->Branch("csclct_pattern_st", csclct_pattern_st, "csclct_pattern_st[4]/I");



  t->Branch("dphi_CSCL1_GE11L1", dphi_CSCL1_GE11L1, "dphi_CSCL1_GE11L1[2]/F");
  t->Branch("dphi_fitCSCL1_GE11L1", dphi_fitCSCL1_GE11L1, "dphi_fitCSCL1_GE11L1[2]/F");
  t->Branch("dphi_CSCSeg_GE11Rechit", dphi_CSCSeg_GE11Rechit, "dphi_CSCSeg_GE11Rechit[2]/F");
  t->Branch("dphi_keyCSCRechit_GE11Rechit", dphi_keyCSCRechit_GE11Rechit, "dphi_keyCSCRechit_GE11Rechit[2]/F");
  t->Branch("dphi_CSCRechits_GE11Rechit", dphi_CSCRechits_GE11Rechit, "dphi_CSCRechits_GE11Rechit[2]/F");
  t->Branch("dphi_propCSC_propGE11", dphi_propCSC_propGE11, "dphi_propCSC_propGE11[2]/F");
  t->Branch("dphi_keyCSCRechitL1_GE11Rechit", dphi_keyCSCRechitL1_GE11Rechit, "dphi_keyCSCRechitL1_GE11Rechit[2]/F");

  t->Branch("dphi_CSCSeg_alignedGE11Rechit", dphi_CSCSeg_alignedGE11Rechit, "dphi_CSCSeg_alignedGE11Rechit[2]/F");
  t->Branch("dphi_keyCSCRechit_alignedGE11Rechit", dphi_keyCSCRechit_alignedGE11Rechit, "dphi_keyCSCRechit_alignedGE11Rechit[2]/F");
  t->Branch("dphi_keyCSCRechitL1_alignedGE11Rechit", dphi_keyCSCRechitL1_alignedGE11Rechit, "dphi_keyCSCRechitL1_alignedGE11Rechit[2]/F");
 
  t->Branch("prop_strip_GE11",prop_strip_GE11,"prop_strip_GE11[2]/F");
  t->Branch("prop_localx_center_GE11",prop_localx_center_GE11,"prop_localx_center_GE11[2]/F");
  t->Branch("propgt_localx_center_GE11",propgt_localx_center_GE11,"propgt_localx_center_GE11[2]/F");
  t->Branch("propinner_localx_center_GE11",propinner_localx_center_GE11,"propinner_localx_center_GE11[2]/F");
  t->Branch("nrechit_ME11", &nrechit_ME11, "nrechit_ME11/I");
  t->Branch("ncscseg", &ncscseg, "ncscseg/I");
  t->Branch("ncscLct", &ncscLct, "ncscLct/I");
  t->Branch("nrechit_GE11", &nrechit_GE11, "nrechit_GE11/I");



  //  the above is the new edited lines

  return t;
}

class SliceTestAnalysis : public edm::EDAnalyzer {
public:
  explicit SliceTestAnalysis(const edm::ParameterSet&);
  ~SliceTestAnalysis(){};

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void beginJob() ;
  virtual void endJob() ;

  // ----------member data ---------------------------
  edm::EDGetTokenT<GEMRecHitCollection> gemRecHits_;
  edm::EDGetTokenT<CSCRecHit2DCollection> cscRecHits_;
  edm::EDGetTokenT<CSCSegmentCollection> cscSegments_;
  edm::EDGetTokenT<CSCCorrelatedLCTDigiCollection> csclcts_;
  edm::EDGetTokenT<edm::View<reco::Muon> > muons_;
  edm::EDGetTokenT<reco::VertexCollection> vertexCollection_;
//vector<reco::Track>                   "standAloneMuons"           ""                "RECO"       
  //edm::EDGetTokenT<reco::Track> standAloneMuons_;

  edm::Service<TFileService> fs;

  MuonServiceProxy* theService_;
  edm::ESHandle<Propagator> propagator_;
  edm::ESHandle<TransientTrackBuilder> ttrackBuilder_;
  edm::ESHandle<MagneticField> bField_;

  edm::ESHandle<CSCGeometry> CSCGeometry_;
  edm::ESHandle<GEMGeometry> GEMGeometry_;
  //match CSC seg to recoMuon

  //match LCT to recoMuon
  //match CSC seg to recoMuon

  //match LCT to recoMuon
  bool matchRecoMuonwithCSCLCT(const LocalPoint muonlp, edm::Handle<CSCCorrelatedLCTDigiCollection> lcts, CSCDetId cscid, CSCCorrelatedLCTDigi &matchedLCT,LocalPoint &matchedlctlp, float &mindR);
  bool matchRecoMuonwithCSCSeg(const LocalPoint muonlp, edm::Handle<CSCSegmentCollection> cscSegments, CSCDetId cscid, CSCSegment &matchedSeg, float &mindR);

  //get float strip number of one strip centre,like 0.5, 1.5 
  float getCenterStripNumber_float(float strip);

  


  double maxMuonEta_, minMuonEta_;
  bool matchMuonwithLCT_;
  bool matchMuonwithCSCRechit_;

  //find it out later 
  float GEMRechit_muon_deltaR_ = 15.0;//cm
  float GEMRechit_muon_deltaX_ = 10.0;//cm
  float CSCRechit_muon_deltaR_ = 8.0;//cm
  float CSCSegment_muon_deltaR_ = 2.0;//cm
  float CSCLCT_muon_deltaR_ = 4.0;//cm

  //GEM alignment correction
  bool applyGEMalignment_ = false;
  std::vector<double> GEM_alginment_deltaX_;
  bool flippedGEMStrip_ = false;

  TTree * tree_data_;
  MuonData data_;
};

SliceTestAnalysis::SliceTestAnalysis(const edm::ParameterSet& iConfig)
{
  cscRecHits_ = consumes<CSCRecHit2DCollection>(iConfig.getParameter<edm::InputTag>("cscRecHits"));
  csclcts_ = consumes<CSCCorrelatedLCTDigiCollection>(iConfig.getParameter<edm::InputTag>("csclcts"));
  cscSegments_ = consumes<CSCSegmentCollection>(iConfig.getParameter<edm::InputTag>("cscSegments"));
  gemRecHits_ = consumes<GEMRecHitCollection>(iConfig.getParameter<edm::InputTag>("gemRecHits"));
  muons_ = consumes<View<reco::Muon> >(iConfig.getParameter<InputTag>("muons"));
  vertexCollection_ = consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexCollection"));
  //standAloneMuons_ = consumes<reco::Track>(iConfig.getParameter<edm::InputTag>("standAloneMuons"));
  edm::ParameterSet serviceParameters = iConfig.getParameter<edm::ParameterSet>("ServiceParameters");
  minMuonEta_ =  iConfig.getUntrackedParameter<double>("minMuonEta", 1.4);
  maxMuonEta_ =  iConfig.getUntrackedParameter<double>("maxMuonEta", 2.5);
  GEM_alginment_deltaX_ =  iConfig.getParameter<std::vector<double>>("GEM_alginment_deltaX");//cm
  matchMuonwithLCT_ =  iConfig.getUntrackedParameter<bool>("matchMuonwithLCT", false);
  matchMuonwithCSCRechit_ =  iConfig.getUntrackedParameter<bool>("matchMuonwithCSCRechit", false);
  applyGEMalignment_ =  iConfig.getUntrackedParameter<bool>("applyGEMalignment", false);
  flippedGEMStrip_ =  iConfig.getUntrackedParameter<bool>("flippedGEMStrip", false);
  theService_ = new MuonServiceProxy(serviceParameters);

  if (applyGEMalignment_)
      assert(GEM_alginment_deltaX_.size() == 8 );//four GEM chambers, each 2 layrs
  //std::cout<<"error in GEM_alginment_deltaX_, size "<< GEM_alginment_deltaX_.size() << std::endl;
  //edm::ParameterSet matchParameters = iConfig.getParameter<edm::ParameterSet>("MatchParameters");
  //edm::ConsumesCollector iC  = consumesCollector();
  //theMatcher = new MuonSegmentMatcher(matchParameters, iC);

  // instantiate the tree
  tree_data_ = data_.book(tree_data_);
}

void
SliceTestAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  iSetup.get<MuonGeometryRecord>().get(GEMGeometry_);

  iSetup.get<MuonGeometryRecord>().get(CSCGeometry_);

  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",ttrackBuilder_);
  // iSetup.get<TrackingComponentsRecord>().get("SteppingHelixPropagatorAny",propagator_);
  // iSetup.get<IdealMagneticFieldRecord>().get(bField_);
  theService_->update(iSetup);
  auto propagator = theService_->propagator("SteppingHelixPropagatorAny");
  

  edm::Handle<GEMRecHitCollection> gemRecHits;
  iEvent.getByToken(gemRecHits_, gemRecHits);

  //if (gemRecHits->size() == 0) return;
      

  bool hasCSCRechitcollection = false;
  edm::Handle<CSCRecHit2DCollection> cscRecHits;
  if (matchMuonwithCSCRechit_){
      try{
          iEvent.getByToken(cscRecHits_, cscRecHits);
          hasCSCRechitcollection = true;
      }catch (cms::Exception){
        std::cout<< "Error! Can't get CSC Rechit by label. " << std::endl;
        hasCSCRechitcollection = false;
      }
  }
   

  edm::Handle<CSCSegmentCollection> cscSegments;
  iEvent.getByToken(cscSegments_, cscSegments);


  bool hasLCTcollection = false;
  edm::Handle<CSCCorrelatedLCTDigiCollection> cscLcts;
  if (matchMuonwithLCT_){
      try{
        iEvent.getByToken(csclcts_, cscLcts);
        hasLCTcollection = true;
      }catch (cms::Exception){
        std::cout<< "Error! Can't get LCT by label. " << std::endl;
        hasLCTcollection = false;
      }
  }
   
  

  edm::Handle<reco::VertexCollection> vertexCollection;
  iEvent.getByToken( vertexCollection_, vertexCollection );
  if(vertexCollection.isValid()) {
    vertexCollection->size();
   //     std::cout << "vertex->size() " << vertexCollection->size() <<std::endl;
  }


  reco::Vertex goodVertex;// collision vertex
  for (const auto& vertex : *vertexCollection.product()) {
    if (vertex.isValid() && !vertex.isFake() && vertex.tracksSize() >= 2 && fabs(vertex.z()) < 24.) {
      goodVertex = vertex;
      break;
    }
  }

  edm::Handle<View<reco::Muon> > muons;
  iEvent.getByToken(muons_, muons);
 // std::cout << "muons->size() " << muons->size() <<std::endl;
  //cout<<"\nlumi="<<data_.lumi<<"\t run="<<data_.run<<"\t event"<<data_.run << endl; //edited by mohit

  //edm::Handle<reco::Track> standAloneMuons;
  //iEvent.getByToken( standAloneMuons_, standAloneMuons );
  //std::cout <<"standalone muons "<< standAloneMuons->size() << std::endl;
  

  for (size_t i = 0; i < muons->size(); ++i) {
    edm::RefToBase<reco::Muon> muRef = muons->refAt(i);
    const reco::Muon* mu = muRef.get();
    const reco::Track* muonTrack = 0;
    if ( mu->globalTrack().isNonnull() ) muonTrack = mu->globalTrack().get();
    else if ( mu->outerTrack().isNonnull()  ) muonTrack = mu->outerTrack().get();
    else 
	continue;

    if (mu->pt() < 2.0) continue;//ignore low pt muon
    if (mu->isGEMMuon()) {
      std::cout << "isGEMMuon " <<std::endl;
    }

    if (not mu->standAloneMuon()) continue;//not standalone muon
    const reco::Track* standaloneMuon =  mu->standAloneMuon().get();
    const reco::Track* innerTrack = mu->track().get();

    //focus on endcap muons
    //GEMs are installed on minus endcap, namly eta < 0
    //if (muonTrack and mu->numberOfChambersCSCorDT() >= 2 and fabs(mu->eta()) > minMuonEta_ and fabs(mu->eta()) < maxMuonEta_) {
    if (muonTrack and fabs(mu->eta()) > minMuonEta_ and fabs(mu->eta()) < maxMuonEta_) {
	 
      data_.init();
      if (gemRecHits->size() > 0)
	  data_.hasGEMdata  = true;
      
      data_.lumi = iEvent.id().luminosityBlock();
      data_.run = iEvent.id().run();
      data_.event = iEvent.id().event();
      data_.muon_nChamber = mu->numberOfChambersCSCorDT();
     
      if (mu->innerTrack().isNonnull())
	  data_.muon_ntrackhit = mu->innerTrack()->hitPattern().trackerLayersWithMeasurement();
      if (mu->globalTrack().isNonnull())
	  data_.muon_chi2 = mu->globalTrack()->normalizedChi2();
      ///muon position
      data_.muonPx = mu->px();
      data_.muonPy = mu->py();
      data_.muonPz = mu->pz();
      data_.muondxy = fabs(mu->muonBestTrack()->dxy(goodVertex.position()));
      data_.muondz = fabs(mu->muonBestTrack()->dz(goodVertex.position()));
      //cout<<"\nmuondxy="<<data_.muondxy<<"\tmuondx"<<data_.muondz;
      data_.muonpt = mu->pt();
      data_.muoneta = mu->eta();
      data_.muonphi = mu->phi();
      data_.muoncharge = mu->charge();
      data_.muonendcap = mu->eta() > 0 ? 1 : -1 ;


      data_.has_TightID = muon::isTightMuon(*mu, goodVertex);
      data_.has_MediumID = muon::isMediumMuon(*mu);
      data_.has_LooseID = muon::isLooseMuon(*mu);

      data_.muonPFIso = (mu->pfIsolationR04().sumChargedHadronPt + max(0., mu->pfIsolationR04().sumNeutralHadronEt + mu->pfIsolationR04().sumPhotonEt - 0.5*mu->pfIsolationR04().sumPUPt))/mu->pt();
      data_.muonTkIso = mu->isolationR03().sumPt/mu->pt();

      std::cout <<"muon pt "<< mu->pt() <<" eta "<< mu->eta() <<" phi "<< mu->phi() <<" charge "<< mu->charge() << std::endl;

      std::set<float> detLists;
      
      /**** trigger and reco muon match ****/
      /**** end of trigger and reco muon match ****/




      reco::TransientTrack ttTrack_gt = ttrackBuilder_->build(muonTrack);
      reco::TransientTrack ttTrack = ttrackBuilder_->build(standaloneMuon);
      reco::TransientTrack ttTrack_inner = ttrackBuilder_->build(innerTrack);


      /**** propagating track to GEM station and then associating gem reco hit to track ****/
      for (const auto& ch : GEMGeometry_->etaPartitions()) {
	  //only GE1/1 !!!
	 if (ch->id().station() != 1) continue;
        //if ( !detLists.insert( ch->surface().position().z() ).second ) continue;

        TrajectoryStateOnSurface tsos = propagator->propagate(ttTrack.innermostMeasurementState(),ch->surface());
        TrajectoryStateOnSurface tsos_gt = propagator->propagate(ttTrack_gt.outermostMeasurementState(),ch->surface());
        TrajectoryStateOnSurface tsos_inner = propagator->propagate(ttTrack_inner.outermostMeasurementState(),ch->surface());

        if (!tsos.isValid()) continue;
        if (!tsos_gt.isValid()) continue;
        if (!tsos_inner.isValid()) continue;

        GlobalPoint tsosGP = tsos.globalPosition();
        GlobalPoint tsosGP_gt = tsos_gt.globalPosition();
        GlobalPoint tsosGP_inner = tsos_inner.globalPosition();
	if (tsosGP.eta() * mu->eta() < 0.0) continue;

        const LocalPoint pos = ch->toLocal(tsosGP);
        const LocalPoint pos_gt = ch->toLocal(tsosGP_gt);
        const LocalPoint pos_inner = ch->toLocal(tsosGP_inner);
        const LocalPoint pos2D(pos.x(), pos.y(), 0);
        const BoundPlane& bps(ch->surface());
        //cout << "transientTrack using standalone muon tsos gp   "<< tsosGP << ch->id() <<" tttrack.innermost Z position "<< ttTrack.innermostMeasurementState().globalPosition().z() <<" outermost Z position "<< ttTrack.outermostMeasurementState().globalPosition().z() <<endl;
	//cout <<"transientTrack using global track inner "<< ttTrack_gt.innermostMeasurementState().globalPosition().z() <<" outermost Z position "<< ttTrack_gt.outermostMeasurementState().globalPosition().z() <<endl;
        //cout << "transientTrack using innertrack tsos gp   "<< tsosGP_inner << ch->id() <<" tttrack.innermost Z position "<< ttTrack_inner.innermostMeasurementState().globalPosition().z() <<" outermost Z position "<< ttTrack_inner.outermostMeasurementState().globalPosition().z() <<endl;

        if (bps.bounds().inside(pos2D)) {
	  //if (ch->id().station() == 1 and ch->id().ring() == 1 )
	  //    cout << "projection to GEM, in chamber "<< ch->id() << " pos = "<<pos<< " R = "<<pos.mag() <<" inside "
          //     <<  bps.bounds().inside(pos2D) <<endl;
	  if (ch->id().station() == 1 and ch->id().ring() == 1 ){
		cout <<"chamber id " << ch->id() << " propagation using standalone muon  tsos gp   "<< tsosGP <<" using globaltrack "<< tsosGP_gt <<" using innerTrack "<< tsosGP_inner << endl;
	        data_.has_propGE11[ch->id().layer()-1]= true;
		data_.roll_propGE11[ch->id().layer()-1] = ch->id().roll();
		data_.chamber_propGE11[ch->id().layer()-1] = ch->id().chamber();
		data_.prop_phi_GE11[ch->id().layer()-1] = tsosGP.phi();
		data_.prop_eta_GE11[ch->id().layer()-1] = tsosGP.eta();
		data_.prop_x_GE11[ch->id().layer()-1]   = tsosGP.x();
		data_.prop_y_GE11[ch->id().layer()-1]   = tsosGP.y();
		data_.prop_r_GE11[ch->id().layer()-1]   = tsosGP.mag();
		data_.prop_localx_GE11[ch->id().layer()-1] = pos.x();
		data_.prop_localy_GE11[ch->id().layer()-1] = pos.y();
		
		data_.propgt_phi_GE11[ch->id().layer()-1] = tsosGP_gt.phi();
		data_.propgt_eta_GE11[ch->id().layer()-1] = tsosGP_gt.eta();
		data_.propgt_x_GE11[ch->id().layer()-1]   = tsosGP_gt.x();
		data_.propgt_y_GE11[ch->id().layer()-1]   = tsosGP_gt.y();
		data_.propgt_r_GE11[ch->id().layer()-1]   = tsosGP_gt.mag();
		data_.propgt_localx_GE11[ch->id().layer()-1] = pos_gt.x();
		data_.propgt_localy_GE11[ch->id().layer()-1] = pos_gt.y();

		data_.propinner_phi_GE11[ch->id().layer()-1] = tsosGP_inner.phi();
		data_.propinner_eta_GE11[ch->id().layer()-1] = tsosGP_inner.eta();
		data_.propinner_x_GE11[ch->id().layer()-1]   = tsosGP_inner.x();
		data_.propinner_y_GE11[ch->id().layer()-1]   = tsosGP_inner.y();
		data_.propinner_r_GE11[ch->id().layer()-1]   = tsosGP_inner.mag();
		data_.propinner_localx_GE11[ch->id().layer()-1] = pos_inner.x();
		data_.propinner_localy_GE11[ch->id().layer()-1] = pos_inner.y();

                const auto& etaPart = GEMGeometry_->etaPartition(ch->id());
		float strip = etaPart->strip(pos);

		strip = getCenterStripNumber_float(strip);
		LocalPoint lp_center = etaPart->centreOfStrip(strip);
		//std::cout <<"prop muon lp "<< pos <<" center of strip lp "<< lp_center <<" strip "<< strip <<std::endl;
		data_.prop_localx_center_GE11[ch->id().layer()-1] = lp_center.x();
		data_.prop_strip_GE11[ch->id().layer()-1] = strip;

		float strip_gt = etaPart->strip(pos_gt);
		strip_gt =  getCenterStripNumber_float(strip_gt);
		LocalPoint lp_center_gt = etaPart->centreOfStrip(strip_gt);
		data_.propgt_localx_center_GE11[ch->id().layer()-1] = lp_center_gt.x();
		float strip_inner = etaPart->strip(pos_inner);
		strip_inner =  getCenterStripNumber_float(strip_inner);
		LocalPoint lp_center_inner = etaPart->centreOfStrip(strip_inner);
		data_.propinner_localx_center_GE11[ch->id().layer()-1] = lp_center_inner.x();


	  }

	  float mindX = 9999.0;
	  //use all GEM reco hit collection instead, because reco muon algorithm might be inefficiency in using GEM hits
          //for (auto hit = muonTrack->recHitsBegin(); hit != muonTrack->recHitsEnd(); hit++) {
	  for (auto hit = gemRecHits->begin(); hit != gemRecHits->end(); hit++){
            if ( (hit)->geographicalId().det() == DetId::Detector::Muon && (hit)->geographicalId().subdetId() == MuonSubdetId::GEM) {
              GEMDetId gemid((hit)->geographicalId());
              if (gemid.chamber() == ch->id().chamber() and gemid.layer() == ch->id().layer() and abs(gemid.roll() - ch->id().roll()) <= 1) {
                const auto& etaPart = GEMGeometry_->etaPartition(gemid);
		float strip = etaPart->strip(hit->localPosition());
		float strip_flipped = 0.0;
		if (strip < 128.0) strip_flipped = 128.0 - strip;
		else if (strip >=128.0 and strip < 256.0) strip_flipped = 256.0-strip + 128.0;
		else if (strip >= 256.0 and strip < 384.0) strip_flipped = 384.0-strip + 128*2.0;
		else
		    std::cout <<"error strip number from rechit hit : strip "<< strip <<" rechit "<< (*hit) << std::endl;
		LocalPoint lp_flipped = etaPart->centreOfStrip(strip_flipped);
		float deltaR_local = std::sqrt(std::pow((hit)->localPosition().x() -pos.x(), 2) + std::pow((hit)->localPosition().y() -pos.y(), 2));
		float deltaX_local = (hit)->localPosition().x() -pos.x();
		float deltaR_local_flipped = std::sqrt(std::pow(lp_flipped.x()-pos.x(), 2) + std::pow(lp_flipped.y()-pos.y(), 2));
		float deltaX_local_flipped = lp_flipped.x() -pos.x();
		LocalPoint lp_aligned(0.0, 0.0);
		float deltaX_local_aligned  = 0.0;
		if (applyGEMalignment_){
		    unsigned int detid_index = (ch->id().chamber() - 27)*2+ch->id().layer()-1;
		    assert(detid_index < 8);
		    lp_aligned = LocalPoint(lp_flipped.x() + GEM_alginment_deltaX_[detid_index], lp_flipped.y(), lp_flipped.z());
		    deltaX_local_aligned = lp_aligned.x() - pos.x();
		}

                //bool rechit_used = std::find( muonTrack->recHitsBegin(), muonTrack->recHitsEnd(), hit->recHits().begin()) != muonTrack->recHitsEnd();
		bool rechit_used = false;
		/*
		for (auto muonhit = muonTrack->recHitsBegin(); muonhit != muonTrack->recHitsEnd(); muonhit++) {
		    if ( (*muonhit)->rawId() == ch->id().rawId() ) {
			float deltaX_hitmatch = (hit)->localPosition().x() - (*muonhit)->localPosition().x();
			//cout <<"muonhit GEMid "<< GEMDetId((*muonhit)->geographicalId()) <<" lp "<< (*muonhit)->localPosition() <<" deltaX_hitmatch "<< deltaX_hitmatch << endl;
			if (fabs(deltaX_hitmatch) < 0.01) // deltaX should be just 0.0
			    rechit_used = true;
		    }
		}*/


		bool dXcut = (flippedGEMStrip_) ? (fabs(deltaX_local_flipped) < GEMRechit_muon_deltaX_) : (fabs(deltaX_local) < GEMRechit_muon_deltaX_);
		if (dXcut and not data_.has_GE11[gemid.layer()-1])
		    data_.nrechit_GE11 += 1;
		bool mindXcut = (flippedGEMStrip_) ? (fabs(deltaX_local_flipped) < mindX) : (fabs(deltaX_local) < mindX);

		if (ch->id().station() == 1 and ch->id().ring() == 1 and mindXcut){
		    cout << "found hit at GEM detector "<< gemid <<" strip "<< strip <<" flipped strip "<< strip_flipped
			 << " lp " << (hit)->localPosition()
			 << " flipped lp "<< lp_flipped
			 << " gp " << etaPart->toGlobal((hit)->localPosition())
			 << " flipped gp " << etaPart->toGlobal(lp_flipped)
			 << " bx " << hit->BunchX() <<" firstclusterstrip "<< hit->firstClusterStrip() <<" cluster size "<< hit->clusterSize()
			 << " "<< (*hit) <<" "
			 << (rechit_used ? "used by muon track":"not used by muon track")
			 <<" propagated lp "<< pos 
			 <<" propagated gp "<< etaPart->toGlobal(pos)
			 <<" deltaX_local "<< deltaX_local <<" local-dR " << deltaR_local
			 <<" deltaX_local_flipped "<< deltaX_local_flipped << " local-dR flipped "<< deltaR_local_flipped
			 << endl;
		    if (applyGEMalignment_){
			 cout<< "after applying GEM alignment, aligned lp " << lp_aligned
			 << " aligned gp " << etaPart->toGlobal(lp_aligned)
			 <<" deltaX_local_aligned "<< deltaX_local_aligned << endl;
		    }
		    
		    mindX = (flippedGEMStrip_) ? fabs(deltaX_local_flipped) : fabs(deltaX_local);
		    data_.has_GE11[gemid.layer()-1] = 1;
		    data_.roll_GE11[gemid.layer()-1] = ch->id().roll();
		    data_.rechit_firstClusterStrip_GE11[gemid.layer()-1] = hit->firstClusterStrip();
		    data_.rechit_flippedStrip_GE11[gemid.layer()-1] = strip_flipped;
		    data_.rechit_clusterSize_GE11[gemid.layer()-1] = hit->clusterSize();
		    data_.rechit_BX_GE11[gemid.layer()-1] = hit->BunchX();
		    data_.rechit_used_GE11[gemid.layer()-1] = rechit_used;
		    data_.chamber_GE11[gemid.layer()-1] = ch->id().chamber();
		    if (flippedGEMStrip_){
		      data_.rechit_prop_dR_GE11[gemid.layer()-1] = deltaR_local_flipped;
		      data_.rechit_prop_dX_GE11[gemid.layer()-1] = deltaX_local_flipped;
		      data_.rechit_phi_GE11[gemid.layer()-1] = etaPart->toGlobal(lp_flipped).phi();
		      data_.rechit_eta_GE11[gemid.layer()-1] = etaPart->toGlobal(lp_flipped).eta();
		      data_.rechit_x_GE11[gemid.layer()-1] = etaPart->toGlobal(lp_flipped).x();
		      data_.rechit_y_GE11[gemid.layer()-1] = etaPart->toGlobal(lp_flipped).y();
		      data_.rechit_localx_GE11[gemid.layer()-1] = lp_flipped.x();
		      data_.rechit_localy_GE11[gemid.layer()-1] = lp_flipped.y();
		      data_.rechit_r_GE11[gemid.layer()-1] = etaPart->toGlobal(lp_flipped).mag();
		    }else {
		    data_.rechit_prop_dR_GE11[gemid.layer()-1] = deltaR_local;
		    data_.rechit_prop_dX_GE11[gemid.layer()-1] = deltaX_local;
		      data_.rechit_phi_GE11[gemid.layer()-1] = etaPart->toGlobal((hit)->localPosition()).phi();
		      data_.rechit_eta_GE11[gemid.layer()-1] = etaPart->toGlobal((hit)->localPosition()).eta();
		      data_.rechit_x_GE11[gemid.layer()-1] = etaPart->toGlobal((hit)->localPosition()).x();
		      data_.rechit_y_GE11[gemid.layer()-1] = etaPart->toGlobal((hit)->localPosition()).y();
		      data_.rechit_r_GE11[gemid.layer()-1] = etaPart->toGlobal((hit)->localPosition()).mag();
		      data_.rechit_localx_GE11[gemid.layer()-1] = (hit)->localPosition().x();
		      data_.rechit_localy_GE11[gemid.layer()-1] = (hit)->localPosition().y();
		    }
		    data_.rechit_prop_dphi_GE11[gemid.layer()-1] = reco::deltaPhi(tsosGP.phi(), data_.rechit_phi_GE11[gemid.layer()-1]);
		    if (applyGEMalignment_){
			data_.rechit_prop_aligneddX_GE11[gemid.layer()-1] = deltaX_local_aligned;
			data_.rechit_alignedphi_GE11[gemid.layer()-1] = etaPart->toGlobal(lp_aligned).phi();
			data_.rechit_alignedlocalx_GE11[gemid.layer()-1] = lp_aligned.x();
			data_.rechit_prop_aligneddphi_GE11[gemid.layer()-1] = reco::deltaPhi(tsosGP.phi(), data_.rechit_alignedphi_GE11[gemid.layer()-1]);
		    }

		}
              }
            }
          }//end of hit loop
        }
      }
      /**** end of propagating track to GEM station and then associating gem reco hit to track ****/
     //std::cout <<" end of propagating track to GEM station and then associating gem reco hit to track "<< std::endl;

      /**** propagating track to CSC station and then associating csc reco hit to track ****/
      for (const auto& ch : CSCGeometry_->layers()) {

	 //ME1/1 only
	if (not (ch->id().station() == 1 and (ch->id().ring() == 1 or ch->id().ring() == 4)) ) continue;
        //TrajectoryStateOnSurface tsos = propagator->propagate(ttTrack.outermostMeasurementState(),ch->surface());
        TrajectoryStateOnSurface tsos = propagator->propagate(ttTrack.innermostMeasurementState(),ch->surface());
        TrajectoryStateOnSurface tsos_gt = propagator->propagate(ttTrack_gt.outermostMeasurementState(),ch->surface());
        TrajectoryStateOnSurface tsos_inner = propagator->propagate(ttTrack_inner.outermostMeasurementState(),ch->surface());
        if (!tsos.isValid()) continue;
        if (!tsos_gt.isValid()) continue;
        if (!tsos_inner.isValid()) continue;

        GlobalPoint tsosGP = tsos.globalPosition();
        GlobalPoint tsosGP_gt = tsos_gt.globalPosition();
        GlobalPoint tsosGP_inner = tsos_inner.globalPosition();

	if (tsosGP.eta() * mu->eta() < 0.0) continue;
	
        const LocalPoint pos = ch->toLocal(tsosGP);
        const LocalPoint pos2D(pos.x(), pos.y(), 0);
        const BoundPlane& bps(ch->surface());
        //cout << "tsos gp   "<< tsosGP << ch->id() <<endl;
        //cout << "tsos gp   "<< tsosGP << ch->id() <<" tttrack.innermost Z position "<< ttTrack.innermostMeasurementState().globalPosition().z() <<" outermost Z position "<< ttTrack.outermostMeasurementState().globalPosition().z() <<endl;

        if (bps.bounds().inside(pos2D)) {
	  //if (ch->id().station() == 1 and ch->id().ring() == 1 )
	  //    cout << "projection to CSC, in layer "<< ch->id() << " pos = "<<pos<< " R = "<<pos.mag() <<" inside "
          //     <<  bps.bounds().inside(pos2D) <<endl;
	  if (ch->id().station() == 1 and (ch->id().ring() == 1 or ch->id().ring() == 4) ){
	    data_.has_propME11[ch->id().layer()-1] = true;
	    data_.chamber_propME11[ch->id().station() - 1] = ch->id().chamber();
	    data_.ring_propME11[ch->id().station() - 1] = ch->id().ring();
	    data_.prop_phi_ME11[ch->id().layer()-1] = tsosGP.phi();
	    data_.prop_eta_ME11[ch->id().layer()-1] = tsosGP.eta();
	    data_.prop_x_ME11[ch->id().layer()-1] = tsosGP.x();
	    data_.prop_y_ME11[ch->id().layer()-1] = tsosGP.y();
	    data_.prop_r_ME11[ch->id().layer()-1] = tsosGP.mag();
	    data_.propgt_phi_ME11[ch->id().layer()-1] = tsosGP_gt.phi();
	    data_.propgt_eta_ME11[ch->id().layer()-1] = tsosGP_gt.eta();
	    data_.propgt_x_ME11[ch->id().layer()-1]   = tsosGP_gt.x();
	    data_.propgt_y_ME11[ch->id().layer()-1]   = tsosGP_gt.y();
	    data_.propgt_r_ME11[ch->id().layer()-1]   = tsosGP_gt.mag();
	    data_.propinner_phi_ME11[ch->id().layer()-1] = tsosGP_inner.phi();
	    data_.propinner_eta_ME11[ch->id().layer()-1] = tsosGP_inner.eta();
	    data_.propinner_x_ME11[ch->id().layer()-1]   = tsosGP_inner.x();
	    data_.propinner_y_ME11[ch->id().layer()-1]   = tsosGP_inner.y();
	    data_.propinner_r_ME11[ch->id().layer()-1]   = tsosGP_inner.mag();

	    data_.prop_localx_ME11[ch->id().layer()-1] = pos.x();
	    data_.prop_localy_ME11[ch->id().layer()-1] = pos.y();
	    if(ch->id().layer() == 3){
		for (unsigned int i =0; i<2; i++){
		    if (data_.has_propGE11[i]){
			data_.dphi_propCSC_propGE11[i] = reco::deltaPhi(data_.prop_phi_ME11[ch->id().layer()-1], data_.prop_phi_GE11[i]);
			//std::cout <<" ME11-GE11, deltaPhi(propME11, propGE11) GEMlayeri "<<i <<" "<< data_.dphi_propCSC_propGE11[i] <<" ME11 phi "<< data_.prop_phi_ME11[ch->id().layer()-1] <<" GE11 phi "<< data_.prop_phi_GE11[i] <<" CSCid "<< ch->id() <<" GEM chamber "<< data_.chamber_propGE11[i] <<" roll "<< data_.roll_propGE11[i] << std::endl;
		    }
		}
	    }//ME11-GE11, deltaPhi(propME11, propGE11)
	  }
	  

	  if (ch->id().layer() == 3)//keylayer
	  {
	      data_.has_prop_st[ch->id().station() -1] = true;
	      data_.prop_phi_st[ch->id().station() - 1] = tsosGP.phi();
	      data_.prop_eta_st[ch->id().station() - 1] = tsosGP.eta();
	      data_.prop_x_st[ch->id().station() - 1]   = tsosGP.x();
	      data_.prop_y_st[ch->id().station() - 1]   = tsosGP.y();
	      data_.prop_r_st[ch->id().station() - 1]   = tsosGP.mag();
	      data_.prop_chamber_st[ch->id().station() - 1] = ch->id().chamber();
	      data_.prop_ring_st[ch->id().station() - 1] = ch->id().ring();

	      CSCSegment matchedSeg;
	      float mindR = 9999.0;
	      bool hasCSCsegment  = matchRecoMuonwithCSCSeg(pos, cscSegments, ch->id(), matchedSeg, mindR);

	      if (mindR < CSCSegment_muon_deltaR_ and not data_.has_cscseg_st[ch->id().station() -1])
		  data_.ncscseg += 1;
	      if (hasCSCsegment){
		  //std::cout <<"CSC segment is found "<< std::endl;
		  data_.has_cscseg_st[ch->id().station() - 1] = hasCSCsegment;
		  //CSCDetId cscid((*cscseg)->geographicalId());
		  //GlobalPoint seggp = CSCGeometry_->idToDet((*cscseg)->cscDetId())->surface().toGlobal((*cscseg)->localPosition());
		  data_.cscseg_phi_st[ch->id().station() - 1] = ch->toGlobal(matchedSeg.localPosition()).phi();
		  data_.cscseg_eta_st[ch->id().station() - 1] = ch->toGlobal(matchedSeg.localPosition()).eta();
		  data_.cscseg_x_st[ch->id().station() - 1] = ch->toGlobal(matchedSeg.localPosition()).x();
		  data_.cscseg_y_st[ch->id().station() - 1] = ch->toGlobal(matchedSeg.localPosition()).y();
		  data_.cscseg_r_st[ch->id().station() - 1] = ch->toGlobal(matchedSeg.localPosition()).mag();
		  data_.cscseg_prop_dR_st[ch->id().station() - 1] = mindR;
		  data_.cscseg_prop_dphi_st[ch->id().station() - 1] = reco::deltaPhi(tsosGP.phi(), data_.cscseg_phi_st[ch->id().station() - 1]);
		  data_.cscseg_chamber_st[ch->id().station() - 1] = ch->id().chamber();
		  data_.cscseg_ring_st[ch->id().station() - 1] = ch->id().ring();
		  std::cout <<" CSCid " << ch->id() << " found matched CSCsegment, lp "<< matchedSeg.localPosition() <<" gp "<< ch->toGlobal(matchedSeg.localPosition()) <<" "<< matchedSeg << std::endl;
		  if (ch->id().station() == 1 and (ch->id().ring() == 1 or ch->id().ring() == 4)){
		      for(unsigned int i=0; i<2; i++){
			  if (data_.has_GE11[i]){
			      data_.dphi_CSCSeg_GE11Rechit[i] = reco::deltaPhi(data_.cscseg_phi_st[ch->id().station() - 1], data_.rechit_phi_GE11[i]);
			      data_.dphi_CSCSeg_alignedGE11Rechit[i] = reco::deltaPhi(data_.cscseg_phi_st[ch->id().station() - 1], data_.rechit_alignedphi_GE11[i]);
			  }
		      }
		  }//ME11-GE11, dphi(CSCsegment, GEMRechit)
	      }else
		  std::cout <<" no CSC segment is found "<< std::endl;
	  }
	  
	  if (matchMuonwithLCT_ and hasLCTcollection and ch->id().layer() == 3)//keylayer
	  {
	      CSCCorrelatedLCTDigi matchedLCT;
	      LocalPoint lctlp;
	      float mindR = 9999.0;
	      bool hasCSCLct  = matchRecoMuonwithCSCLCT(pos, cscLcts, ch->id(), matchedLCT, lctlp, mindR);
	      if (mindR < CSCLCT_muon_deltaR_ and not data_.has_csclct_st[ch->id().station() -1])
		  data_.ncscLct += 1;
	      if (hasCSCLct){
		  data_.has_csclct_st[ch->id().station() - 1] = hasCSCLct;
		  //CSCDetId cscid((*cscseg)->geographicalId());
		  //GlobalPoint seggp = CSCGeometry_->idToDet((*cscseg)->cscDetId())->surface().toGlobal((*cscseg)->localPosition());
		  data_.csclct_phi_st[ch->id().station() - 1] = ch->toGlobal(lctlp).phi();
		  data_.csclct_eta_st[ch->id().station() - 1] = ch->toGlobal(lctlp).eta();
		  data_.csclct_x_st[ch->id().station() - 1] = ch->toGlobal(lctlp).x();
		  data_.csclct_y_st[ch->id().station() - 1] = ch->toGlobal(lctlp).y();
		  data_.csclct_r_st[ch->id().station() - 1] = ch->toGlobal(lctlp).mag();
		  data_.csclct_prop_dR_st[ch->id().station() - 1] = mindR;
		  data_.csclct_prop_dphi_st[ch->id().station() - 1] = reco::deltaPhi(tsosGP.phi(), data_.csclct_phi_st[ch->id().station() - 1]);
		  data_.csclct_chamber_st[ch->id().station() - 1] = ch->id().chamber();
		  data_.csclct_ring_st[ch->id().station() - 1] = ch->id().ring();
		  data_.csclct_keyStrip_st[ch->id().station() - 1] = matchedLCT.getStrip();
		  data_.csclct_keyWG_st[ch->id().station() - 1] = matchedLCT.getKeyWG();
		  data_.csclct_matchWin_st[ch->id().station() - 1] = matchedLCT.getBX0();
		  data_.csclct_pattern_st[ch->id().station() - 1] = matchedLCT.getPattern();
		  //std::cout <<" CSCid " << ch->id() << " found matched CSC LCT, lp "<< lctlp <<" gp "<< ch->toGlobal(lctlp) << std::endl;
		  //if (ch->id().station() == 1 and (ch->id().ring() == 1 or ch->id().ring() == 4)){
		  //    for(unsigned int i=0; i<2; i++){
		  //        if (data_.has_GE11[i]){
		  //            data_.dphi_CSCseg_GE11Rechit[i] = reco::deltaPhi(data_.cscseg_phi_st[ch->id().station() - 1], data_.rechit_phi_GE11[i]);
		  //        }
		  //    }
		  //}//ME11-GE11, dphi(CSCLCT, GEMPad), L1
	      }
	  }
	  //use all CSC reco hit collection instead, because reco muon algorithm might be inefficiency in using CSC hits
          //for (auto hit = muonTrack->recHitsBegin(); hit != muonTrack->recHitsEnd(); hit++) {
	  float mindR = 9999.0;
          if (matchMuonwithCSCRechit_ and hasCSCRechitcollection) for (auto hit = cscRecHits->begin(); hit != cscRecHits->end(); hit++) {
            if ((hit)->geographicalId().det() == DetId::Detector::Muon && (hit)->geographicalId().subdetId() == MuonSubdetId::CSC) {
              if ((hit)->rawId() == ch->id().rawId() ) {
                CSCDetId cscid((hit)->geographicalId());
                const auto& layer = CSCGeometry_->layer(cscid);
		float deltaR_local = std::sqrt(std::pow((hit)->localPosition().x() -pos.x(), 2) + std::pow((hit)->localPosition().y() -pos.y(), 2));
	        if (deltaR_local < CSCRechit_muon_deltaR_ and not data_.has_ME11[cscid.layer() -1])
		    data_.nrechit_ME11 += 1;

		bool rechit_used = false;
		
		for (auto muonhit = muonTrack->recHitsBegin(); muonhit != muonTrack->recHitsEnd(); muonhit++) {
		    if ( (*muonhit)->rawId() == ch->id().rawId() ) {
			float deltaX_hitmatch = (hit)->localPosition().x() - (*muonhit)->localPosition().x();
			if (fabs(deltaX_hitmatch) < 0.01) // deltaX should be just 0.0
			    rechit_used = true;
			cout <<"muonhit CSCid "<< CSCDetId((*muonhit)->geographicalId()) <<" lp "<< (*muonhit)->localPosition() <<" deltaX_hitmatch "<< deltaX_hitmatch << (rechit_used ? "matched":"notmatched")<< endl;
		    }
		}


		if (ch->id().station() == 1 and (ch->id().ring()==1 or ch->id().ring() ==4) and deltaR_local < mindR){
		    //cout << "found hit ME11 CSC detector "<< cscid
		    //     << " lp " << (hit)->localPosition()
		    //     << " gp " << layer->toGlobal((hit)->localPosition())
		    //     <<" "<< (*hit)
		    //     << endl;
		    mindR = deltaR_local;
		    data_.has_ME11[cscid.layer()-1] = 1;
		    data_.rechit_used_ME11[cscid.layer()-1] = rechit_used;
		    data_.chamber_ME11[cscid.layer()-1] = ch->id().chamber();

		    data_.rechit_hitWire_ME11[cscid.layer()-1] = hit->hitWire();
		    data_.rechit_nStrips_ME11[cscid.layer()-1] = hit->nStrips();
		    int centralStrip = -1;
		    if (hit->nStrips() > 0)
			centralStrip = hit->channels(hit->nStrips()/2);
		    data_.rechit_centralStrip_ME11[cscid.layer()-1] = centralStrip;
		    data_.rechit_halfstrip_ME11[cscid.layer()-1] = (hit->positionWithinStrip()<0.0)? 2*(centralStrip-1):2*(centralStrip-1)+1;
		    //data_.rechit_WG_ME11[cscid.layer()-1] = layer->geometry()->wireGroup(hit->hitWire());
		    //std::cout <<"WG "<< data_.rechit_WG_ME11[cscid.layer()-1] <<" wire "<< hit->hitWire() << std::endl;
		    if (hit->nStrips() > 0 and hit->hitWire() >=0){
			GlobalPoint rechit_L1_gp = layer->toGlobal(layer->geometry()->stripWireGroupIntersection(centralStrip, hit->hitWire()));
			data_.rechit_L1phi_ME11[cscid.layer()-1] = rechit_L1_gp.phi();
			data_.rechit_L1eta_ME11[cscid.layer()-1] = rechit_L1_gp.eta();
		    }//use resolution at L1
		    data_.rechit_prop_dR_ME11[cscid.layer()-1] = mindR;
		    data_.rechit_phi_ME11[cscid.layer()-1] = layer->toGlobal((hit)->localPosition()).phi();
		    data_.rechit_eta_ME11[cscid.layer()-1] = layer->toGlobal((hit)->localPosition()).eta();
		    data_.rechit_x_ME11[cscid.layer()-1] = layer->toGlobal((hit)->localPosition()).x();
		    data_.rechit_y_ME11[cscid.layer()-1] = layer->toGlobal((hit)->localPosition()).y();
		    data_.rechit_localx_ME11[cscid.layer()-1] = (hit)->localPosition().x();
		    data_.rechit_localy_ME11[cscid.layer()-1] = (hit)->localPosition().y();
		    data_.rechit_r_ME11[cscid.layer()-1] = layer->toGlobal((hit)->localPosition()).mag();
		    data_.rechit_prop_dphi_ME11[cscid.layer()-1] = reco::deltaPhi(tsosGP.phi(),  data_.rechit_phi_ME11[cscid.layer()-1]);
		    if (ch->id().station() == 1 and (ch->id().ring() == 1 or ch->id().ring() == 4) and cscid.layer() == 3){//keylayer
		        for(unsigned int i=0; i<2; i++){
		            if (data_.has_GE11[i]){
		                data_.dphi_keyCSCRechit_GE11Rechit[i] = reco::deltaPhi(data_.rechit_phi_ME11[cscid.layer()-1], data_.rechit_phi_GE11[i]);
		                data_.dphi_keyCSCRechit_alignedGE11Rechit[i] = reco::deltaPhi(data_.rechit_phi_ME11[cscid.layer()-1], data_.rechit_alignedphi_GE11[i]);
				if (data_.rechit_L1phi_ME11[cscid.layer()-1] < 4.0){//avoid fake value
				    data_.dphi_keyCSCRechitL1_GE11Rechit[i] = reco::deltaPhi(data_.rechit_L1phi_ME11[cscid.layer()-1], data_.rechit_phi_GE11[i]);
				    data_.dphi_keyCSCRechitL1_alignedGE11Rechit[i] = reco::deltaPhi(data_.rechit_L1phi_ME11[cscid.layer()-1], data_.rechit_alignedphi_GE11[i]);
				}
		            }
		        }
		    }//ME11-GE11, dphi(CSCRechit, GEMRechit)

		}
              }
	    }  
          }//end of csc rechit loop

        }//if (bps.bounds().inside(pos2D)) 
      }


      /**** end of propagating track to CSC station and then associating csc reco hit to track ****/
      ///std::cout <<"end of propagating track to CSC station and then associating csc reco hit to track" << std::endl;


      /**** check gem reco hit used to build muon track and then propagate the track to nearby****/
      /*
      if (muonTrack->hitPattern().numberOfValidMuonGEMHits()) {
        std::cout << "numberOfValidMuonGEMHits->size() " << muonTrack->hitPattern().numberOfValidMuonGEMHits()
                  << " recHitsSize " << muonTrack->recHitsSize()
                  << " pt " << muonTrack->pt()
                  <<std::endl;
        for (auto hit = muonTrack->recHitsBegin(); hit != muonTrack->recHitsEnd(); hit++) {
          if ( (*hit)->geographicalId().det() == DetId::Detector::Muon && (*hit)->geographicalId().subdetId() ==  MuonSubdetId::GEM) {
            //if ((*hit)->rawId() == ch->id().rawId() ) {
            GEMDetId gemid((*hit)->geographicalId());
            const auto& etaPart = GEMGeometry_->etaPartition(gemid);
            TrajectoryStateOnSurface tsos = propagator->propagate(ttTrack.outermostMeasurementState(),etaPart->surface());
            if (!tsos.isValid()) continue;
            GlobalPoint tsosGP = tsos.globalPosition();
            LocalPoint && tsos_localpos = tsos.localPosition();
            LocalError && tsos_localerr = tsos.localError().positionError();
            LocalPoint && dethit_localpos = (*hit)->localPosition();
            LocalError && dethit_localerr = (*hit)->localPositionError();
            auto res_x = (dethit_localpos.x() - tsos_localpos.x());
            auto res_y = (dethit_localpos.y() - tsos_localpos.y());
            auto pull_x = (dethit_localpos.x() - tsos_localpos.x()) /
              std::sqrt(dethit_localerr.xx() + tsos_localerr.xx());
            auto pull_y = (dethit_localpos.y() - tsos_localpos.y()) /
              std::sqrt(dethit_localerr.yy() + tsos_localerr.yy());
            cout << "gem hit "<< gemid<< endl;
            cout << " gp " << etaPart->toGlobal((*hit)->localPosition())<< endl;
            cout << " tsosGP "<< tsosGP << endl;
            cout << " res_x " << res_x
                 << " res_y " << res_y
                 << " pull_x " << pull_x
                 << " pull_y " << pull_y
                 << endl;
          }
        }
      }*/
      /**** end of checking gem reco hit used to build muon track and then propagating the track to nearby****/
     //std::cout << "end of checking gem reco hit used to build muon track and then propagating the track to nearby "<< std::endl;



      /**** check csc reco hit used to build muon track and then propagate the track to nearby****/
     /*
      if (muonTrack->hitPattern().numberOfValidMuonCSCHits()) {
        std::cout << "numberOfValidMuonCSCHits->size() " << muonTrack->hitPattern().numberOfValidMuonCSCHits()
                  << " recHitsSize " << muonTrack->recHitsSize()
                  << " pt " << muonTrack->pt()
                  <<std::endl;
        for (auto hit = muonTrack->recHitsBegin(); hit != muonTrack->recHitsEnd(); hit++) {
          if ( (*hit)->geographicalId().det() == DetId::Detector::Muon && (*hit)->geographicalId().subdetId() == MuonSubdetId::CSC) {
	    std::cout <<" hit detid "<< (*hit)->rawId() << std::endl;
	     
            //if ((*hit)->rawId() == ch->id().rawId() ) {
            CSCDetId cscid((*hit)->geographicalId());
	    std::cout <<"csc rect hit in det id "<< cscid <<" hit "<<  (*hit)->localPosition() << std::endl;
            const auto& layer = CSCGeometry_->layer(cscid);
            TrajectoryStateOnSurface tsos = propagator->propagate(ttTrack.outermostMeasurementState(),layer->surface());
            if (!tsos.isValid()) continue;
            GlobalPoint tsosGP = tsos.globalPosition();
            LocalPoint && tsos_localpos = tsos.localPosition();
            LocalError && tsos_localerr = tsos.localError().positionError();
            LocalPoint && dethit_localpos = (*hit)->localPosition();
            LocalError && dethit_localerr = (*hit)->localPositionError();
            auto res_x = (dethit_localpos.x() - tsos_localpos.x());
            auto res_y = (dethit_localpos.y() - tsos_localpos.y());
            auto pull_x = (dethit_localpos.x() - tsos_localpos.x()) /
              std::sqrt(dethit_localerr.xx() + tsos_localerr.xx());
            auto pull_y = (dethit_localpos.y() - tsos_localpos.y()) /
              std::sqrt(dethit_localerr.yy() + tsos_localerr.yy());
            cout << "csc hit "<< cscid<< endl;
            cout << " gp " << layer->toGlobal((*hit)->localPosition())<< endl;
            cout << " tsosGP "<< tsosGP << endl;
            cout << " res_x " << res_x
                 << " res_y " << res_y
                 << " pull_x " << pull_x
                 << " pull_y " << pull_y
                 << endl;
          }
        }
      }*/
      /**** end of checking csc reco hit used to build muon track and then propagating the track to nearby****/
      //std::cout  <<" end of checking csc reco hit used to build muon track and then propagating the track to nearby "<< std::endl;
      

       tree_data_->Fill();
    } //end of valid muontrack
    // fill the tree for each muon
  }// end of loop over reco muons
}



//////////////  Get the matching with CSC-sgements...
bool SliceTestAnalysis::matchRecoMuonwithCSCSeg(const LocalPoint muonlp, edm::Handle<CSCSegmentCollection> cscSegments, CSCDetId idCSC, CSCSegment &matchedSeg, float &mindR){

  float deltaCSCR = 9999.;
  bool matched = false;
  for(CSCSegmentCollection::const_iterator segIt=cscSegments->begin(); segIt != cscSegments->end(); segIt++) {
    CSCDetId id  = (CSCDetId)(*segIt).cscDetId();
    if(idCSC.endcap() != id.endcap())continue;
    if(idCSC.station() != id.station())continue;
    if(idCSC.chamber() != id.chamber())continue;
      
    Bool_t ed1 = (idCSC.station() == 1) && ((idCSC.ring() == 1 || idCSC.ring() == 4) && (id.ring() == 1 || id.ring() == 4));
    Bool_t ed2 = (idCSC.station() == 1) && ((idCSC.ring() == 2 && id.ring() == 2) || (idCSC.ring() == 3 && id.ring() == 3));
    Bool_t ed3 = (idCSC.station() != 1) && (idCSC.ring() == id.ring());
    Bool_t TMCSCMatch = (ed1 || ed2 || ed3);
    if(! TMCSCMatch)continue;
    
    //TrajectoryStateOnSurface TrajSuf_ = surfExtrapTrkSam(trackRef, cscchamber->toGlobal( (*segIt).localPosition() ).z());


    float deltaR_local = std::sqrt(std::pow((*segIt).localPosition().x() - muonlp.x(), 2) + std::pow((*segIt).localPosition().y() -muonlp.y(), 2));
    std::cout << " Seg mathced to TT: "<<id.endcap()<<" "<<id.station()<<" "<< id.chamber() << " and targeted idCSC "<< idCSC <<" deltaR_local "<< deltaR_local <<std::endl;

    if ( deltaR_local < deltaCSCR  ){
      matched = true;
      deltaCSCR = deltaR_local;
      mindR = deltaR_local;
      matchedSeg = *segIt;
    }
  }//loop over segments
  return matched;

}



//////////////  Get the matching with CSC LCT...
bool SliceTestAnalysis::matchRecoMuonwithCSCLCT(const LocalPoint muonlp, edm::Handle<CSCCorrelatedLCTDigiCollection> cscLcts, CSCDetId idCSC, CSCCorrelatedLCTDigi &matchedLCT, LocalPoint &matchedlctlp, float &mindR){

  float deltaCSCR = 9999.;
  bool matched = false;
  for (CSCCorrelatedLCTDigiCollection::DigiRangeIterator detUnitIt = cscLcts->begin(); 
       detUnitIt != cscLcts->end(); detUnitIt++) {

    CSCDetId id = (*detUnitIt).first;
 
    
    if(idCSC.endcap() != id.endcap())continue;
    if(idCSC.station() != id.station())continue;
    if(idCSC.chamber() != id.chamber())continue;
      
    Bool_t ed1 = (idCSC.station() == 1) && ((idCSC.ring() == 1 || idCSC.ring() == 4) && (id.ring() == 1 || id.ring() == 4));
    Bool_t ed2 = (idCSC.station() == 1) && ((idCSC.ring() == 2 && id.ring() == 2) || (idCSC.ring() == 3 && id.ring() == 3));
    Bool_t ed3 = (idCSC.station() != 1) && (idCSC.ring() == id.ring());
    Bool_t TMCSCMatch = (ed1 || ed2 || ed3);
    if(! TMCSCMatch)continue;
    
    const CSCCorrelatedLCTDigiCollection::Range& Lctrange = (*detUnitIt).second;
    for (CSCCorrelatedLCTDigiCollection::const_iterator lctIt = Lctrange.first; lctIt != Lctrange.second; lctIt++) {
      bool lct_valid = (*lctIt).isValid();
      if(!lct_valid)continue;

      int wireGroup_id = (*lctIt).getKeyWG()+1;
      int strip_id=(*lctIt).getStrip()/2+1;
      bool me11=(id.station() == 1) && (id.ring() == 1 || id.ring() == 4); 
      bool  me11a = me11 && strip_id>64;
      if ( me11a ) {
        strip_id-=64;
        id=CSCDetId(idCSC.endcap(), 1, 4, idCSC.chamber(), 3); //id for key layer
      }
      const CSCLayerGeometry *layerGeom = CSCGeometry_->chamber(id)->layer (3)->geometry ();
      LocalPoint lctlp = layerGeom->stripWireGroupIntersection(strip_id, wireGroup_id);


      float deltaR_local = std::sqrt(std::pow(lctlp.x() - muonlp.x(), 2) + std::pow(lctlp.y() -muonlp.y(), 2));
      //std::cout << " LCT mathced to TT: "<<id.endcap()<<" "<<id.station()<<" "<< id.chamber() << " and targeted idCSC "<< idCSC <<" deltaR_local "<< deltaR_local <<std::endl;
     
     
      if ( deltaR_local < deltaCSCR  ){
        matched = true;
        deltaCSCR = deltaR_local;
        mindR = deltaR_local;
        matchedlctlp = lctlp;
        matchedLCT = *lctIt;

 
      }
    }
  }//loop over LCTs
  return matched;

}

float SliceTestAnalysis::getCenterStripNumber_float(float strip){

    int strip_int= int(strip);
    if ((strip-strip_int)>0.25 and (strip-strip_int)<=0.75) strip = strip_int + 0.5;
    else if ((strip-strip_int)>0.75) strip = strip_int +1.0;
    else if ((strip-strip_int) <= 0.25) strip = strip_int*1.0;
    else 
	std::cout <<"localpoint, strip "<< strip << "strip_int "<< strip_int <<" warning !! "<< std::endl; 
    return strip;

}

void SliceTestAnalysis::beginJob(){}
void SliceTestAnalysis::endJob(){}

//define this as a plug-in
DEFINE_FWK_MODULE(SliceTestAnalysis);
