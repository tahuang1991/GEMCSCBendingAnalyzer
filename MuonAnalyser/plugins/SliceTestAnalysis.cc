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

#include "RecoMuon/TrackingTools/interface/MuonServiceProxy.h"
#include "TrackingTools/GeomPropagators/interface/Propagator.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackPropagation/SteppingHelixPropagator/interface/SteppingHelixPropagator.h"
#include "MagneticField/Engine/interface/MagneticField.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/CSCRecHit/interface/CSCRecHit2D.h"
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

  double pt, eta, phi;
  bool charge;
  bool endcap;

  bool has_TightID;
  bool has_ME11[6];
  bool has_GE11[2];
  bool isGood_GE11[2];
  double phi_ME11[6];
  double phi_GE11[2];
  double phiprop_GE11[2];
};

void MuonData::init()
{
  lumi = -99;
  run = -99;
  event = -99;

  pt = 0.;
  eta = -9.;
  phi = -9.;
  charge = -9;
  endcap = -9;

  has_TightID = 0;
  for (int i=0; i<2; ++i){
    has_GE11[i] = 0;
    phi_GE11[i] = -9;
    phiprop_GE11[i] = -9;
    isGood_GE11[i] = 0;
  }
  for (int i=0; i<6; ++i){
    has_ME11[i] = 0;
    phi_ME11[i] = -9;
  }
}

TTree* MuonData::book(TTree *t)
{
  edm::Service< TFileService > fs;
  t = fs->make<TTree>("MuonData", "MuonData");

  t->Branch("lumi", &lumi);
  t->Branch("run", &run);
  t->Branch("event", &event);

  t->Branch("pt", &pt);
  t->Branch("eta", &eta);
  t->Branch("phi", &phi);
  t->Branch("charge", &charge);
  t->Branch("endcap", &endcap);
  t->Branch("has_TightID", &has_TightID);

  t->Branch("isGood_GE11", isGood_GE11, "isGood_GE11[2]/O");
  t->Branch("has_GE11", has_GE11, "has_GE11[2]/O");
  t->Branch("has_ME11", has_ME11, "has_ME11[6]/O");
  t->Branch("phi_GE11", phi_GE11, "phi_GE11[2]/F");
  t->Branch("phiprop_GE11", phiprop_GE11, "phiprop_GE11[2]/F");
  t->Branch("phi_ME11", phi_ME11, "phi_ME11[6]/F");

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
  edm::EDGetTokenT<edm::View<reco::Muon> > muons_;
  edm::EDGetTokenT<reco::VertexCollection> vertexCollection_;
  edm::Service<TFileService> fs;

  MuonServiceProxy* theService_;
  edm::ESHandle<Propagator> propagator_;
  edm::ESHandle<TransientTrackBuilder> ttrackBuilder_;
  edm::ESHandle<MagneticField> bField_;

  TTree * tree_data_;
  MuonData data_;
};

SliceTestAnalysis::SliceTestAnalysis(const edm::ParameterSet& iConfig)
{
  cscRecHits_ = consumes<CSCRecHit2DCollection>(iConfig.getParameter<edm::InputTag>("cscRecHits"));
  gemRecHits_ = consumes<GEMRecHitCollection>(iConfig.getParameter<edm::InputTag>("gemRecHits"));
  muons_ = consumes<View<reco::Muon> >(iConfig.getParameter<InputTag>("muons"));
  vertexCollection_ = consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexCollection"));
  edm::ParameterSet serviceParameters = iConfig.getParameter<edm::ParameterSet>("ServiceParameters");
  theService_ = new MuonServiceProxy(serviceParameters);

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

  edm::Handle<reco::VertexCollection> vertexCollection;
  iEvent.getByToken( vertexCollection_, vertexCollection );
  if(vertexCollection.isValid()) {
    vertexCollection->size();
    //    std::cout << "vertex->size() " << vertexCollection->size() <<std::endl;
  }

  reco::Vertex goodVertex;
  for (const auto& vertex : *vertexCollection.product()) {
    if (vertex.isValid() && !vertex.isFake() && vertex.tracksSize() >= 2 && fabs(vertex.z()) < 24.) {
      goodVertex = vertex;
      break;
    }
  }

  Handle<View<reco::Muon> > muons;
  iEvent.getByToken(muons_, muons);
  //std::cout << "muons->size() " << muons->size() <<std::endl;

  for (size_t i = 0; i < muons->size(); ++i) {
    edm::RefToBase<reco::Muon> muRef = muons->refAt(i);
    const reco::Muon* mu = muRef.get();
    if (mu->isGEMMuon()) {
      std::cout << "isGEMMuon " <<std::endl;
    }
    const reco::Track* muonTrack = 0;
    if ( mu->globalTrack().isNonnull() ) muonTrack = mu->globalTrack().get();
    else if ( mu->outerTrack().isNonnull()  ) muonTrack = mu->outerTrack().get();


    if (muonTrack) {

      data_.lumi = iEvent.id().luminosityBlock();
      data_.run = iEvent.id().run();
      data_.event = iEvent.id().event();

      data_.pt = mu->pt();
      data_.eta = mu->eta();
      data_.phi = mu->phi();
      data_.charge = mu->charge();
      data_.endcap = mu->eta() > 0 ? 1 : -1 ;


      data_.has_TightID = muon::isTightMuon(*mu, goodVertex);

      std::set<double> detLists;

      reco::TransientTrack ttTrack = ttrackBuilder_->build(muonTrack);
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
          cout << " in chamber "<< ch->id() << " pos = "<<pos<< " R = "<<pos.mag() <<" inside "
               <<  bps.bounds().inside(pos2D) <<endl;

          for (auto hit = muonTrack->recHitsBegin(); hit != muonTrack->recHitsEnd(); hit++) {
            if ( (*hit)->geographicalId().det() == 2 && (*hit)->geographicalId().subdetId() == 4) {
              if ((*hit)->rawId() == ch->id().rawId() ) {
                GEMDetId gemid((*hit)->geographicalId());
                const auto& etaPart = GEMGeometry_->etaPartition(gemid);
                cout << "found it "<< gemid
                     << " lp " << (*hit)->localPosition()
                     << " gp " << etaPart->toGlobal((*hit)->localPosition())
                     << endl;

                data_.has_GE11[gemid.layer()-1] = 1;
                data_.phi_GE11[gemid.layer()-1] = etaPart->toGlobal((*hit)->localPosition()).phi();
              }
            }
          }
        }
      }

      for (const auto& ch : CSCGeometry_->layers()) {

        TrajectoryStateOnSurface tsos = propagator->propagate(ttTrack.outermostMeasurementState(),ch->surface());
        if (!tsos.isValid()) continue;

        GlobalPoint tsosGP = tsos.globalPosition();
        const LocalPoint pos = ch->toLocal(tsosGP);
        const LocalPoint pos2D(pos.x(), pos.y(), 0);
        const BoundPlane& bps(ch->surface());
        //cout << "tsos gp   "<< tsosGP << ch->id() <<endl;

        if (bps.bounds().inside(pos2D)) {
          cout << " in layer "<< ch->id() << " pos = "<<pos<< " R = "<<pos.mag() <<" inside "
               <<  bps.bounds().inside(pos2D) <<endl;

          for (auto hit = muonTrack->recHitsBegin(); hit != muonTrack->recHitsEnd(); hit++) {
            if ((*hit)->geographicalId().subdetId() == MuonSubdetId::GEM) {
              if ((*hit)->rawId() == ch->id().rawId() ) {
                CSCDetId cscid((*hit)->geographicalId());
                const auto& layer = CSCGeometry_->layer(cscid);
                cout << "found it "<< cscid
                     << " lp " << (*hit)->localPosition()
                     << " gp " << layer->toGlobal((*hit)->localPosition())
                     << endl;
                data_.has_ME11[cscid.layer()-1] = 1;
                data_.phi_ME11[cscid.layer()-1] = layer->toGlobal((*hit)->localPosition()).phi();
              }
            }
          }
        }
      }

      if (muonTrack->hitPattern().numberOfValidMuonGEMHits()) {
        std::cout << "numberOfValidMuonGEMHits->size() " << muonTrack->hitPattern().numberOfValidMuonGEMHits()
                  << " recHitsSize " << muonTrack->recHitsSize()
                  << " pt " << muonTrack->pt()
                  <<std::endl;
        for (auto hit = muonTrack->recHitsBegin(); hit != muonTrack->recHitsEnd(); hit++) {
          if ( (*hit)->geographicalId().det() == 2 && (*hit)->geographicalId().subdetId() == 4) {
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
      }

      if (muonTrack->hitPattern().numberOfValidMuonCSCHits()) {
        std::cout << "numberOfValidMuonCSCHits->size() " << muonTrack->hitPattern().numberOfValidMuonCSCHits()
                  << " recHitsSize " << muonTrack->recHitsSize()
                  << " pt " << muonTrack->pt()
                  <<std::endl;
        for (auto hit = muonTrack->recHitsBegin(); hit != muonTrack->recHitsEnd(); hit++) {
          if ( (*hit)->geographicalId().det() == 2 && (*hit)->geographicalId().subdetId() == 4) {
            //if ((*hit)->rawId() == ch->id().rawId() ) {
            CSCDetId cscid((*hit)->geographicalId());
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
      }
    }
    // fill the tree for each muon
    tree_data_->Fill();
  }
}

void SliceTestAnalysis::beginJob(){}
void SliceTestAnalysis::endJob(){}

//define this as a plug-in
DEFINE_FWK_MODULE(SliceTestAnalysis);
