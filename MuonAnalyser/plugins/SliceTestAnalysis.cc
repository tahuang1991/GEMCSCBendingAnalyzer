// system include files
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

#include "DataFormats/CSCRecHit/interface/CSCRecHit2D.h"
#include <DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h>
#include "Geometry/CSCGeometry/interface/CSCGeometry.h"

#include "DataFormats/GEMRecHit/interface/GEMRecHitCollection.h"
#include "Geometry/GEMGeometry/interface/GEMGeometry.h"
#include "Geometry/GEMGeometry/interface/GEMEtaPartitionSpecs.h"

#include "Geometry/Records/interface/MuonGeometryRecord.h"
#include "Geometry/CommonTopologies/interface/StripTopology.h"

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

  double muonPx, muonPy, muonPz;
  double muondxy, muondz;
  int muon_ntrackhit, muon_nChameber, muon_chi2;
  double muonpt, muoneta, muonphi;
  bool muoncharge;
  bool muonendcap;
  double muonPFIso, muonTkIso;
  int muon_nChamber;
  

  bool has_TightID;
  bool has_MediumID;
  bool has_LooseID;
  
  bool has_ME11[6];
  bool has_GE11[2];

  //Muon position at ME11
  double rechit_phi_ME11[6];//phi at each layer, from CSC rechit
  double rechit_eta_ME11[6];
  double rechit_x_ME11[6];
  double rechit_y_ME11[6];
  double rechit_r_ME11[6];
  double prop_phi_ME11[6];//projected position in ME11
  double prop_eta_ME11[6];//projected position in ME11
  double prop_x_ME11[6];//projected position in ME11
  double prop_y_ME11[6];
  double prop_r_ME11[6];
  double rechit_prop_dR_ME11[6];
  int chamber_ME11[6];

  //CSC segment matched to recoMuon
  bool has_cscseg_st[4];
  double cscseg_phi_st[4];
  double cscseg_eta_st[4];
  double cscseg_x_st[4];
  double cscseg_y_st[4];
  double cscseg_z_st[4];
  int cscseg_chamber_st[4];
  int cscseg_ring_st[4];
  //match LCT to recoMuon by projection
  bool has_csclct_st[4];
  double csclct_phi_st[4];
  double csclct_eta_st[4];
  double csclct_x_st[4];
  double csclct_y_st[4];
  double csclct_r_st[4];
  int    csclct_chamber_st[4];
  int    csclct_ring_st[4];

  //Muon position at GE11

  //Muon position at GE11
  bool isGood_GE11[2];
  int roll_GE11[2];
  int chamber_GE11[2];
  double rechit_phi_GE11[2];//phi,eta from GE11 rechits
  double rechit_eta_GE11[2];
  double rechit_x_GE11[2];//rechit position in GE11
  double rechit_y_GE11[2];
  double rechit_r_GE11[2];
  double prop_phi_GE11[2];//phi,eta from GE11 rechits
  double prop_eta_GE11[2];
  double prop_x_GE11[2];//projected position in GE11
  double prop_y_GE11[2];
  double prop_r_GE11[2];
  double rechit_prop_dR_GE11[2];
  
  double dphi_CSC_GE11[2];//average CSC phi - GEM phi for each GEM layer
  double dphi_keyCSC_GE11[2];// CSC phi in key layer - GEM phi for each GEM layer
  double dphi_fitCSC_GE11[2];// CSC phi from fit - GEM phi for each GEM layer
  
  
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

  for (int i=0; i<2; ++i){
    has_GE11[i] = 0;
    rechit_phi_GE11[i] = -9;
    rechit_eta_GE11[i] = -9;
    rechit_x_GE11[i] = 0.0;
    rechit_y_GE11[i] = 0.0;
    rechit_r_GE11[i] = 0.0;
    isGood_GE11[i] = 0;
  }
  for (int i=0; i<6; ++i){
    has_ME11[i] = 0;
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
  t->Branch("has_TightID", &has_TightID);

  t->Branch("isGood_GE11", isGood_GE11, "isGood_GE11[2]/I");
  t->Branch("has_GE11", has_GE11, "has_GE11[2]/I");
  t->Branch("has_ME11", has_ME11, "has_ME11[6]/I");
  t->Branch("rechit_phi_GE11", rechit_phi_GE11, "phi_GE11[2]/F");  // Is this right?
  t->Branch("prop_phi_GE11", prop_phi_GE11, "prop_phi_GE11[2]/F");
  t->Branch("rechit_phi_ME11", rechit_phi_ME11, "rechit_phi_ME11[6]/F");
  t->Branch("prop_phi_ME11", prop_phi_ME11, "prop_phi_ME11[6]/F");

  //edited my mohit khurana need verfication
  t->Branch("muonPx", &muonPx);
  t->Branch("muonPy", &muonPy);
  t->Branch("muonPz", &muonPz);
  t->Branch("muondxy", &muondxy);
  t->Branch("muondz", &muondz);
  t->Branch("muon_ntrackhit", &muon_ntrackhit);
  t->Branch("muon_nChameber", &muon_nChameber);  
  t->Branch("muon_chi2", &muon_chi2);
  t->Branch("muonPFIso", &muonPFIso);
  t->Branch("muonTkIso", &muonTkIso);
  t->Branch("muon_nChamber", &muon_nChamber);
  t->Branch("has_MediumID", &has_MediumID);
  t->Branch("has_LooseID", &has_LooseID);  
  t->Branch("rechit_eta_ME11", rechit_eta_ME11, "rechit_eta_ME11[6]/F");
  t->Branch("rechit_x_ME11", rechit_x_ME11, "rechit_x_ME11[6]/F");
  t->Branch("rechit_y_ME11", rechit_y_ME11, "rechit_y_ME11[6]/F");
  t->Branch("rechit_r_ME11", rechit_r_ME11, "rechit_r_ME11[6]/F");
  t->Branch("prop_eta_ME11", prop_eta_ME11, "prop_eta_ME11[6]/F");
  t->Branch("prop_x_ME11", prop_x_ME11, "prop_x_ME11[6]/F");
  t->Branch("prop_y_ME11", prop_y_ME11, "prop_y_ME11[6]/F");
  t->Branch("prop_r_ME11", prop_r_ME11, "prop_r_ME11[6]/F");
  t->Branch("rechit_prop_dR_ME11", rechit_prop_dR_ME11, "rechit_prop_dR_ME11[6]/F");
  t->Branch("chamber_ME11", chamber_ME11, "chamber_ME11[6]/I");
  t->Branch("roll_GE11", roll_GE11, "roll_GE11[2]/I");
  t->Branch("chamber_GE11", chamber_GE11, "chamber_GE11[2]/I");
  //  t->Branch("rechit_phi_GE11", rechit_phi_GE11, "rechit_phi_GE11[2]/F");   // in doubt please check!!!
  t->Branch("rechit_eta_GE11", rechit_eta_GE11, "rechit_eta_GE11[2]/F");
  t->Branch("rechit_x_GE11", rechit_x_GE11, "rechit_x_GE11[2]/F");
  t->Branch("rechit_y_GE11", rechit_y_GE11, "rechit_y_GE11[2]/F");
  t->Branch("rechit_r_GE11", rechit_r_GE11, "rechit_r_GE11[2]/F");
  t->Branch("prop_eta_GE11", prop_eta_GE11, "prop_eta_GE11[2]/F");
  t->Branch("prop_x_GE11", prop_x_GE11, "prop_x_GE11[2]/F");
  t->Branch("prop_y_GE11", prop_y_GE11, "prop_y_GE11[2]/F");
  t->Branch("prop_r_GE11", prop_r_GE11, "prop_r_GE11[2]/F");
  t->Branch("rechit_prop_dR_GE11", rechit_prop_dR_GE11, "rechit_prop_dR_GE11[2]/F");
  t->Branch("dphi_CSC_GE11", dphi_CSC_GE11, "dphi_CSC_GE11[2]/F");
  t->Branch("dphi_keyCSC_GE11", dphi_keyCSC_GE11, "dphi_keyCSC_GE11[2]/F");
  t->Branch("dphi_fitCSC_GE11", dphi_fitCSC_GE11, "dphi_fitCSC_GE11[2]/F");

  //  the aboe is the new edited lines

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
  edm::EDGetTokenT<CSCCorrelatedLCTDigiCollection> csclcts_;
  edm::EDGetTokenT<edm::View<reco::Muon> > muons_;
  edm::EDGetTokenT<reco::VertexCollection> vertexCollection_;
  edm::Service<TFileService> fs;

  MuonServiceProxy* theService_;
  edm::ESHandle<Propagator> propagator_;
  edm::ESHandle<TransientTrackBuilder> ttrackBuilder_;
  edm::ESHandle<MagneticField> bField_;

  //match CSC seg to recoMuon

  //match LCT to recoMuon
  bool matchRecoMuonwithLCT(const LocalPoint muonlp, const CSCCorrelatedLCTDigiCollection& lcts, CSCDetId cscid, CSCCorrelatedLCTDigi &matchedLCT);

  


  float maxMuonEta_, minMuonEta_;

  //find it out later 
  float GEMResolution = 10.0;//in term of local R from local x,y
  float CSCResolution = 10.0;// 

  TTree * tree_data_;
  MuonData data_;
};

SliceTestAnalysis::SliceTestAnalysis(const edm::ParameterSet& iConfig)
{
  cscRecHits_ = consumes<CSCRecHit2DCollection>(iConfig.getParameter<edm::InputTag>("cscRecHits"));
  csclcts_ = consumes<CSCCorrelatedLCTDigiCollection>(iConfig.getParameter<edm::InputTag>("csclcts"));
  gemRecHits_ = consumes<GEMRecHitCollection>(iConfig.getParameter<edm::InputTag>("gemRecHits"));
  muons_ = consumes<View<reco::Muon> >(iConfig.getParameter<InputTag>("muons"));
  vertexCollection_ = consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexCollection"));
  edm::ParameterSet serviceParameters = iConfig.getParameter<edm::ParameterSet>("ServiceParameters");
  minMuonEta_ =  iConfig.getUntrackedParameter<double>("minMuonEta", 1.4);
  maxMuonEta_ =  iConfig.getUntrackedParameter<double>("maxMuonEta", 2.5);
  theService_ = new MuonServiceProxy(serviceParameters);
  //edm::ParameterSet matchParameters = iConfig.getParameter<edm::ParameterSet>("MatchParameters");
  //edm::ConsumesCollector iC  = consumesCollector();
  //theMatcher = new MuonSegmentMatcher(matchParameters, iC);

  // instantiate the tree
  tree_data_ = data_.book(tree_data_);
}

void
SliceTestAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::ESHandle<GEMGeometry> hGeom;
  iSetup.get<MuonGeometryRecord>().get(hGeom);
  const GEMGeometry* GEMGeometry_ = &*hGeom;

  edm::ESHandle<CSCGeometry> hGeomCSC;
  iSetup.get<MuonGeometryRecord>().get(hGeomCSC);
  const CSCGeometry* CSCGeometry_ = &*hGeomCSC;

  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",ttrackBuilder_);
  // iSetup.get<TrackingComponentsRecord>().get("SteppingHelixPropagatorAny",propagator_);
  // iSetup.get<IdealMagneticFieldRecord>().get(bField_);
  theService_->update(iSetup);
  auto propagator = theService_->propagator("SteppingHelixPropagatorAny");
  

  edm::Handle<GEMRecHitCollection> gemRecHits;
  iEvent.getByToken(gemRecHits_, gemRecHits);

  edm::Handle<CSCRecHit2DCollection> cscRecHits;
  iEvent.getByToken(cscRecHits_, cscRecHits);

  edm::Handle<CSCCorrelatedLCTDigiCollection> cscLcts;
  iEvent.getByToken(csclcts_, cscLcts);
  

  edm::Handle<reco::VertexCollection> vertexCollection;
  iEvent.getByToken( vertexCollection_, vertexCollection );
  if(vertexCollection.isValid()) {
    vertexCollection->size();
    //    std::cout << "vertex->size() " << vertexCollection->size() <<std::endl;
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
  //std::cout << "muons->size() " << muons->size() <<std::endl;
  //
  //

  for (size_t i = 0; i < muons->size(); ++i) {
    edm::RefToBase<reco::Muon> muRef = muons->refAt(i);
    const reco::Muon* mu = muRef.get();
    const reco::Track* muonTrack = 0;
    if ( mu->globalTrack().isNonnull() ) muonTrack = mu->globalTrack().get();
    else if ( mu->outerTrack().isNonnull()  ) muonTrack = mu->outerTrack().get();
    else 
	continue;

    if (mu->pt() < 0.0) continue;
    if (mu->isGEMMuon()) {
      std::cout << "isGEMMuon " <<std::endl;
    }

    if (not mu->standAloneMuon()) continue;//not standalone muon

    //focus on endcap muons
    if (muonTrack and mu->numberOfChambersCSCorDT() >= 2 and fabs(mu->eta()) > minMuonEta_ and fabs(mu->eta()) < maxMuonEta_) {
	 
      data_.init();

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

      std::set<double> detLists;
      
      /**** trigger and reco muon match ****/
      /**** end of trigger and reco muon match ****/



      /*vector<const CSCSegment*> range = theMatcher->matchCSC(mu->standAloneMuon(),iEvent);
      for (vector<const CSCSegment*>::iterator cscseg = range.begin(); cscseg != range.end(); ++cscseg) 
      {
          // Create the ChamberId
          CSCDetId cscid((*cscseg)->geographicalId());
	   
	  GlobalPoint seggp = CSCGeometry_->idToDet((*cscseg)->cscDetId())->surface().toGlobal((*cscseg)->localPosition());
	  data_.has_cscseg_st[cscid.station() - 1] = true;
	  data_.cscseg_phi_st[cscid.station() - 1] = seggp.phi();
	  data_.cscseg_eta_st[cscid.station() - 1] = seggp.eta();
	  data_.cscseg_x_st[cscid.station() - 1] = (*cscseg)->localPosition().x();
	  data_.cscseg_y_st[cscid.station() - 1] = (*cscseg)->localPosition().y();
	  data_.cscseg_z_st[cscid.station() - 1] = (*cscseg)->localPosition().mag();
	  data_.cscseg_chamber_st[cscid.station() - 1] = cscid.chamber();
	  data_.cscseg_ring_st[cscid.station() - 1] = cscid.ring();
      }*/





      reco::TransientTrack ttTrack = ttrackBuilder_->build(muonTrack);


      /**** propagating track to GEM station and then associating gem reco hit to track ****/
      for (const auto& ch : GEMGeometry_->etaPartitions()) {
        //if ( !detLists.insert( ch->surface().position().z() ).second ) continue;

        TrajectoryStateOnSurface tsos = propagator->propagate(ttTrack.outermostMeasurementState(),ch->surface());
        if (!tsos.isValid()) continue;

        GlobalPoint tsosGP = tsos.globalPosition();
        const LocalPoint pos = ch->toLocal(tsosGP);
        const LocalPoint pos2D(pos.x(), pos.y(), 0);
        const BoundPlane& bps(ch->surface());
        //cout << "tsos gp   "<< tsosGP << ch->id() <<endl;

        if (bps.bounds().inside(pos2D)) {
	  //if (ch->id().station() == 1 and ch->id().ring() == 1 )
	  //    cout << "projection to GEM, in chamber "<< ch->id() << " pos = "<<pos<< " R = "<<pos.mag() <<" inside "
          //     <<  bps.bounds().inside(pos2D) <<endl;

	  float mindR = 9999.0;
	  //use all GEM reco hit collection instead, because reco muon algorithm might be inefficiency in using GEM hits
          //for (auto hit = muonTrack->recHitsBegin(); hit != muonTrack->recHitsEnd(); hit++) {
	  for (auto hit = gemRecHits->begin(); hit != gemRecHits->end(); hit++){
            if ( (hit)->geographicalId().det() == DetId::Detector::Muon && (hit)->geographicalId().subdetId() == MuonSubdetId::GEM) {
              if ((hit)->rawId() == ch->id().rawId() ) {
                GEMDetId gemid((hit)->geographicalId());
                const auto& etaPart = GEMGeometry_->etaPartition(gemid);
		float deltaR_local = std::sqrt(std::pow((hit)->localPosition().x() -pos.x(), 2) + std::pow((hit)->localPosition().y() -pos.y(), 2));

		if (ch->id().station() == 1 and ch->id().ring() == 1 and deltaR_local < mindR){
		    cout << "found hit at GEM detector "<< gemid
			 << " lp " << (hit)->localPosition()
			 << " gp " << etaPart->toGlobal((hit)->localPosition())
			 << endl;
		    mindR = deltaR_local;
		    data_.has_GE11[gemid.layer()-1] = 1;
		    data_.roll_GE11[gemid.layer()-1] = ch->id().roll();
		    data_.chamber_GE11[gemid.layer()-1] = ch->id().chamber();
		    data_.rechit_prop_dR_GE11[gemid.layer()-1] = mindR;
		    data_.rechit_phi_GE11[gemid.layer()-1] = etaPart->toGlobal((hit)->localPosition()).phi();
		    data_.rechit_eta_GE11[gemid.layer()-1] = etaPart->toGlobal((hit)->localPosition()).eta();
		    data_.rechit_x_GE11[gemid.layer()-1] = (hit)->localPosition().x();
		    data_.rechit_y_GE11[gemid.layer()-1] = (hit)->localPosition().y();
		    data_.rechit_r_GE11[gemid.layer()-1] = (hit)->localPosition().mag();
		    data_.prop_phi_GE11[gemid.layer()-1] = tsosGP.phi();
		    data_.prop_eta_GE11[gemid.layer()-1] = tsosGP.eta();
		    data_.prop_x_GE11[gemid.layer()-1] = pos.x();
		    data_.prop_y_GE11[gemid.layer()-1] = pos.y();
		    data_.prop_r_GE11[gemid.layer()-1] = pos.mag();

		}
              }
            }
          }//end of hit loop
        }
      }
      /**** end of propagating track to GEM station and then associating gem reco hit to track ****/
     std::cout <<" end of propagating track to GEM station and then associating gem reco hit to track "<< std::endl;

      /**** propagating track to CSC station and then associating csc reco hit to track ****/
      for (const auto& ch : CSCGeometry_->layers()) {

        TrajectoryStateOnSurface tsos = propagator->propagate(ttTrack.outermostMeasurementState(),ch->surface());
        if (!tsos.isValid()) continue;

        GlobalPoint tsosGP = tsos.globalPosition();
	
        const LocalPoint pos = ch->toLocal(tsosGP);
        const LocalPoint pos2D(pos.x(), pos.y(), 0);
        const BoundPlane& bps(ch->surface());
        //cout << "tsos gp   "<< tsosGP << ch->id() <<endl;

        if (bps.bounds().inside(pos2D)) {
	  //if (ch->id().station() == 1 and ch->id().ring() == 1 )
	  //    cout << "projection to CSC, in layer "<< ch->id() << " pos = "<<pos<< " R = "<<pos.mag() <<" inside "
          //     <<  bps.bounds().inside(pos2D) <<endl;

	  float mindR = 9999.0;
	  
	  //use all CSC reco hit collection instead, because reco muon algorithm might be inefficiency in using CSC hits
          //for (auto hit = muonTrack->recHitsBegin(); hit != muonTrack->recHitsEnd(); hit++) {
          for (auto hit = cscRecHits->begin(); hit != cscRecHits->end(); hit++) {
            if ((hit)->geographicalId().det() == DetId::Detector::Muon && (hit)->geographicalId().subdetId() == MuonSubdetId::CSC) {
              if ((hit)->rawId() == ch->id().rawId() ) {
                CSCDetId cscid((hit)->geographicalId());
                const auto& layer = CSCGeometry_->layer(cscid);
		float deltaR_local = std::sqrt(std::pow((hit)->localPosition().x() -pos.x(), 2) + std::pow((hit)->localPosition().y() -pos.y(), 2));

		if (ch->id().station() == 1 and (ch->id().ring()==1 or ch->id().ring() ==4) and deltaR_local < mindR){
		    cout << "found hit ME11 CSC detector "<< cscid
			 << " lp " << (hit)->localPosition()
			 << " gp " << layer->toGlobal((hit)->localPosition())
			 << endl;
		    mindR = deltaR_local;
		    data_.has_ME11[cscid.layer()-1] = 1;
		    data_.chamber_ME11[cscid.layer()-1] = ch->id().chamber();
		    data_.rechit_prop_dR_ME11[cscid.layer()-1] = mindR;
		    data_.rechit_phi_ME11[cscid.layer()-1] = layer->toGlobal((hit)->localPosition()).phi();
		    data_.rechit_eta_ME11[cscid.layer()-1] = layer->toGlobal((hit)->localPosition()).eta();
		    data_.rechit_x_ME11[cscid.layer()-1] = (hit)->localPosition().x();
		    data_.rechit_y_ME11[cscid.layer()-1] = (hit)->localPosition().y();
		    data_.rechit_r_ME11[cscid.layer()-1] = (hit)->localPosition().mag();
		    data_.prop_phi_ME11[cscid.layer()-1] = tsosGP.phi();
		    data_.prop_eta_ME11[cscid.layer()-1] = tsosGP.eta();
		    data_.prop_x_ME11[cscid.layer()-1] = pos.x();
		    data_.prop_y_ME11[cscid.layer()-1] = pos.y();
		    data_.prop_r_ME11[cscid.layer()-1] = pos.mag();

		}
              }
            }
	    
          }//end of csc rechit loop
        }
      }

      /**** end of propagating track to CSC station and then associating csc reco hit to track ****/
      std::cout <<"end of propagating track to CSC station and then associating csc reco hit to track" << std::endl;


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

void SliceTestAnalysis::beginJob(){}
void SliceTestAnalysis::endJob(){}

//define this as a plug-in
DEFINE_FWK_MODULE(SliceTestAnalysis);
