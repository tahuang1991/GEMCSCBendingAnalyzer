import ROOT
import os
os.chdir("/afs/cern.ch/user/m/mkhurana/CMSSW_10_1_5/src/GEMCSCBendingAnalyzer/MuonAnalyser/test")

F=ROOT.TFile.Open('histo.root');

def plot_hist(branch_name):
	c1=ROOT.TCanvas("c1","New Graph",0,0,1600,1000);
	h=F.Get("SliceTestAnalysis/MuonData");
	h.Draw(branch_name);
	k=str(branch_name)+".png"
	
	os.chdir("/afs/cern.ch/user/m/mkhurana/private/Graphs_bendingangle")

	c1.Print(k);
	os.chdir("/afs/cern.ch/user/m/mkhurana/CMSSW_10_1_5/src/GEMCSCBendingAnalyzer/MuonAnalyser/test")
	

branch_list=["lumi","run","event","muonpt","muoneta","muonphi","muoncharge","muonendcap","has_TightID","isGood_GE11","has_GE11","has_ME11","rechit_phi_GE11",
"prop_phi_GE11","rechit_phi_ME11","prop_phi_ME11","muonPx","muonPy","muonPz","muondxy","muondz","muon_ntrackhit","muon_nChameber","muon_chi2","muonPFIso","muonTkIso", "muon_nChamber","has_MediumID","has_LooseID", "phipro_ME11", 
"rechit_eta_ME11", "rechit_x_ME11", "rechit_y_ME11", "rechit_r_ME11", "prop_eta_ME11","prop_x_ME11", "prop_y_ME11", "prop_r_ME11", "rechit_prop_dR_ME11","chamber_ME11", "roll_GE11", "chamber_GE11", "rechit_eta_GE11", "rechit_x_GE11",
"rechit_y_GE11", "rechit_r_GE11", "prop_eta_GE11", "prop_x_GE11", "prop_y_GE11","prop_r_GE11","rechit_prop_dR_GE11","dphi_CSC_GE11","dphi_keyCSC_GE11", "dphi_fitCSC_GE11"]

for name in branch_list:
	plot_hist(name);
	


#print(h.Print());
#for bname in branch_list:
#	print bname
#print(len(branch_list))
#h.MakeClass("my class")
#k=h.GetListOfBranches()
#print(k.Print());
#c1.Divide(4,4);
#c1.cd(2);
#h.Draw("has_ME11");
#c1.cd(3);
#h.Draw("muonphi");
#c1.cd(4);
#h.Draw("muonpt");
#c1.Print("output_hist.png")


