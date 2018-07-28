import ROOT
import os

def plot_tree_1D(filename, treename, branch_name, cut, xtitle, nbins, xmin, xmax, plotname):

    F=ROOT.TFile.Open(filename);
    c1=ROOT.TCanvas("c1","New Graph",0,0 600,800);
    #h=F.Get("SliceTestAnalysis/MuonData");
    tree=F.Get(treename);
    hist = ROOT.TH1F("hist","hist_title", nbins, xmin, xmax)
    
    ##cut = "muonpt>10"
    tree.Draw(branch_name + ">> hist", cut);## plot hist with cut
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2017")
    hist.GetXaxis().SetTitle(xtitle)
    outplot = os.path.join(plotname, str(branch_name))
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




plot_tree_1D(filename, treename, branch_name, cut, xtitle, nbins, xmin, xmax, plotname)


branch_list=["lumi","run","event","muonpt","muoneta","muonphi","muoncharge","muonendcap","has_TightID","isGood_GE11","has_GE11","has_ME11","rechit_phi_GE11",
"prop_phi_GE11","rechit_phi_ME11","prop_phi_ME11"]

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


