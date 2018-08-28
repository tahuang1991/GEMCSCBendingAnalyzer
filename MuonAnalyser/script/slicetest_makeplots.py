import ROOT
import os
import time

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetStatW(0.07)
ROOT.gStyle.SetStatH(0.06)

ROOT.gStyle.SetOptStat(111110)

#ROOT.gStyle.SetErrorX(0)
#ROOT.gStyle.SetErrorY(0)

ROOT.gStyle.SetTitleStyle(0)
ROOT.gStyle.SetTitleAlign(13) ## coord in top left
ROOT.gStyle.SetTitleX(0.)
ROOT.gStyle.SetTitleY(1.)
ROOT.gStyle.SetTitleW(1)
ROOT.gStyle.SetTitleH(0.058)
ROOT.gStyle.SetTitleBorderSize(0)

ROOT.gStyle.SetPadLeftMargin(0.126)
ROOT.gStyle.SetPadRightMargin(0.10)
ROOT.gStyle.SetPadTopMargin(0.06)
ROOT.gStyle.SetPadBottomMargin(0.13)

ROOT.gStyle.SetMarkerStyle(1)

import numpy as np

color = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2, ROOT.kMagenta+2,ROOT.kCyan+2 ]
marker = [20,21,22,23,33]
def setcolortables():
     red = np.array([ 0.0, 1.0, 1.0], dtype=np.double)
     green = np.array([ 0.0, 1.0, 0.0], dtype=np.double)
     blue = np.array([ 1.0, 1.0, 0.0], dtype=np.double)
     stop = np.array([ 0.0, 0.5, 1.0], dtype=np.double)
     print "red ",red
     ROOT.TColor.CreateGradientColorTable(3, stop, red, green, blue, 40)
     
def cloneDummyHistogram(Histogram):
    dummyhist = Histogram.Clone()
    dummyhist.SetName("dummy")
    for xbin in xrange(dummyhist.GetNbinsX()):
        dummyhist.SetBinContent(xbin+1, 0.0)
        dummyhist.SetBinError(xbin+1, 0.0)
    return dummyhist
    
def getTefficiency(ch, todraw, dencut, numcut, xbins):
    hden = ROOT.TH1F("hden","hden", len(xbins)-1, xbins)
    hnum = ROOT.TH1F("hnum","hnum", len(xbins)-1, xbins)
    print " dencut, ",dencut," numcut ",numcut
    ch.Draw(todraw+">>hden", dencut)
    ch.Draw(todraw+">>hnum", numcut)
    Teff = ROOT.TEfficiency(hnum, hden)
    ROOT.SetOwnership(Teff, False)
    return Teff
    
    
#_____________________________________________________________
def makeEffplot(Teffs, xtitle,ytitle, legs, legheader, txt,picname):
	
    #b1 = ROOT.TH1F("b1","b1")
    b1 = cloneDummyHistogram(Teffs[0].GetCopyTotalHisto())
    b1.GetYaxis().SetRangeUser(0.0,1.05)
    b1.GetYaxis().SetTitleOffset(1.1)
    b1.GetYaxis().SetNdivisions(520)
    b1.GetYaxis().SetTitle(ytitle)
    b1.GetXaxis().SetTitle(xtitle)
    b1.GetXaxis().SetTitleSize(0.05)
    b1.GetXaxis().SetLabelSize(0.05)
    b1.GetYaxis().SetTitleSize(0.05)
    b1.GetYaxis().SetLabelSize(0.05)
    b1.SetTitle(" #scale[1.4]{#font[61]{CMS}} #font[52]{Internal}"+"  "*8+" 2018 RunC")
    
    c1 = ROOT.TCanvas()
    c1.SetGridx()
    c1.SetGridy()
    c1.SetTickx()
    c1.SetTicky()
    #c1.SetLogx()

    b1.SetStats(0)
    b1.Draw()
    color = [2,4,3,5,6,7,8,9,1]
    #marker = [20,21, 22, 23,, 24, 25]
    marker = [20,21,22,23,33, 24, 25, 26, 27, 28, 30]
    legend = ROOT.TLegend(0.65,0.20,0.8,0.24+0.04*len(Teffs))
    legend.SetFillColor(ROOT.kWhite)
    legend.SetTextFont(42)
    legend.SetTextSize(.035)
    legend.SetHeader("%s"%legheader)
    for m, Teff in enumerate(Teffs):
	Teffs[m].SetLineColor(color[m])
	Teffs[m].SetMarkerColor(color[m])
	Teffs[m].SetMarkerStyle(marker[m])
	Teffs[m].Draw("same")
	legend.AddEntry(Teffs[m],"%s"%legs[m],"pl")
    #print "Teffs ",Teffs
    #Teffs[0].Print("ALL")
    legend.Draw("same")

    tex = ROOT.TLatex(0.35,0.57,"%s"%txt)
    #tex = ROOT.TLatex(0.45,0.57,"#splitline{%s}{%d%% eff at %d [GeV]}"%(txt,fractionToKeep,pt))
    #tex = ROOT.TLatex(0.45,0.57,"#splitline{%s}{check the sign of #Delta Y_{12} and #Delta Y_{23}}"%(txt))
    tex.SetTextSize(0.05)
    tex.SetTextFont(62)
    tex.SetNDC()
    tex.Draw("same")
    #c1.Update()
    c1.SaveAs("%s.png"%(picname))
    c1.SaveAs("%s.pdf"%(picname))
    #c1.SaveAs("%s.C"%(picname))
	

def plotGEMHitEff(chain, todraw, dencut, xbins,xtitle, txt, plotdir):

    ytitle = "GEM hit efficiency"
    for ch in [27, 28, 29, 30]:
        Teff_layers = []
        leg_layers = []
        for layer in [0, 1]:
            dRcut = "&& abs(rechit_prop_dphi_GE11[%d])<.02"%(layer)
            layercut = "has_propGE11[%d] && chamber_propGE11[%d] == %d && has_cscseg_st[0] && cscseg_chamber_st[0]==%d"%(layer, layer, ch, ch)## 
            thisdencut = dencut + " && "+ layercut
            thisnumcut = dencut + " && "+ layercut+"&& has_GE11[%d] && chamber_GE11[%d] == %d"%(layer, layer, ch)  +dRcut
            Teff_layers.append(getTefficiency(chain, todraw, thisdencut, thisnumcut, xbins))
            leg_layers.append("layer %d"%(layer+1))

            Teff_rolls = []
            leg_rolls = []
            header_roll = "GEM %d,layer%d"%(ch, layer+1)
            for roll in range(1, 9):
                detidcut = layercut +"&& roll_propGE11[%d] == %d"%(layer, roll)
                thisdencut  = dencut + " && "+detidcut
                #thisnumcut = dencut + " && "+detidcut+"&& has_GE11[%d] && chamber_GE11[%d] == %d && roll_GE11[%d]==%d"%(layer, layer, ch, layer,roll)
                thisnumcut = dencut + " && "+detidcut+"&& has_GE11[%d] && chamber_GE11[%d] == %d"%(layer, layer, ch)+dRcut
                Teff_rolls.append(getTefficiency(chain, todraw, thisdencut, thisnumcut, xbins))
                leg_rolls.append("roll%d"%(roll))
            picname_roll = plotdir + "ch%d_layer%d_rolls"%(ch, layer)
            makeEffplot(Teff_rolls, xtitle, ytitle, leg_rolls, header_roll, txt, picname_roll)
        header_layer = "GEM %d"%(ch)
        picname_layer = plotdir+"ch%d_layers"%(ch)
        makeEffplot(Teff_layers, xtitle, ytitle, leg_layers, header_layer, txt, picname_layer)


###
def plotGEMHitEff_phi(chain, dencut, txt, plotdir):
    ytitle = "GEM hit efficiency"
    xtitle = "Muon global #phi at GE11"
    for ch in [27, 28, 29, 30]:
        Teff_layers = []
        leg_layers = []
        phimin = -1.850 + (ch-27)*0.175
        phimax = -1.650 + (ch-27)*0.175
        phibin = 20
        phi_step = abs(phimax-phimin)/phibin
        phibin_x = np.arange(phimin, phimax, phi_step)
        for layer in [0, 1]:
            todraw = "prop_phi_GE11[%d]"%layer
            dRcut = "&& abs(rechit_prop_dphi_GE11[%d])<.02"%(layer)
            layercut = "has_propGE11[%d] && chamber_propGE11[%d] == %d && has_cscseg_st[0] && cscseg_chamber_st[0]==%d"%(layer, layer, ch, ch)## 
            thisdencut = dencut + " && "+ layercut
            thisnumcut = dencut + " && "+ layercut+"&& has_GE11[%d] && chamber_GE11[%d] == %d"%(layer, layer, ch)  +dRcut
            Teff_layers.append(getTefficiency(chain, todraw, thisdencut, thisnumcut, phibin_x))
            leg_layers.append("layer %d"%(layer+1))
            Teff_rolls = []
            leg_rolls = []
            header_roll = "GEM %d,layer%d"%(ch, layer+1)
            for roll in range(1, 9):
                detidcut = layercut +"&& roll_propGE11[%d] == %d"%(layer, roll)
                thisdencut  = dencut + " && "+detidcut
                #thisnumcut = dencut + " && "+detidcut+"&& has_GE11[%d] && chamber_GE11[%d] == %d && roll_GE11[%d]==%d"%(layer, layer, ch, layer,roll)
                thisnumcut = dencut + " && "+detidcut+"&& has_GE11[%d] && chamber_GE11[%d] == %d"%(layer, layer, ch)+dRcut
                Teff_rolls.append(getTefficiency(chain, todraw, thisdencut, thisnumcut, phibin_x))
                leg_rolls.append("roll%d"%(roll))
            picname_roll = plotdir + "ch%d_layer%d_rolls"%(ch, layer)
            makeEffplot(Teff_rolls, xtitle, ytitle, leg_rolls, header_roll, txt, picname_roll)
        header_layer = "GEM %d"%(ch)
        picname_layer = plotdir+"ch%d_layers"%(ch)
        makeEffplot(Teff_layers, xtitle, ytitle, leg_layers, header_layer, txt, picname_layer)


def plot_tree_1D(tree, branch_name, cut, xtitle, nbins, xmin, xmax, text, plotname):

   
    c1=ROOT.TCanvas("c1","New Graph",0,0, 800,600);
    #h=F.Get("SliceTestAnalysis/MuonData");
    hist = ROOT.TH1F("hist","hist_title", nbins, xmin, xmax)
    
    ##cut = "muonpt>10"
    tree.Draw(branch_name + ">> hist", cut);## plot hist with cut
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2018C")
    hist.GetXaxis().SetTitle(xtitle)
    hist.SetStats(0)
    print "todraw ", branch_name, " cut ",cut
#    outplot = os.path.join(plotname, str(branch_name))
    txt = ROOT.TLatex(.65, .6, text)
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

    c1.SetGridx()
    c1.SetGridy()
    #c1.SetTickx()
    #c1.SetTicky()
    #h=F.Get("SliceTestAnalysis/MuonData");
    hist = ROOT.TH2F("hist","hist_title", xnbins, xmin, xmax, ynbins, ymin, ymax)
    
    todraw = branch_name_y +":"+branch_name_x
    ##cut = "muonpt>10"
    tree.Draw(todraw + ">> hist", cut, "colz");## plot hist with cut
    print "todraw ",todraw, " cut ",cut
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2018C")
    hist.SetStats(0)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetXaxis().SetTitleSize(0.04)
    hist.GetYaxis().SetTitleSize(0.04)
    hist.GetXaxis().CenterTitle()
    hist.GetYaxis().SetTitleOffset(1.2)
    #hist.SetStat(0)
    #outplot = os.path.join(plotname, str(branch_name))
    outplot = plotname
    txt = ROOT.TLatex(.15, .8, text)
    txt.SetNDC()
    txt.SetTextFont(42)
    txt.SetTextSize(.04)
    txt.Draw("same")

    c1.SaveAs(outplot + ".png")
    c1.SaveAs(outplot + ".pdf")



def plot_tree_2D_alignment(tree, chamber, layer, cut, xnbins, xmin, xmax, ynbins, ymin, ymax, text, plotname):

    c1=ROOT.TCanvas("c1","New Graph",0,0,1200,800);
    #h=F.Get("SliceTestAnalysis/MuonData");
    ##pad1
    branch_name_x="prop_localx_GE11[%d]"%(layer)
    #branch_name_x="(rechit_prop_dphi_GE11[%d]*rechit_r_GE11[%d])"%(layer,layer)
    #branch_name_x = "rechit_flippedStrip_GE11[%d]"%(layer)
    branch_name_y="(prop_localy_GE11[%d]+25.0*(roll_GE11[%d]-1))"%(layer, layer)
    #branch_name_y="(prop_localy_GE11[%d])"%(layer)
    xtitle = branch_name_x
    ytitle = branch_name_y
    #z = "(prop_localx_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer)
    #z = "(rechit_prop_dphi_GE11[%d]*rechit_r_GE11[%d])"%(layer, layer)
    #z = "(prop_localx_center_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer)
    z = "(prop_localx_center_GE11[%d]-rechit_alignedlocalx_GE11[%d])"%(layer, layer)

    
    hist_weight = ROOT.TH2F("hist_weight","hist_title", xnbins, xmin, xmax, ynbins, ymin, ymax)
    hist_entry = ROOT.TH2F("hist_entry","hist_title", xnbins, xmin, xmax, ynbins, ymin, ymax)
    hist = ROOT.TH2F("hist","hist_title", xnbins, xmin, xmax, ynbins, ymin, ymax)

    
    todraw = branch_name_y +":"+branch_name_x
    ##cut = "muonpt>10"
    tree.Draw(todraw + ">> hist_weight", "("+cut+")*"+z, "colz");## plot hist with cut
    tree.Draw(todraw + ">> hist_entry", "("+cut+")", "colz");## plot hist with cut
    #print "todraw ",todraw, " cut ","("+cut+")*"+z
    #hist.Divide(hist_entry)
    total_all = 0.0; events_all = 0;
    for xbin in xrange(xnbins):
        for ybin in xrange(ynbins):
            events = hist_entry.GetBinContent(xbin+1, ybin+1)
            events_all = events_all + events
            if events>0:
                total = hist_weight.GetBinContent(xbin+1, ybin+1)
                total_all = total + total_all
                average = total/events
                hist.SetBinContent(xbin+1, ybin+1, average)
            else:
                hist.SetBinContent(xbin+1, ybin+1, -999)

    print " total weight ", total_all, " total events ", events_all," correction ", total_all/events_all
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2018C")
    hist.SetStats(0)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetXaxis().SetTitleSize(0.04)
    hist.GetYaxis().SetTitleSize(0.04)
    hist.GetXaxis().CenterTitle()
    hist.GetYaxis().SetTitleOffset(1.2)
    zmax=4.0
    hist.SetMaximum(zmax*(1.0+1.0/40))
    hist.SetMinimum(zmax*(-1.0))
    #hist.SetStat(0)
    #outplot = os.path.join(plotname, str(branch_name))
    c1.Clear()
    outplot = plotname
    setcolortables()
    hist.Draw("colz")
    txt = ROOT.TLatex(.15, .8, text)
    txt.SetNDC()
    txt.SetTextFont(42)
    txt.SetTextSize(.04)
    txt.Draw("same")

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
chain = ROOT.TChain("SliceTestAnalysis/MuonData")
#chain.Add('/eos/uscms/store/user/mkhurana/GEMCSCBending_2018C/out_ana_10*.root')
#chain.Add("GEMCSCBending_2018C_v8.root")
chain.Add("/eos/uscms/store/user/tahuang/DoubleMuon/GEMCSCAan_Run2018D_Doublemuon_GEMon_320995-321475_20180817/180827_210513/0000/*root")
chain.Add("/eos/uscms/store/user/tahuang/DoubleMuon/GEMCSCAan_Run2018D_Doublemuon_GEMon_320995-321475_20180817/180827_210513/0001/*root")
#chain.Add("/eos/uscms/store/user/tahuang/SingleMuon/GEMCSCAan_Run2018D_singlemuon_GEMon_320995-321475_20180827/180827_210539/0000/*root")
#chain.Add("/eos/uscms/store/user/tahuang/SingleMuon/GEMCSCAan_Run2018D_singlemuon_GEMon_320995-321475_20180827/180827_210539/0001/*root")
plotdir = "GEMCSCBending_2018D_GEMhitEff_plots/"
os.system("mkdir -p "+plotdir)
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
	plotname = os.path.join(plotdir, "2018C_GEMCSCbending_rechit_prop_dR_ME11_CSClayer%d"%i)
	plot_tree_1D(chain, todraw, thiscut, todraw, 100, 0.0, 20.0, text,plotname)

    todraws_GE11 = "rechit_prop_dR_GE11"
    for i in range(0, 2):#2layers for GEM
        todraw = todraws_GE11+"[%d]"%i
        thiscut = cut + "&& has_GE11[%d]>0"%i
	plotname = os.path.join(plotdir, "2018C_GEMCSCbending_rechit_prop_dR_GE11_GEMlayer%d"%i)
	plot_tree_1D(chain, todraw, thiscut, todraw, 100, 0.0, 20.0, text,plotname)

    todraws_GE11 = "rechit_prop_dX_GE11"
    for i in range(0, 2):#2layers for GEM
        todraw = todraws_GE11+"[%d]"%i
        thiscut = cut + "&& has_GE11[%d]>0"%i
	plotname = os.path.join(plotdir, "2018C_GEMCSCbending_rechit_prop_dX_GE11_GEMlayer%d"%i)
	plot_tree_1D(chain, todraw, thiscut, todraw, 100, 0.0, 20.0, text,plotname)
    
    todraws_X = "rechit_phi_GE11"
    todraws_Y = "prop_phi_GE11"
    phimin = -2.0
    phimax = -0.8
    phibin = 60
    ##29: [-1.5, -1.3]
    for chamber in [27, 28,29, 30]:
    #for chamber in [1]:##all
    #for roll in xrange(8):
        for i in range(0, 2):#2layers for GEM
            todrawX = todraws_X+"[%d]"%i
            todrawY = todraws_Y+"[%d]"%i
            thiscut = cut + "&& has_GE11[%d]>0 && abs(%s)<4"%(i, todrawX) +" && chamber_GE11[%d] == %d"%(i, chamber)
            #thiscut = cut + "&& has_GE11[%d]>0 && abs(%s)<4"%(i, todrawX) 
            #thiscut = cut + "&& has_GE11[%d]>0 && abs(%s)<4"%(i, todrawX) + " && roll_GE11[%d] == %d"%(i, roll) 
            plotname = os.path.join(plotdir, "2018C_GEMCSCbending_rechit_prop_phi_2D_GE11_GEMlayer%d_chamber%d"%(i, chamber))
            #plotname = os.path.join(plotdir, "2018C_GEMCSCbending_rechit_prop_phi_2D_GE11_GEMlayer%d_roll%d"%(i, roll))
            plot_tree_2D(chain, todrawX, todrawY, thiscut, "Rechit global phi", phibin, phimin,phimax, "Muon propagated phi", phibin, phimin, phimax,text, plotname)
    

    todraws_seg = "cscseg_prop_dR_st"
    for i in range(0, 4):#4 station CSCs 
        todraw = todraws_seg+"[%d]"%i
        thiscut = cut + " && has_cscseg_st[%d]>0"%i
	plotname = os.path.join(plotdir, "2018C_GEMCSCbending_cscseg_prop_dR_st%d"%i)
        #plot_tree_1D(chain, todraw, thiscut, todraw, 100, 0.0, 20.0, text,plotname)

#plotdeltaR(chain, "has_TightID && muonpt>10","muon p_{T}> 30, tight ID", plotdir)

def plotdPhiGEMMuon(chain, cut, text, plotdir):
    todraw = "rechit_prop_dphi_GE11"
    #for chamber in [27, 28,29, 30]:
    for chamber in [0]:

        for i in range(0, 2):#2layers for GEM
            todrawX = todraw+"[%d]"%i
            #thiscut = cut + "&& has_GE11[%d]>0 && abs(%s)<4"%(i, todrawX) +" && chamber_GE11[%d] == %d"%(i, chamber)
            thiscut = cut + "&& has_GE11[%d]>0 && abs(%s)<4"%(i, todrawX) 
            plotname = os.path.join(plotdir, "2018C_GEMCSCbending_rechit_prop_dphi_GE11_GEMlayer%d_chamber%d"%(i, chamber))
            plot_tree_1D(chain, todraw, thiscut, "#Delta phi between GEM rechit and propagated muon", 100, -0.10, 0.10, text,plotname)
#plotdPhiGEMMuon(chain, "has_TightID", "tight ID", plotdir)


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

    #for i in range(0, 6):
    #    todrawX_strip = "rechit_centralStrip_ME11"
    #    todrawY_strip = "rechit_nStrips_ME11"
    #    thiscut = cut + " && has_ME11[%d]>0 && rechit_prop_dR_ME11[%d] < 5.0"%(i, i)
    #    plotname = os.path.join(plotdir, "2018C_GEMCSCbending_rechit_centralstrip_nstrips_ME11layer%d"%i)
    #    plot_tree_2D(chain, todrawX_strip, todrawY_strip, thiscut, "CSC Rechit centralStrip", , -600.0, 600.0,  "CSC Rechit Y", 600, -600.0, 600.0,text, plotname)

    #todrawXlist = ["rechit_centralStrip_ME11","rechit_hotWire_ME11", "rechit_WG_ME11"]

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
    todrawlist = ["rechit_clusterSize_GE11"]
    xbins = [[20, 0,20]]
    xtitles = ["cluster size, GE11"]
    for itodraw, todraw in enumerate(todrawlist):
        for chamber in [27, 28, 29, 30]:
            for i in range(0, 2):
                thistodraw = todrawlist+"[%d]"%i
                thiscut = cut +" && has_GE11[%d]>0 && rechit_prop_dX_GE11[%d] < 2.0 && chamber_GE11[%d]==%d"%(i,i, i, chamber)
                plot_tree_1D(chain, thistodraw, thiscut, xtiles[itodraw], xbins[itodraw][0], xbins[itodraw][1], xbins[itodraw][2], text, plotname)

def plotGEMdXVsRoll(chain, cut, text, plotdir):
    todrawX_0 = "rechit_prop_dX_GE11"
    todrawY_0 = "roll_GE11"
    xbin=100; xmin=-10; xmax=10
    ybin=8; ymin=1; ymax=9
    for ilayer in range(0, 2):
        todrawX = todrawX_0 + "[%d]"%ilayer
        todrawY = todrawY_0 +  "[%d]"%ilayer
        thiscut = cut+" && has_GE11[%d]>0 "%(ilayer)
        namesuffix = todrawX.split('[')[0]
        thistext = text+" layer %d"%(ilayer+1)
        plotname =  os.path.join(plotdir, "2018C_GEMCSCbending_%s_vsroll_gemlayer%d"%(namesuffix, ilayer))
        plot_tree_2D(chain, todrawX, todrawY, thiscut, "#Delta X between GEM rechit and propagated muon", xbin, xmin, xmax,  "roll number", ybin, ymin, ymax, thistext, plotname)



#plotGEMdXVsRoll(chain, "has_TightID && muonpt>25", "muon tight ID, p_{T}>25", plotdir)

#plotGEMHits(chain, "has_TightID && muonpt>10", "muon p_{T}> 10, tight ID",plotdir)
def plotGEMRechitVsMuon(chain, cut, text, plotdir):
    todrawX_gem = "rechit_phi_GE11"
    todrawY_muon = "prop_phi_GE11"
    for ich in xrange(27, 31):
        phimin = -1.850 + (ich-27)*0.175
        phimax = -1.650 + (ich-27)*0.175
        phibin = 60
        for ilayer in range(0, 2):
            todrawX = todrawX_gem + "[%d]"%ilayer
            todrawY = todrawY_muon +  "[%d]"%ilayer
            thiscut = cut+" && has_GE11[%d]>0 && chamber_GE11[%d]==%d"%(ilayer, ilayer, ich)
            namesuffix = todrawY.split('[')[0]
            thistext = text+" GEM chamber %d, layer %d"%(ich, ilayer+1)
            plotname =  os.path.join(plotdir, "2018C_GEMCSCbending_globalphi_GE11_muonprop_%s_chamber%d_gemlayer%d"%(namesuffix,ich, ilayer))
            plot_tree_2D(chain, todrawX, todrawY, thiscut, "global phi, GEM Rechit", phibin, phimin, phimax,  "global phi, Propagated Muon", phibin, phimin, phimax, thistext, plotname)


#plotGEMRechitVsMuon(chain, "has_TightID && muonpt>25"," tight ID,muon p_{T}>25 " , plotdir)

def plotGEMPhiVsCSCPhi(chain, cut, text, plotdir):
    todrawX_gem = "rechit_phi_GE11"
    todrawY_CSC = ["cscseg_phi_st[0]", "rechit_phi_ME11[2]","rechit_L1phi_ME11[2]"]
    cuts = [cut+"&& has_cscseg_st[0]>0", cut+"&& has_ME11[2]>0", cut+"&& has_ME11[2]>0"]
    for icsc, todrawY in enumerate(todrawY_CSC):
        for ilayer in range(0, 2):
            todrawX = todrawX_gem + "[%d]"%ilayer
            thiscut = cuts[icsc]+" && has_GE11[%d]>0"%ilayer
            namesuffix = todrawY.split('[')[0]
            plotname =  os.path.join(plotdir, "2018C_GEMCSCbending_globalphi_GE11_ME11_%s_gemlayer%d"%(namesuffix, ilayer))
            phimin = -2.0
            phimax = -0.8
            phibin = 120
            plot_tree_2D(chain, todrawX, todrawY, thiscut, "global phi, GE11", phibin, phimin, phimax,  "global phi, ME11", phibin, phimin, phimax, text, plotname)


#plotGEMPhiVsCSCPhi(chain, "has_TightID && muonpt>30", "muon p_{T}> 30, tight ID", plotdir)

def plotdeltaPhi(chain, cut, text, plotdir):
    todrawlist  = ["dphi_CSCSeg_GE11Rechit", "dphi_keyCSCRechit_GE11Rechit", "dphi_propCSC_propGE11"]
    for i, todraw in enumerate(todrawlist):
	for layer in range(0,2):
	    todraw_dphi = todraw + "[%d]"%layer
	    plotname = os.path.join(plotdir, "2018C_GEMCSCbending_%s_gemlayer%d"%(todraw, layer))
	    thiscut = cut + " &&  has_GE11[%d]>0 && has_propGE11[%d]>0 && has_ME11[2]>0 "%(layer, layer)
	    plot_tree_1D(chain, todraw, thiscut, todraw_dphi, 60, -0.30, 0.3, text, plotname)

#plotdeltaPhi(chain, "has_TightID", "tight ID",plotdir)
def plotdeltaPhiVspt(chain, cut, text, plotdir):
    #todrawlist  = ["dphi_CSCSeg_GE11Rechit", "dphi_keyCSCRechit_GE11Rechit", "dphi_propCSC_propGE11"]
    #todrawlist  = ["dphi_keyCSCRechit_GE11Rechit", "dphi_keyCSCRechit_alignedGE11Rechit"]
    todrawlist = ["dphi_CSCSeg_GE11Rechit","dphi_CSCSeg_alignedGE11Rechit"]
    todrawY= "muonpt"
    xbin = 90; xmin=-0.045; xmax = 0.045
    ybin= 14; ymin=5.0; ymax=75.0
    for i, todraw in enumerate(todrawlist):
        for ich in range(27, 31):
            for layer in range(0,2):
                todraw_dphi = todraw + "[%d]"%layer
                plotname = os.path.join(plotdir, "2018C_GEMCSCbending_%s_gemchamber%d_layer%d_drcut"%(todraw, ich, layer))
                #dRcut = "&& rechit_prop_dR_ME11[2]<5.0 && abs(rechit_prop_dphi_GE11[0])<.02"
                dRcut = "&& cscseg_prop_dR_st[0]< 2.0 && abs(rechit_prop_dphi_GE11[0])<.02"
                #thiscut = cut + " &&  has_GE11[%d]>0 && has_propGE11[%d]>0 && has_ME11[2]>0 "%(layer, layer) +" && chamber_GE11[%d]==%d"%(layer, ich) + dRcut
                thiscut = cut + " &&  has_GE11[%d]>0 && has_propGE11[%d]>0 && has_cscseg_st[0]>0 "%(layer, layer) +" && chamber_GE11[%d]==%d"%(layer, ich) + dRcut
                thistext = text+" GEM chamber %d, layer %d"%(ich, layer+1)
                plot_tree_2D(chain, todraw_dphi, todrawY, thiscut, "GEM-CSC bending angle", xbin, xmin, xmax,  "Muon p_{T} GeV", ybin, ymin, ymax, thistext, plotname)

#plotdeltaPhi(chain, "has_TightID", "tight ID",plotdir)
#plotdeltaPhiVspt(chain, "has_TightID ", "muon tight ID", plotdir)

def plotGEMalignment(chain, cut, text, plotdir):
    xbin = 40; xmin=-24.0; xmax = 24.0
    #xbin =384/6; xmin=0; xmax = 384
    ybin= 15*8; ymin=-10.0; ymax= 25*7.0+15.0
    #ybin= 20; ymin=-10.0; ymax= 10.0
    for ich in range(27, 31):
        for layer in range(0,2):
            plotname = os.path.join(plotdir, "2018C_GEMCSCbending_GEMalignment_gemchamber%d_layer%d_drcut_alignedlocalx"%( ich, layer))
            dRcut = "&& abs(rechit_prop_dphi_GE11[%d])<.02"%(layer)
            thiscut = cut + " &&  has_GE11[%d]>0 && has_propGE11[%d]>0"%(layer, layer) +" && chamber_GE11[%d]==%d"%(layer, ich)+dRcut
            thistext = text+" GEM chamber %d, layer %d"%(ich, layer+1)
            plot_tree_2D_alignment(chain, ich, layer, thiscut,  xbin, xmin, xmax, ybin, ymin, ymax, thistext, plotname)

#plotGEMalignment(chain, "has_MediumID && muonpt>25", "medium ID",plotdir)

ptbin = [10.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 80.0, 100.0, 150.0, 200.0]
myptbin = np.asarray(ptbin)
def plotGEMHitEff_ptbin(chain, dencut, text, plotdir):
    thisplotdir = os.path.join(plotdir, "GEMRechit_Eff_ptbin_")
    plotGEMHitEff(chain, "muonpt", dencut,  myptbin, "Muon p_{T}^{reco}", text, thisplotdir)

plotGEMHitEff_ptbin(chain, "has_TightID", "Muon tight ID", plotdir)
plotGEMHitEff_phi(chain,  "has_TightID && muonpt>=25", "Muon tight ID, p_{T}^{reco}>25", os.path.join(plotdir, "GEMRechit_Eff_phibin_pt25_"))
