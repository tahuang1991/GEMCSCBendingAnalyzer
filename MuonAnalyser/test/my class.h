//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Jul 27 19:26:31 2018 by ROOT version 5.34/36
// from TTree MuonData/MuonData
// found on file: histo.root
//////////////////////////////////////////////////////////

#ifndef my class_h
#define my class_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

// Fixed size dimensions of array or collections stored in the TTree if any.

class my class {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Int_t           lumi;
   Int_t           run;
   Int_t           event;
   Double_t        muonpt;
   Double_t        muoneta;
   Double_t        muonphi;
   Bool_t          muoncharge;
   Bool_t          muonendcap;
   Bool_t          has_TightID;
   Int_t           isGood_GE11[2];
   Int_t           has_GE11[2];
   Int_t           has_ME11[6];
   Float_t         rechit_phi_GE11[2];
   Float_t         prop_phi_GE11[2];
   Float_t         rechit_phi_ME11[6];
   Float_t         prop_phi_ME11[6];

   // List of branches
   TBranch        *b_lumi;   //!
   TBranch        *b_run;   //!
   TBranch        *b_event;   //!
   TBranch        *b_muonpt;   //!
   TBranch        *b_muoneta;   //!
   TBranch        *b_muonphi;   //!
   TBranch        *b_muoncharge;   //!
   TBranch        *b_muonendcap;   //!
   TBranch        *b_has_TightID;   //!
   TBranch        *b_isGood_GE11;   //!
   TBranch        *b_has_GE11;   //!
   TBranch        *b_has_ME11;   //!
   TBranch        *b_phi_GE11;   //!
   TBranch        *b_prop_phi_GE11;   //!
   TBranch        *b_rechit_phi_ME11;   //!
   TBranch        *b_prop_phi_ME11;   //!

   my class(TTree *tree=0);
   virtual ~my class();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef my class_cxx
my class::my class(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("histo.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("histo.root");
      }
      TDirectory * dir = (TDirectory*)f->Get("histo.root:/SliceTestAnalysis");
      dir->GetObject("MuonData",tree);

   }
   Init(tree);
}

my class::~my class()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t my class::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t my class::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void my class::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("lumi", &lumi, &b_lumi);
   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("event", &event, &b_event);
   fChain->SetBranchAddress("muonpt", &muonpt, &b_muonpt);
   fChain->SetBranchAddress("muoneta", &muoneta, &b_muoneta);
   fChain->SetBranchAddress("muonphi", &muonphi, &b_muonphi);
   fChain->SetBranchAddress("muoncharge", &muoncharge, &b_muoncharge);
   fChain->SetBranchAddress("muonendcap", &muonendcap, &b_muonendcap);
   fChain->SetBranchAddress("has_TightID", &has_TightID, &b_has_TightID);
   fChain->SetBranchAddress("isGood_GE11", isGood_GE11, &b_isGood_GE11);
   fChain->SetBranchAddress("has_GE11", has_GE11, &b_has_GE11);
   fChain->SetBranchAddress("has_ME11", has_ME11, &b_has_ME11);
   fChain->SetBranchAddress("rechit_phi_GE11", rechit_phi_GE11, &b_phi_GE11);
   fChain->SetBranchAddress("prop_phi_GE11", prop_phi_GE11, &b_prop_phi_GE11);
   fChain->SetBranchAddress("rechit_phi_ME11", rechit_phi_ME11, &b_rechit_phi_ME11);
   fChain->SetBranchAddress("prop_phi_ME11", prop_phi_ME11, &b_prop_phi_ME11);
   Notify();
}

Bool_t my class::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void my class::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t my class::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef my class_cxx
