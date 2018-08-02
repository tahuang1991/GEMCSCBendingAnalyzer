import ROOT
import os
import time
os.chdir('/eos/uscms/store/user/mkhurana/GEMCSCBending_2017G/Graphs')
def plot_tree_1D(filename, treename, branch_name, cut, xtitle, nbins, xmin, xmax, plotname):

    F=ROOT.TFile.Open(filename);
    c1=ROOT.TCanvas("c1","New Graph",0,0, 600,800);
    #h=F.Get("SliceTestAnalysis/MuonData");
    tree=F.Get(treename);
    hist = ROOT.TH1F("hist","hist_title", nbins, xmin, xmax)
    
    ##cut = "muonpt>10"
    tree.Draw(branch_name + ">> hist", cut);## plot hist with cut
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2017")
    hist.GetXaxis().SetTitle(xtitle)
#    outplot = os.path.join(plotname, str(branch_name))
    
    outplot = os.path.join(os.getcwd(), str(plotname))
    c1.SaveAs(outplot + ".png")
    c1.SaveAs(outplot + ".pdf")


def plot_tree_2D(filename, treename, branch_name_x, branch_name_y, cut, xtitle, xnbins, xmin, xmax,  ytitle, ynbins, ymin, ymax, plotname):

    F=ROOT.TFile.Open(filename);
    c1=ROOT.TCanvas("c1","New Graph",0,0,600,800);
    #h=F.Get("SliceTestAnalysis/MuonData");
    tree=F.Get(treename);
    hist = ROOT.TH2F("hist","hist_title", xnbins, xmin, xmax, ynbins, ymin, ymax)
    
    ##cut = "muonpt>10"
    tree.Draw(branch_name + ">> hist", cut);## plot hist with cut
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2017")
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    outplot = os.path.join(plotname, str(branch_name))

    c1.SaveAs(outplot + ".png")
    c1.SaveAs(outplot + ".pdf")

branch_list=["lumi","run","event","muonpt","muoneta","muonphi","muoncharge","muonendcap","has_TightID","isGood_GE11","has_GE11","has_ME11","rechit_phi_GE11",
"prop_phi_GE11","rechit_phi_ME11","prop_phi_ME11","muonPx","muonPy","muonPz","muondxy","muondz","muon_ntrackhit","muon_nChameber","muon_chi2","muonPFIso","muonTkIso", "muon_nChamber","has_MediumID","has_LooseID", 
"rechit_eta_ME11", "rechit_x_ME11", "rechit_y_ME11", "rechit_r_ME11", "prop_eta_ME11","prop_x_ME11", "prop_y_ME11", "prop_r_ME11", "rechit_prop_dR_ME11","chamber_ME11", "roll_GE11", "chamber_GE11", "rechit_eta_GE11", "rechit_x_GE11",
"rechit_y_GE11", "rechit_r_GE11", "prop_eta_GE11", "prop_x_GE11", "prop_y_GE11","prop_r_GE11","rechit_prop_dR_GE11","has_cscseg_st",
"cscseg_phi_st","cscseg_eta_st","cscseg_x_st","cscseg_y_st","cscseg_z_st","cscseg_prop_dR_st",
"cscseg_chamber_st","cscseg_ring_st","has_csclct_st","csclct_phi_st","csclct_eta_st","csclct_x_st", "csclct_y_st", "csclct_r_st","csclct_chamber_st","csclct_ring_st",
"csclct_prop_dR_st", "csclct_keyStrip_st", "csclct_keyWG_st","csclct_matchWin_st","csclct_pattern_st", "has_propME11", "ring_ME11",
"chamber_propME11","ring_propME11","has_propGE11","roll_propGE11","chamber_propGE11",  "dphi_CSCL1_GE11L1",
"dphi_fitCSCL1_GE11L1","dphi_CSCSeg_GE11Rechit","dphi_keyCSCRechit_GE11Rechit","dphi_CSCRechits_GE11Rechit","dphi_propCSC_propGE11"]

for number in range(555):

	filename1='/eos/uscms/store/user/mkhurana/GEMCSCBending_2017G/out_ana_'+str(number)+'.root'
	for branch_name1 in branch_list:
    		treename1='SliceTestAnalysis/MuonData'		
		print branch_name1
##
#	if branch_name1 == "rechit_phi_GE11":
#		cut1="has_GE11=1"
#	else :
		cut1="muonpt>10"	
		xtitle1=branch_name1+' '+cut1;
		nbins1=10
		xmin1=0
		xmax1=5
    		plotname1=branch_name1+'_'+'out_ana_'+str(number)
    		plot_tree_1D(filename1, treename1, branch_name1, cut1, xtitle1, nbins1, xmin1, xmax1, plotname1)
	print ('##################################################\n\n\n')
	print('#########################################################')
	time.sleep(1)
#plot_tree_1D(filename, treename, branch_name, cut, xtitle, nbins, xmin, xmax, plotname)



#for name in branch_list:
#	plot_hist(name);
	


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


