import ROOT
import os
import time
def plot_tree_1D(tree, branch_name, cut, xtitle, nbins, xmin, xmax, text, plotname):

   
    c1=ROOT.TCanvas("c1","New Graph",0,0, 800,600);
    #h=F.Get("SliceTestAnalysis/MuonData");
    hist = ROOT.TH1F("hist","hist_title", nbins, xmin, xmax)
    
    ##cut = "muonpt>10"
    tree.Draw(branch_name + ">> hist", cut);## plot hist with cut
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2018C")
    hist.GetXaxis().SetTitle(xtitle)
    #hist.SetStat(0)
    print "todraw ", branch_name, " cut ",cut
#    outplot = os.path.join(plotname, str(branch_name))
    txt = ROOT.TLatex(.5, .6, text)
    txt.SetNDC()
    txt.SetTextFont(42)
    txt.SetTextFont(42)
    txt.SetTextSize(.04)
    txt.Draw("same")
    
    #outplot = os.path.join(os.getcwd(), str(plotname))
    outplot = plotname
    c1.SaveAs(outplot + ".png")
    c1.SaveAs(outplot + ".pdf")


def plot_tree_2D(tree, branch_name_x, branch_name_y, cut, xtitle, xnbins, xmin, xmax,  ytitle, ynbins, ymin, ymax, text, plotname):

    c1=ROOT.TCanvas("c1","New Graph",0,0,800,600);
    #h=F.Get("SliceTestAnalysis/MuonData");
    hist = ROOT.TH2F("hist","hist_title", xnbins, xmin, xmax, ynbins, ymin, ymax)
    
    todraw = branch_name_y +":"+branch_name_x;
    ##cut = "muonpt>10"
    tree.Draw(todraw + ">> hist", cut, "colz");## plot hist with cut
    print "todraw ",todraw, " cut ",cut
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2018C")
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    #hist.SetStat(0)
    #outplot = os.path.join(plotname, str(branch_name))
    outplot = plotname
    txt = ROOT.TLatex(.15, .8, text)
    txt.SetNDC()
    txt.SetTextFont(42)
    txt.SetTextSize(.04)
    txt.Draw("same")

    c1.SaveAs(outplot + ".png")
    #c1.SaveAs(outplot + ".pdf")

def plot_tree_3D(tree, branch_name_x, branch_name_y,branch_name_z, cut, xtitle, xnbins, xmin, xmax,  ytitle, ynbins, ymin, ymax,ztitle,znbins, zmin, zmax, text, plotname):

    c1=ROOT.TCanvas("c1","New Graph",0,0,800,600);
    #h=F.Get("SliceTestAnalysis/MuonData");
    hist = ROOT.TH2F("hist","hist_title", xnbins, xmin, xmax, ynbins, ymin, ymax, znbins, zmin, zmax,)

    todraw = branch_name_y +":"+branch_name_x+":"+branch_name_z;
    ##cut = "muonpt>10"
    tree.Draw(todraw + ">> hist", cut, "colz");## plot hist with cut
    print "todraw ",todraw, " cut ",cut
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2018C")
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetZaxis().SetTitle(ztitle)


    #hist.SetStat(0)
    #outplot = os.path.join(plotname, str(branch_name))
    outplot = plotname
    txt = ROOT.TLatex(.15, .8, text)
    txt.SetNDC()
    txt.SetTextFont(42)
    txt.SetTextSize(.04)
    txt.Draw("same")

    c1.SaveAs(outplot + ".png")
    #c1.SaveAs(outplot + ".pdf")





branch_list=["lumi", "run", "event", "muonpt","muoneta", "muonphi", "muoncharge", "muonendcap", "muonPx","muonPy","muonPz", "muondxy", "muondz", "muon_ntrackhit", "muon_chi2", "muonPFIso","muonTkIso", "muon_nChamber", "has_MediumID", "has_LooseID", "has_TightID", "has_ME11", "chamber_ME11", "has_propME11", "ring_ME11", "chamber_propME11", "ring_propME11","rechit_phi_ME11", "rechit_eta_ME11", "prop_phi_ME11", "rechit_x_ME11", "rechit_y_ME11", "rechit_r_ME11","rechit_localx_ME11","rechit_localy_ME11" "rechit_L1eta_ME11", "rechit_L1phi_ME11", "rechit_hitWire_ME11", "rechit_WG_ME11", "rechit_nStrips_ME11", "rechit_centralStrip_ME11", "rechit_used_ME11", "prop_eta_ME11", "prop_x_ME11", "prop_y_ME11", "prop_r_ME11", "rechit_prop_dR_ME11", "rechit_prop_dphi_ME11", "isGood_GE11", "has_GE11", "roll_GE11", "chamber_GE11", "rechit_phi_GE11","rechit_eta_GE11","rechit_x_GE11", "rechit_y_GE11", "rechit_r_GE11", "rechit_used_GE11", "rechit_BX_GE11", "rechit_firstClusterStrip_GE11", "rechit_clusterSize_GE11", "has_propGE11", "roll_propGE11", "chamber_propGE11", "prop_phi_GE11", "prop_eta_GE11", "prop_x_GE11", "prop_y_GE11", "prop_r_GE11", "rechit_prop_dR_GE11","rechit_prop_dX_GE11", "rechit_prop_dphi_GE11","has_cscseg_st", "cscseg_phi_st", "cscseg_eta_st", "cscseg_x_st", "cscseg_y_st", "cscseg_r_st", "cscseg_prop_dR_st", "cscseg_prop_dphi_st", "cscseg_chamber_st","cscseg_ring_st", "has_csclct_st","csclct_phi_st", "csclct_eta_st", "csclct_x_st", "csclct_y_st", "csclct_r_st",  "csclct_chamber_st","csclct_ring_st","csclct_prop_dR_st","csclct_prop_dphi_st", "csclct_keyStrip_st", "csclct_keyWG_st","csclct_matchWin_st","csclct_pattern_st", "dphi_CSCL1_GE11L1","dphi_fitCSCL1_GE11L1","dphi_CSCSeg_GE11Rechit", "dphi_keyCSCRechit_GE11Rechit", "dphi_CSCRechits_GE11Rechit", "dphi_propCSC_propGE11","dphi_keyCSCRechitL1_GE11Rechit", "nrechit_ME11", "ncscseg", "ncscLct", "nrechit_GE11", "prop_localx_ME11","prop_localy_ME11","rechit_localx_GE11","rechit_localy_GE11","prop_localx_GE11","prop_localy_GE11"]
chain = ROOT.TChain("SliceTestAnalysis/MuonData")
chain.Add('out_ana_all_2018C_v5.root')
#chain.Add("slicetest_ana.root")
#chain.Add("2017G_out_ana.root")
#for branch_name1 in branch_list:

#treename1='SliceTestAnalysis/MuonData'		
#	print branch_name1
##
##	if branch_name1 == "rechit_phi_GE11":
##		cut1="has_GE11=1"
##	else :



def dx_x_y_rechit(chamber_number,layer_number):

        cut1="has_GE11["+str(layer_number)+"]>0  && chamber_GE11["+str(layer_number)+"]=="+str(chamber_number)
        nxbins1=200
        nybins1=200
        nzbins1=200
        xmin1=-1.5
        xmax1=1.5
        ymin1=-1.5
        ymax1=1.5
        zmin1=-1.5
        zmax1=1.5

        plotname1='rechit_3d_plot_GE11_chamber_'+str(chamber_number)+'_layer_'+str(layer_number)
        brx="rechit_localx_GE11["+str(layer_number)+"]";
        bry="rechit_localy_GE11["+str(layer_number)+"]";
        brz="rechit_prop_dX_GE11["+str(layer_number)+"]";

        text=cut1
        ytitle1="rechit_loacly_GE11["+str(layer_number)+"]";
        xtitle1="rechit_localx_GE11["+str(layer_number)+"]";
        ztitle1="rechit_prop_dX_GE11["+str(layer_number)+"]";

        plot_tree_3D(chain, brx, bry,bry, cut1, xtitle1, nxbins1, xmin1, xmax1,  ytitle1, nybins1, ymin1, ymax1,ytitle1, nzbins1, ymin1, ymax1, text, plotname1)
dx_x_y_rechit(29,1);
def dx_x_y_extraploated(chamber_number,layer_number):

        cut1="has_GE11["+str(layer_number)+"]>0  && chamber_GE11["+str(layer_number)+"]=="+str(chamber_number)
        nxbins1=200
        nybins1=200
        nzbins1=200
        xmin1=-1.5
        xmax1=1.5
        ymin1=-1.5
        ymax1=1.5
        zmin1=-1.5
        zmax1=1.5

        plotname1='extrapolated_3d_plot_GE11_chamber_'+str(chamber_number)+'_layer_'+str(layer_number)
    #    brx="rechit_localx_GE11["+str(layer_number)+"]";
    #    bry="rechit_localy_GE11["+str(layer_number)+"]";
    #    brz="rechit_prop_dX_GE11["+str(layer_number)+"]";

        text=cut1
    #    ytitle1="rechit_loacly_GE11["+str(layer_number)+"]";
    #    xtitle1="rechit_localx_GE11["+str(layer_number)+"]";
    #    ztitle1="rechit_prop_dX_GE11["+str(layer_number)+"]";

        plot_tree_3D(chain, brx, bry,bry, cut1, xtitle1, nxbins1, xmin1, xmax1,  ytitle1, nybins1, ymin1, ymax1,ytitle1, nzbins1, ymin1, ymax1, text, plotname1)
dx_x_y_extrapolated(29,1);


def prop_rechit_phi(chamber_number,layer_number):
	
	cut1="has_GE11["+str(layer_number)+"]>0  && chamber_GE11["+str(layer_number)+"]=="+str(chamber_number)	
	xtitle1="prop_phi_GE11["+str(layer_number)+"]";
	nbins1=200##why always 10bins?
	xmin1=-1.5## why range goes from [0.0, 5]?
	xmax1=-1.3
	ymin1=-1.5
	ymax1=-1.3
	plotname1='rechit_and_prop_phi_GE11_chamber_'+str(chamber_number)+'_layer_'+str(layer_number)
	brx="prop_phi_GE11["+str(layer_number)+"]";
	bry="rechit_phi_GE11["+str(layer_number)+"]";
	text=cut1
	ytitle1="rechit_phi_GE11["+str(layer_number)+"]";
	plot_tree_2D(chain, brx, bry, cut1, xtitle1, nbins1, xmin1, xmax1,  ytitle1, nbins1, ymin1, ymax1, text, plotname1)

def dphi_key_CSC(chamber_number,layer_number):

        cut1="has_GE11["+str(layer_number)+"]>0  && chamber_GE11["+str(layer_number)+"]=="+str(chamber_number)
        xtitle1="dphi_keyCSCRechit_GE11["+str(layer_number)+"]";
        nbins1=200##why always 10bins?
        xmin1=-.04## why range goes from [0.0, 5]?
        xmax1=.04
        ymin1=0
        ymax1=80
        plotname1='dphi_GE11_chamber_'+str(chamber_number)+'_layer_'+str(layer_number)
        brx="dphi_keyCSCRechit_GE11Rechit["+str(layer_number)+"]";
        bry="muonpt";
        text=cut1
        ytitle1="muonpt";
        plot_tree_2D(chain, brx, bry, cut1, xtitle1, nbins1, xmin1, xmax1,  ytitle1, nbins1, ymin1, ymax1, text, plotname1)
def plot_for_meeting():

    for i in [0,1]:
        for j in [27,28,29,30]:
            prop_rechit_phi(j,i);
            dphi_key_CSC(j,i);

#plot_for_meeting();
#	plot_tree_1D(filename1, treename1, branch_name1, cut1, xtitle1, nbins1, xmin1, xmax1, plotname1)
#print ('##################################################\n\n\n')
#print('#########################################################')
#plot_tree_1D(filename, treename, branch_name, cut, xtitle, nbins, xmin, xmax, plotname)
#plotdir = "GEMCSCBending_2018C_graphs/"
#os.system("mkdir -p "+plotdir)
def plotmuons(chain, cut, plotdir):
    text = "reco muon"
    todrawlist = ["muonpt", "muoneta","muonphi","muonendcap"]
    xbinlist = [[50, 0, 200.0], [40, 0, 2.5], [60, -3.14, 3.14], [3, -1.5, 1.5]]
    for i, todraw in enumerate(todrawlist):
	xbins = xbinlist[i]
	plotname = os.path.join(plotdir, "2018C_GEMCSCbending_"+todraw)
	plot_tree_1D(chain, todraw, cut, todraw, xbins[0], xbins[1], xbins[2], text, plotname)

#plotmuons(chain, "has_TightID", plotdir)


def plotdeltaR(chain, cut, text, plotdir):
    
    todraws_ME11 = "rechit_prop_dR_ME11"
    for i in range(0, 6):#6layers for CSC
        todraw = todraws_ME11+"[%d]"%i
        thiscut = cut + "&& has_ME11[%d]>0"%i
#	plotname = os.path.join(plotdir, "2018C_GEMCSCbending_rechit_prop_dR_ME11_CSClayer%d"%i)
        plotname = os.path.join(plotdir, "pt_25_2018C_GEMCSCbending_rechit_prop_dR_ME11_CSClayer%d"%i)
	plot_tree_1D(chain, todraw, thiscut, todraw, 100, 0.0, 20.0, text,plotname)

    todraws_GE11 = "rechit_prop_dR_GE11"
    for i in range(0, 2):#2layers for GEM
        todraw = todraws_GE11+"[%d]"%i
        thiscut = cut + "&& has_GE11[%d]>0"%i
#	plotname = os.path.join(plotdir, "2018C_GEMCSCbending_rechit_prop_dR_GE11_GEMlayer%d"%i)
        plotname = os.path.join(plotdir, "pt_25__2018C_GEMCSCbending_rechit_prop_dR_GE11_GEMlayer%d"%i)
	plot_tree_1D(chain, todraw, thiscut, todraw, 100, 0.0, 20.0, text,plotname)

    todraws_seg = "cscseg_prop_dR_st"
    for i in range(0, 4):#4 station CSCs 
        todraw = todraws_seg+"[%d]"%i
        thiscut = cut + " && has_cscseg_st[%d]>0"%i
#	plotname = os.path.join(plotdir, "2018_GEMCSCbending_cscseg_prop_dR_st%d"%i)
        plotname = os.path.join(plotdir, "pt_25__2018C_GEMCSCbending_cscseg_prop_dR_st%d"%i)
	plot_tree_1D(chain, todraw, thiscut, todraw, 100, 0.0, 20.0, text,plotname)

#plotdeltaR(chain, "has_TightID && muonpt>25","muon p_{T}>25, tight ID", plotdir)



def plotCSCHits(chain, cut, text, plotdir):
    todrawX_seg = "cscseg_x_st"
    todrawY_seg = "cscseg_y_st"
    for i in range(0, 4):
	todrawX = todrawX_seg + "[%d]"%i
	todrawY = todrawY_seg + "[%d]"%i
	plotname = os.path.join(plotdir, "2018C_GEMCSCbending_CSCsegment_x_y_st%d"%i)
	thiscut = cut + " && has_cscseg_st[%d]>0 && cscseg_prop_dR_st[%d] < 5.0"%(i, i) 
        plot_tree_2D(chain, todrawX, todrawY, thiscut, "CSC Segment X", 100, -600.0, 600.0,  "CSC segment Y", 600, -600.0, 600.0,text, plotname)

    todrawX_seg = "rechit_x_ME11"
    todrawY_seg = "rechit_y_ME11"
    for i in range(0, 6):
	todrawX = todrawX_seg + "[%d]"%i
	todrawY = todrawY_seg + "[%d]"%i
	plotname = os.path.join(plotdir, "2018C_GEMCSCbending_CSCRechit_x_y_ME11layer%d"%i)
	thiscut = cut + " && has_ME11[%d]>0 && rechit_prop_dR_ME11[%d] < 5.0"%(i, i) 
        plot_tree_2D(chain, todrawX, todrawY, thiscut, "CSC Rechit X", 100, -600.0, 600.0,  "CSC Rechit Y", 600, -600.0, 600.0,text, plotname)

#plotCSCHits(chain, "has_TightID && muonpt>10", "muon p_{T}> 10, tight ID",plotdir)



def plotGEMHits(chain, cut, text, plotdir):
    todrawX_gem = "rechit_x_GE11"
    todrawY_gem = "rechit_y_GE11"
    for i in range(0, 2):
	todrawX = todrawX_gem + "[%d]"%i
	todrawY = todrawY_gem + "[%d]"%i
	plotname = os.path.join(plotdir, "2018C_GEMCSCbending_GEMRechit_x_y_gemlayer%d"%i)
	thiscut = cut + " && has_GE11[%d]>0 && rechit_prop_dR_GE11[%d] < 5.0"%(i, i) 
        plot_tree_2D(chain, todrawX, todrawY, thiscut, "GEM Rechit X", 100, -600.0, 600.0,  "GEM Rechit Y", 100, -600.0, 600.0, text, plotname)

#plotGEMHits(chain, "has_TightID && muonpt>10", "muon p_{T}> 10, tight ID",plotdir)


def plotdeltaPhi(chain, cut, text, plotdir):
    todrawlist  = ["dphi_CSCSeg_GE11Rechit", "dphi_keyCSCRechit_GE11Rechit", "dphi_propCSC_propGE11"]
    for i, todraw in enumerate(todrawlist):
	for layer in range(0,2):
	    todraw_dphi = todraw + "[%d]"%layer
	    plotname = os.path.join(plotdir, "pt_50_2018C_GEMCSCbending_%s_gemlayer%d"%(todraw, layer))
	    thiscut = cut + " &&  has_GE11[%d]>0 && has_propGE11[%d]>0 && has_ME11[2]>0 "%(layer, layer)
	    plot_tree_1D(chain, todraw, thiscut, todraw_dphi, 60, -0.30, 0.3, text, plotname)

#plotdeltaPhi(chain, "has_TightID && muonpt>50", "muon p_{T}>50, tight ID",plotdir)
