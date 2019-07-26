import ROOT
import os
import time

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetStatW(0.15)
ROOT.gStyle.SetStatH(0.25)

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

ROOT.gStyle.SetPaintTextFormat(".4f")

ROOT.gStyle.SetMarkerStyle(1)

import numpy as np

color = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2, ROOT.kMagenta+2,ROOT.kCyan+2 ]
marker = [20,21,22,23,33]
def setcolortables():
     red = np.array([ 0.0, 1.0, 1.0], dtype=np.double)
     green = np.array([ 0.0, 1.0, 0.0], dtype=np.double)
     blue = np.array([ 1.0, 1.0, 0.0], dtype=np.double)
     stop = np.array([ 0.0, 0.5, 1.0], dtype=np.double)
     #print "red ",red
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
    b1.GetYaxis().SetRangeUser(-0.40,1.05)##GEM
    #b1.GetYaxis().SetRangeUser(0.9,1.01)##CSC
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
    c1.SetLogx()

    b1.SetStats(0)
    b1.Draw()
    color = [2,4,3,5,6,7,8,9,1]
    color = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2, ROOT.kOrange, ROOT.kMagenta+2,ROOT.kCyan+2, 5,6,7,8,9, ROOT.kBlack]
    #marker = [20,21, 22, 23,, 24, 25]
    marker = [20, 24, 21, 25, 22, 26, 23, 27, 33, 28, 30]
    legend = ROOT.TLegend(0.65,0.16,0.83,0.20+0.04*len(Teffs))
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

    tex = ROOT.TLatex(0.2,0.27,"%s"%txt)
    #tex = ROOT.TLatex(0.45,0.57,"#splitline{%s}{%d%% eff at %d [GeV]}"%(txt,fractionToKeep,pt))
    #tex = ROOT.TLatex(0.45,0.57,"#splitline{%s}{check the sign of #Delta Y_{12} and #Delta Y_{23}}"%(txt))
    tex.SetTextSize(0.04)
    tex.SetTextFont(62)
    tex.SetNDC()
    tex.Draw("same")
    #c1.Update()
    c1.SaveAs("%s.png"%(picname))
    c1.SaveAs("%s.pdf"%(picname))
    #c1.SaveAs("%s.C"%(picname))
	

def plotGEMHitEff(chain, todraw, dencut, xbins,xtitle, txt, plotdir):

    ytitle = "GEM hit efficiency"
    Teff_all = []
    leg_all = []
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
            Teff_all.append(getTefficiency(chain, todraw, thisdencut, thisnumcut, xbins))
            leg_all.append("Ch%d, layer %d"%(ch, layer+1))

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

    header_all = ""
    picname_all = plotdir+"all4chambers_layers"
    makeEffplot(Teff_all, xtitle, ytitle, leg_all, header_all, txt, picname_all)


###
def plotGEMHitEff_phi(chain, dencut, txt, plotdir):
    ytitle = "GEM hit efficiency"
    xtitle = "Muon global #phi at GE11"
    xtitle = "Muon strip number at GE11"
    Teff_all = []
    leg_all = []
    for ch in [27, 28, 29, 30]:
        Teff_layers = []
        leg_layers = []
        #phimin = -1.850 + (ch-27)*0.175
        #phimax = -1.650 + (ch-27)*0.175
        #phibin = 20
        phimax = 384.0; phimin= 0.0; phibin= 24
        phi_step = abs(phimax-phimin)/phibin
        phibin_x = np.arange(phimin, phimax, phi_step)
        ##important!!!
        phibin_x = np.append(phibin_x, phimax)
        #print "phibin_x ",phibin_x
        for layer in [0, 1]:
            #todraw = "prop_phi_GE11[%d]"%layer
            todraw = "prop_strip_GE11[%d]"%layer
            #dRcut = "&& abs(rechit_prop_dphi_GE11[%d])<.02"%(layer)
            dRcut = "&& abs(rechit_prop_aligneddphi_GE11[%d])<.02"%(layer)
            layercut = "has_propGE11[%d] && chamber_propGE11[%d] == %d && has_cscseg_st[0] && cscseg_chamber_st[0]==%d"%(layer, layer, ch, ch)## 
            thisdencut = dencut + " && "+ layercut
            thisnumcut = dencut + " && "+ layercut+"&& has_GE11[%d] && chamber_GE11[%d] == %d"%(layer, layer, ch)  +dRcut
            Teff_layers.append(getTefficiency(chain, todraw, thisdencut, thisnumcut, phibin_x))
            leg_layers.append("layer %d"%(layer+1))
            Teff_all.append(getTefficiency(chain, todraw, thisdencut, thisnumcut, phibin_x))
            leg_all.append("Ch%d, layer %d"%(ch, layer+1))
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
            picname_roll = plotdir + "ch%d_layer%d_rolls_dphi02"%(ch, layer)
            makeEffplot(Teff_rolls, xtitle, ytitle, leg_rolls, header_roll, txt, picname_roll)
        header_layer = "GEM %d"%(ch)
        picname_layer = plotdir+"ch%d_layers_dphi02"%(ch)
        makeEffplot(Teff_layers, xtitle, ytitle, leg_layers, header_layer, txt, picname_layer)

    header_all = ""
    picname_all = plotdir+"all4chambers_layers"
    print " Teff_all ",Teff_all
    makeEffplot(Teff_all, xtitle, ytitle, leg_all, header_all, txt, picname_all)
    

###
def plotME11CSCHitEff(chain, xtodraw, dencut, nbins, xmin, xmax,  xtitle, txt, plotdir):
    ytitle = "CSC hit efficiency, ME11"
    
    Teff_layers = []
    leg_layers = []
    step = abs(xmax-xmin)/nbins
    bin_x = np.arange(xmin, xmax, step)
    ##important!!!
    bin_x = np.append(bin_x, xmax)
    #print "bin_x ",bin_x
    for layer in xrange(6):
        #todraw = "prop_phi_GE11[%d]"%layer
        todraw = xtodraw +"[%d]"%layer
        dRcut = "&& abs(rechit_prop_dR_ME11[%d])< 5"%(layer)
        layercut = "has_propME11[%d]>0 "%(layer)## 
        thisdencut = dencut + " && "+ layercut
        thisnumcut = dencut + " && "+ layercut +dRcut
        Teff_layers.append(getTefficiency(chain, todraw, thisdencut, thisnumcut, bin_x))
        leg_layers.append("layer %d"%(layer+1))
    header_layer = "ME11"
    picname_layer = plotdir+"layers_dR05"
    makeEffplot(Teff_layers, xtitle, ytitle, leg_layers, header_layer, txt, picname_layer)

###
def plotCSCSegmentEff(chain, xtodraw, dencut, nbins, xmin, xmax,  xtitle, txt, plotdir):
    ytitle = "CSC Segment efficiency, MEX1"
    
    Teff_st = []
    leg_st = []
    step = abs(xmax-xmin)/nbins
    bin_x = np.arange(xmin, xmax, step)
    ##important!!!
    bin_x = np.append(bin_x, xmax)
    #print "bin_x ",bin_x
    for st in xrange(4):
        #todraw = "prop_phi_GE11[%d]"%layer
        todraw = xtodraw +"[%d]"%st
        dRcut = "&& abs(cscseg_prop_dR_st[%d])< 2 "%(st)
        stationcut = "has_prop_st[%d]>0 && (prop_ring_st[%d]==1 || prop_ring_st[%d]==4) "%(st, st, st)## 
        thisdencut = dencut + " && "+ stationcut
        thisnumcut = dencut + " && "+ stationcut +dRcut+" && has_cscseg_st[%d]>0"%(st)
        Teff_st.append(getTefficiency(chain, todraw, thisdencut, thisnumcut, bin_x))
        leg_st.append("ME%d/1"%(st+1))
    header_st = "MEX1"
    picname_st = plotdir+"MEX1_dR2"
    makeEffplot(Teff_st, xtitle, ytitle, leg_st, header_st, txt, picname_st)



def plot_tree_1D(tree, branch_name, cut, xtitle, nbins, xmin, xmax, text, plotname):

   
    c1=ROOT.TCanvas("c1","New Graph",0,0, 800,600);
    c1.SetGridx()
    c1.SetGridy()
    #c1.SetTickx()
    #c1.SetTicky()
    #h=F.Get("SliceTestAnalysis/MuonData");
    hist = ROOT.TH1F("hist","hist_title", nbins, xmin, xmax)
    
    ##cut = "muonpt>10"
    tree.Draw(branch_name + ">> hist", cut);## plot hist with cut
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*16+"data, Run2018C")
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle("Normalized to unity")
    hist.SetStats(0)
    print "todraw ", branch_name, " cut ",cut
    hist.Scale(1.0/hist.Integral())
    hist.Draw("hist")
#    outplot = os.path.join(plotname, str(branch_name))
    txt = ROOT.TLatex(.15, .8, text)
    txt.SetNDC()
    txt.SetTextFont(42)
    txt.SetTextFont(42)
    txt.SetTextSize(.04)
    txt.Draw("same")
    
    #outplot = os.path.join(os.getcwd(), str(plotname))
    outplot = plotname
    c1.SaveAs(outplot + ".png")
    c1.SaveAs(outplot + ".pdf")


def plot_tree_1D_multiple(tree, branch_names, cuts, legs, xtitle, nbins, xmin, xmax, text, plotname):

   
    c1=ROOT.TCanvas("c1","New Graph",0,0, 800,600);
    #h=F.Get("SliceTestAnalysis/MuonData");
    histlist = []
    hs = ROOT.THStack("hs",  " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*16+"data, Run2018")
    legend = ROOT.TLegend(0.55,0.67,0.91,0.7+0.04*len(cuts))
    legend.SetFillColor(ROOT.kWhite)

    for i,branch_name in enumerate(branch_names):
        histlist.append( ROOT.TH1F("hist%d"%i,"hist_title", nbins, xmin, xmax))
        
        ##cut = "muonpt>10"
        tree.Draw(branch_name + ">> hist%d"%i, cuts[i]);## plot hist with cut
        histlist[-1].SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*16+"data, Run2018")
        histlist[-1].GetXaxis().SetTitle(xtitle)
        histlist[-1].SetStats(0)
        histlist[-1].SetLineColor(color[i])
        histlist[-1].SetLineWidth(2)
        hs.Add(histlist[-1])
        legend.AddEntry(histlist[-1], legs[i], "l")
        print "todraw ", branch_name, " cut ",cuts[i]
        #hist.Scale(1.0/hist.Integral())
        #hist.Draw("hist")
#    outplot = os.path.join(plotname, str(branch_name))
    hs.Draw("nostackhist")
    legend.Draw("same")
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

    #c1.SetGridx()
    #c1.SetGridy()
    #c1.SetTickx()
    #c1.SetTicky()
    #h=F.Get("SliceTestAnalysis/MuonData");
    hist = ROOT.TH2F("hist","hist_title", xnbins, xmin, xmax, ynbins, ymin, ymax)
    
    todraw = branch_name_y +":"+branch_name_x
    ##cut = "muonpt>10"
    tree.Draw(todraw + ">> hist", cut, "colz");## plot hist with cut
    print "todraw ",todraw, " cut ",cut
    #hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2018C")
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"Run2,MC")
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
    #txt.Draw("same")

    c1.SaveAs(outplot + ".png")
    c1.SaveAs(outplot + ".pdf")



def plot_tree_2D_alignment(tree, chamber, layer, cut, branch_name_x, branch_name_y,z, xnbins, xmin, xmax, ynbins, ymin, ymax, text, plotname):

    c1=ROOT.TCanvas("c1","New Graph",0,0,1200,800);
    #h=F.Get("SliceTestAnalysis/MuonData");
    ##pad1
    #branch_name_x="prop_localx_GE11[%d]"%(layer)
    #branch_name_x="(rechit_prop_dphi_GE11[%d]*rechit_r_GE11[%d])"%(layer,layer)
    #branch_name_x = "rechit_flippedStrip_GE11[%d]"%(layer)
    #branch_name_y="(prop_localy_GE11[%d]+25.0*(8-roll_GE11[%d]))"%(layer, layer)
    #branch_name_y="(prop_localy_GE11[%d])"%(layer)
    xtitle = branch_name_x
    ytitle = branch_name_y
    #z = "(prop_localx_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer)
    #z = "(rechit_prop_dphi_GE11[%d]*rechit_r_GE11[%d])"%(layer, layer)
    #z = "(prop_localx_center_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer)
    #z = "(prop_localx_center_GE11[%d]-rechit_alignedlocalx_GE11[%d])"%(layer, layer)
    #z = "(rechit_prop_dX_GE11_foralignment[%d])"%layer
    #z = "TMath::Cos(rechit_stripangle_GE11[%d])*(prop_localx_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer, layer)
    #z = "(rechit_propinner_dX_GE11_foralignment[%d])"%layer
    #z = "TMath::Cos(rechit_stripangle_GE11[%d])*(propinner_localx_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer, layer)

    
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

    print "x ",branch_name_x," y ",branch_name_y," z ",z
    print " total weight ", total_all, " total events ", events_all," correction ", total_all/events_all
    #hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"data, 2018C")
    hist.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"Phase-2 Simulation")
    hist.SetStats(0)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetXaxis().SetTitleSize(0.04)
    hist.GetYaxis().SetTitleSize(0.04)
    hist.GetXaxis().CenterTitle()
    hist.GetYaxis().SetTitleOffset(1.2)
    zmax=2.0
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

    c1.SaveAs(outplot + ".C")
    c1.SaveAs(outplot + ".png")
    c1.SaveAs(outplot + ".pdf")

    c2=ROOT.TCanvas("c2","New Graph",0,0,1200,800);
    ROOT.gStyle.SetPaintTextFormat("4.0f")
    hist_entry.SetTitle( " #scale[1.4]{#font[61]{CMS}} #font[42]{Internal} "+"  "*24+"Phase-2 Simulation")
    hist_entry.SetStats(0)
    hist_entry.GetXaxis().SetTitle(xtitle)
    hist_entry.GetYaxis().SetTitle(ytitle)
    hist_entry.GetXaxis().SetTitleSize(0.04)
    hist_entry.GetYaxis().SetTitleSize(0.04)
    hist_entry.GetXaxis().CenterTitle()
    hist_entry.GetYaxis().SetTitleOffset(1.2)
    hist_entry.RebinX(4)
    hist_entry.RebinY(4)
    hist_entry.Draw("colztext")
    txt.Draw("same")

    c2.SaveAs(outplot + "_occupancy.C")
    c2.SaveAs(outplot + "_occupancy.png")
    c2.SaveAs(outplot + "_occupancy.pdf")


def plot_residual_1D(tree, cut, xtitle, nbins, xmin, xmax, text, plotname):

   
    color = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2, ROOT.kOrange, ROOT.kMagenta+2,ROOT.kCyan+2, 5,6,7,8,9, ROOT.kBlack]
    doFit = True
    #for ch in [27, 28, 29, 30]
    for ch in [28, 29]:
        for layer in range(0, 2):
            #c1=ROOT.TCanvas("c1","Alignment of GEM ch%d layer%d"%(ch, layer+1),0,0, 800,600);
            c1=ROOT.TCanvas("c1","Alignment of GEM ch%d layer%d"%(ch, layer+1),0,0, 800,400);
            c1.Clear()
            c1.Divide(4, 2)
            ## standalone muon
            #todraw = "rechit_propinner_dX_GE11_foralignment[%d]"%layer
            todraw = "(rechit_prop_RdPhi_GE11[%d])"%layer
            #todraw = "(prop_localx_center_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer)
            ## inner track
            #todraw = "(propinner_localx_center_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer)
            #layercut = "has_propGE11[%d]>0 && chamber_propGE11[%d] == %d "%(layer, layer, ch)## 
	    ##MC case
            layercut = "has_propGE11[%d]>0 && chamber_propGE11[%d]%%2 == %d "%(layer, layer, ch%2)## 
            #boundarycut = "abs(prop_y_center_GE11[%d])<15.0"
            boundarycut = "&& abs(prop_localy_GE11[%d])<6.0 && abs(prop_localx_center_GE11[%d])<15.0"%(layer, layer)
            dRcut = "&& abs(rechit_prop_dphi_GE11[%d])<.02 && rechit_clusterSize_GE11[%d]<=6"%(layer, layer)
            hs_list = []
            legend_list = []
            for roll in range(1, 9):
                c1.cd(roll)

                detidcut = layercut +"&& roll_propGE11[%d] == %d"%(layer, roll)
                #thiscut = cut +"&& "+detidcut + dRcut
                thiscut = cut +"&& "+detidcut+boundarycut
                hs_list.append( ROOT.THStack("hs_roll%d"%roll, "GEM ch%d layer%d roll%d"%(ch, layer+1, roll)) )
                legend_list.append( ROOT.TLegend(0.63,0.7,1.0,0.8))
                legend_list[roll -1].SetFillColor(ROOT.kWhite)
                legend_list[roll-1].SetTextFont(42)
                legend_list[roll-1].SetTextSize(.035)
                #legend.SetHeader("%s"%legheader)
                hist_list = []
                fit_list = []
                #for vfat in range(0, 3):
                for vfat in range(0, 1):
                    hist_list.append( ROOT.TH1F("hist_eta%d_vfat%d"%(roll, vfat), "GEM ch%d layer%d roll%d VFAT%d"%(ch, layer+1, roll, vfat), nbins, xmin, xmax) )
                    vfatcut_1 = "rechit_flippedStrip_GE11[%d]>=%d && rechit_flippedStrip_GE11[%d]< %d"%(layer, vfat*128, layer, (vfat+1)*128)
                    #tree.Draw(todraw +" >> hist_eta%d_vfat%d"%(roll, vfat), thiscut +" && "+vfatcut_1)
                    tree.Draw(todraw +" >> hist_eta%d_vfat%d"%(roll, vfat), thiscut)
                    #hist_list[vfat].Scale(1.0/hist_list[vfat].Integral())
		    if doFit:
			hist_list[vfat].Fit("gaus","S","",-1.0, 1.0)
			fit_list.append(hist_list[vfat].GetFunction("gaus"))
			fit_list[vfat].SetLineColor(ROOT.kRed)
			mean = fit_list[vfat].GetParameter(1)
			std =  fit_list[vfat].GetParameter(2)
			meanerr = fit_list[vfat].GetParError(1)
			stderr =  fit_list[vfat].GetParError(2)
			legend_list[roll-1].AddEntry(hist_list[vfat], "#splitline{#mu: %.3f +/- %.3f}{#sigma: %.3f +/- %.3f}"%(mean,meanerr, std, stderr),'')
                    else:
			mean = hist_list[vfat].GetMean()
			std =  hist_list[vfat].GetStdDev()
			legend_list[roll-1].AddEntry(hist_list[vfat], "#splitline{#mu: %.3f}{#sigma: %.3f}"%(mean, std),'')
			#meanerr = hist_list[vfat].GetParError(1)
			#stderr =  hist_list[vfat].GetParError(2)
                    #mean = 0.0; std = 1.0
                    #legend_list[roll-1].AddEntry(hist_list[vfat], "mean: %.2f, std:%.1f"%(mean, std))
                    legend_list[roll-1].SetTextColor(ROOT.kRed)
                    hs_list[roll-1].Add(hist_list[vfat])
                    #hist_list[vfat].SetLineColor(color[vfat])
                    #fit_list[vfat].SetLineColor(color[vfat])
                    hist_list[vfat].SetLineColor(ROOT.kBlack)
                #hs_list[roll-1].Draw("nostacke")
                hs_list[roll-1].Draw("nostackhist")
                legend_list[roll-1].Draw("same")
		#if doFit:
		#    for fit in fit_list:
		#	fit.Draw("same")
                hs_list[roll-1].GetHistogram().GetXaxis().SetTitle("residual [cm]")
                c1.Update()
            c1.cd()
            txt = ROOT.TLatex(.5, .5, text)
            txt.SetNDC()
            txt.SetTextFont(42)
            txt.SetTextSize(.035)
            txt.Draw("same")

            #txt0 = ROOT.TLatex(.15, .93, legs)
            #txt0.SetNDC()
            #txt0.SetTextFont(42)
            #txt0.SetTextSize(.04)
            #txt0.Draw("same")
            
            picname_layer = plotname+"_ch%d_layer%d_NOdphicutv3_boundary"%(ch, layer)
            c1.SaveAs(picname_layer+ ".png")
            c1.SaveAs(picname_layer+ ".pdf")


def plot_residual_1D_v2(tree, cut, xtitle, nbins, xmin, xmax, text, plotname):

   
    ROOT.gStyle.SetOptStat(111111)
    ROOT.gStyle.SetOptFit(1111)
    color = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2, ROOT.kOrange, ROOT.kMagenta+2,ROOT.kCyan+2, 5,6,7,8,9, ROOT.kBlack]
    totalvfat = 6
    nstrip = 384/totalvfat
    alignment_localXshift = {"ch27_layer1":-0.152,  "ch27_layer2":-0.145, "ch28_layer1": 0.1382, "ch28_layer2":0.1345, "ch29_layer1":-0.2737, "ch29_layer2":-0.2939,"ch30_layer1":0.387, "ch30_layer2":0.377}
    #alignment_localXshift = {"ch27_layer1":0.0,  "ch27_layer2":0.0, "ch28_layer1": 0.0, "ch28_layer2": 0.0, "ch29_layer1": 0.0, "ch29_layer2": 0.0, "ch30_layer1":0.0, "ch30_layer2":0.0}
    #for ch in [27, 28, 29, 30]:
    #for ch in [27,30]:
    for ch in [28, 29]:
        for layer in range(0, 2):
            hist_rotation_list = []
            for vfat in range(0, totalvfat):
                hist_rotation_list.append( ROOT.TH1F("hist_rotationfit_GEM_ch%d_layer%d_vfat%d"%(ch, layer+1, vfat), "GEM ch%d layer%d VFAT%d"%(ch, layer+1,  vfat), 8, -4.0, 4.0) )
            hist_rotation_list_v2 = []
            for roll in range(1, 9):
                hist_rotation_list_v2.append( ROOT.TH1F("hist_rotationfit_v2_GEM_ch%d_layer%d_roll%d"%(ch, layer+1, roll), "GEM ch%d layer%d Roll%d"%(ch, layer+1,  roll), totalvfat, -1.0*totalvfat, 1.0*totalvfat) )

            residual_2D = ROOT.TH2F("residual_2D","residual_2D", totalvfat, 0.0, totalvfat, 8, 1.0, 9.0)
            todraw = "(prop_localx_center_GE11[%d]-rechit_localx_GE11[%d] - %f)"%(layer, layer, alignment_localXshift["ch%d_layer%d"%(ch, layer+1)])
            #todraw = "(prop_localx_center_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer)
            layercut = "has_propGE11[%d] && chamber_propGE11[%d] == %d "%(layer, layer, ch)## 
            #dRcut = "&& abs(rechit_prop_dphi_GE11[%d])<.02"%(layer)
            dRcut = "&& abs(rechit_prop_dphi_GE11[%d])<.02 && rechit_clusterSize_GE11[%d]<=6"%(layer, layer)
            hs_list = []
            c1=ROOT.TCanvas("c1","Alignment of GEM ch%d layer%d"%(ch, layer+1),0,0, 900,1200);
            #c1.Clear()
            c1.Divide(totalvfat, 8)
            hs_list = []
            legend_list = []
            hist_list = []
            fit_list = []
            txt_list = []
            localX_shift = 0.0; nVfat = 0
            for roll in range(1, 9):
                detidcut = layercut +"&& roll_propGE11[%d] == %d"%(layer, roll)
                thiscut = cut +"&& "+detidcut + dRcut
                #hs_list.append( ROOT.THStack("hs_roll%d"%roll, "GEM ch%d layer%d roll%d"%(ch, layer+1, roll)) )
                #legend_list.append( ROOT.TLegend(0.63,0.7,0.91,0.8))
                #legend_list[roll -1].SetFillColor(ROOT.kWhite)
                #legend_list[roll-1].SetTextFont(42)
                #legend_list[roll-1].SetTextSize(.035)
                #legend.SetHeader("%s"%legheader)
                for vfat in range(0, totalvfat):
                    c1.cd((roll-1)*totalvfat+vfat+1)
                    #hist_list.append( ROOT.TH1F("hist_eta%d_vfat%d"%(roll, vfat),"hist_eta%d_vfat%d"%(roll, vfat), nbins, xmin, xmax) )
                    hist_list.append( ROOT.TH1F("hist_eta%d_vfat%d"%(roll, vfat), "GEM ch%d layer%d roll%d VFAT%d"%(ch, layer+1, roll, vfat), nbins, xmin, xmax) )
                    minstrip = vfat*nstrip;  maxstrip = (vfat+1)*nstrip 
                    vfatcut_1 = "rechit_flippedStrip_GE11[%d]>=%d && rechit_flippedStrip_GE11[%d]< %d"%(layer, minstrip, layer, maxstrip)
                    tree.Draw(todraw +" >> hist_eta%d_vfat%d"%(roll, vfat), thiscut +" && "+vfatcut_1)
                    #hist_list[roll*3+vfat].SetLineColor(color[vfat])
                    #hist_list[roll*3+vfat].Scale(1.0/hist_list[roll*3+vfat].Integral())
                    hist_list[(roll-1)*totalvfat+vfat].Fit("gaus","S","", -1.0, 1.0)
                    if ch == 30:
                        hist_list[(roll-1)*totalvfat+vfat].Fit("gaus","S","", -1.0, 1.5)
                    hist_list[(roll-1)*totalvfat+vfat].GetXaxis().SetTitle("residual [cm]")
                    hist_list[(roll-1)*totalvfat+vfat].GetXaxis().SetTitleSize(0.05)
                    hist_list[(roll-1)*totalvfat+vfat].GetXaxis().SetTitleFont(42)
                    if hist_list[(roll-1)*totalvfat+vfat].GetEntries() > 60 :
                        fit_list.append( hist_list[(roll-1)*totalvfat+vfat].GetFunction("gaus"))
                        mean = fit_list[(roll-1)*totalvfat+vfat].GetParameter(1)
                        std =  fit_list[(roll-1)*totalvfat+vfat].GetParameter(2)
                        meanerr = fit_list[(roll-1)*totalvfat+vfat].GetParError(1)
                        stderr  = fit_list[(roll-1)*totalvfat+vfat].GetParError(2)
                        if abs(mean) < 1.0 and abs(meanerr) < 1.0:
                            residual_2D.SetBinContent(vfat+1, roll, mean)
                            residual_2D.SetBinError(vfat+1, roll, meanerr)
                            localX_shift = mean + localX_shift
                            nVfat = nVfat+1
                            hist_rotation_list[vfat].SetBinContent(roll, mean)
                            hist_rotation_list[vfat].SetBinError(roll, meanerr)
                            hist_rotation_list_v2[roll-1].SetBinContent(vfat+1, mean)
                            hist_rotation_list_v2[roll-1].SetBinError(vfat+1, meanerr)

                        else:
                            print "warning!!! large residual!!! "
                            residual_2D.SetBinContent(vfat+1, roll, -99)
                    else:
                        fit_list.append("nofit")
                        residual_2D.SetBinContent(vfat+1, roll, -99)
                        print "no fit for GEM ch%d layer%d roll%d VFAT%d"%(ch, layer+1, roll, vfat)

                    #print "mean ",mean," std ",std
                    #mean = 0.0; std = 1.0
                    #legend_list[roll-1].AddEntry(hist_list[vfat], "mean: %.2f, std:%.1f"%(mean, std))
                    #legend_list[roll-1].AddEntry(hist_list[vfat], "#mu: %.2f, #sigma:%.1f"%(mean, std))
                    #hs_list[roll-1].Add(hist_list[vfat])
                    #txt_list.append(ROOT.TLatex(.65, .7, "#mu: %.2f, #sigma:%.1f"%(mean, std)))
                    #txt_list[(roll-1)*3+vfat].SetNDC()
                    #txt_list[(roll-1)*3+vfat].SetTextFont(42)
                    #txt_list[(roll-1)*3+vfat].SetTextSize(.035)
           
                    #print "(roll-1)*3+vfat ",(roll-1)*3+vfat
                    hist_list[(roll-1)*totalvfat+vfat].Draw("e")
                    #fit_list[(roll-1)*3+vfat].Draw("same")
                    #txt_list[(roll-1)*3+vfat].Draw("same")
                    c1.Update()
            c1.cd()
            c1.Update()
            #print "hist_list ",hist_list," fit_list ",fit_list
            txt = ROOT.TLatex(.5, .5, text)
            txt.SetNDC()
            txt.SetTextFont(42)
            txt.SetTextSize(.035)
            txt.Draw("same")


            picname_layer = plotname+"_ch%d_layer%d_dphi02"%(ch, layer)
            c1.SaveAs(picname_layer+ "_clustersize6.png")
            c1.SaveAs(picname_layer+ "_clustersize6.pdf")

            c2=ROOT.TCanvas("c2","Alignment of GEM ch%d layer%d"%(ch, layer+1),0,0, 800,600);
            residual_2D.SetStats(0)
            setcolortables()
            maxresidualshift = 0.5
            if ch == 30:
                maxresidualshift = 0.7

            residual_2D.SetMaximum(maxresidualshift)
            residual_2D.SetMinimum(maxresidualshift*(-1.0))
            residual_2D.SetTitle("Average local x residual in each VFAT,GEM ch%d layer%d,"%(ch, layer+1) + text)
            residual_2D.SetTitleSize(0.035)
            residual_2D.Draw("text colz err")
            print "Alignment of GEM ch%d layer%d"%(ch, layer+1)," shift in local X ", localX_shift/nVfat
            residual_2D.GetXaxis().SetTitle("#VFAT")
            residual_2D.GetYaxis().SetTitle("#Roll")
            txt2D = ROOT.TLatex(.1, .05,"whole layer average local X residual: %.3f"%( localX_shift/nVfat))
            txt2D.SetNDC()
            txt2D.SetTextFont(42)
            txt2D.SetTextSize(.035)
            txt2D.Draw("same")
            c2.SaveAs(picname_layer+ "_clustersize6_2D.png")
            c2.SaveAs(picname_layer+ "_clustersize6_2D.pdf")


            c3=ROOT.TCanvas("c3","Alignment of GEM ch%d layer%d"%(ch, layer+1),0,0, 800,600);

            hs_rotation_layer = ROOT.THStack("hs_GEM ch%d layer%d"%(ch, layer+1), "GEM ch%d layer%d"%(ch, layer+1))
            fit_rotation_list = []
            legend = ROOT.TLegend(0.6,0.67,0.91,0.7+0.04*totalvfat)
            legend.SetFillColor(ROOT.kWhite)
            #legend.SetTextFont(42)
            #legend.SetTextSize(.035)
            legend.SetHeader("GEM ch%d layer%d"%(ch, layer+1))
            for vfat in range(0, totalvfat):
                hist_rotation_list[vfat].Fit('pol1')
                hist_rotation_list[vfat].SetLineColor(color[vfat])
                fit_rotation_list.append( hist_rotation_list[vfat].GetFunction('pol1'))
                fit_rotation_list[vfat].SetLineColor(color[vfat])
                p0 =  fit_rotation_list[vfat].GetParameter(0)
                p1 =  fit_rotation_list[vfat].GetParameter(1)
                hs_rotation_layer.Add(hist_rotation_list[vfat])
                legend.AddEntry(hist_rotation_list[vfat], "VFAT%d: slope = %.3f"%(vfat, p1),"l")
            hs_rotation_layer.Draw("nostacke")
            for vfat in range(0, totalvfat):
                fit_rotation_list[vfat].Draw("same")
            legend.Draw("same")


            c3.SaveAs(picname_layer+ "_clustersize6_rotationfit.png")
            c3.SaveAs(picname_layer+ "_clustersize6_rotationfit.pdf")


            c4=ROOT.TCanvas("c4","Alignment of GEM ch%d layer%d"%(ch, layer+1),0,0, 800,600);

            hs_rotation_layer_v2 = ROOT.THStack("hs_GEM ch%d layer%d"%(ch, layer+1), "GEM ch%d layer%d"%(ch, layer+1))
            fit_rotation_list_v2 = []
            legend_v2 = ROOT.TLegend(0.6,0.67,0.91,0.7+0.035*8)
            legend_v2.SetFillColor(ROOT.kWhite)
            #legend.SetTextFont(42)
            #legend.SetTextSize(.035)
            legend_v2.SetHeader("GEM ch%d layer%d"%(ch, layer+1))
            for roll in range(1, 9):
                hist_rotation_list_v2[roll-1].Fit('pol1')
                hist_rotation_list_v2[roll-1].SetLineColor(color[roll-1])
                fit_rotation_list_v2.append( hist_rotation_list_v2[roll-1].GetFunction('pol1'))
                fit_rotation_list_v2[roll-1].SetLineColor(color[roll-1])
                p0 =  fit_rotation_list_v2[roll-1].GetParameter(0)
                p1 =  fit_rotation_list_v2[roll-1].GetParameter(1)
                hs_rotation_layer_v2.Add(hist_rotation_list_v2[roll-1])
                legend_v2.AddEntry(hist_rotation_list_v2[roll-1], "roll%d: slope = %.3f"%(roll, p1),"l")
            hs_rotation_layer_v2.Draw("nostacke")
            for roll in range(1, 9):
                fit_rotation_list_v2[roll-1].Draw("same")
            legend_v2.Draw("same")


            c4.SaveAs(picname_layer+ "_clustersize6_rotationfit_v2.png")
            c4.SaveAs(picname_layer+ "_clustersize6_rotationfit_v2.pdf")









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
#chain.Add("slicetest_ana.root")
#chain.Add("2018C_out_ana_v2.root")
#chain.Add("out_ana_all_2018C.root")
#chain.Add("GEMCSCBending_2018C_v11.root")
#chain.Add("GEMCSCAan_crab_SingleMuPt30_MC_1M_20190621_RecoMuNoGEM/*root")
#chain.Add("GEMCSCAan_Run2018D_ZMu_323470-323470_all.root")
#chain.Add("GEMCSCBending_doublemuon_2018C_v1.root")
#filedir = '/eos/uscms/store/group/lpcgem/SingleMuon_Pt30_Eta0To2p5_Extended2023D17_phase2_realistic_1M/GEMCSCAan_crab_SingleMuPt30_MC_1M_20190718_RecoMuNoGEM/190718_202517/0000/'
#filedir = '/eos/uscms/store/group/lpcgem/SingleMuon_Pt30_Eta0To2p5_Extended2023D17_phase2_realistic_1M/GEMCSCAan_crab_SingleMuPt30_MC_1M_20190718_RecoMuNoGEM_xshift/190718_211110/0000/'
#filedir = '/eos/uscms/store/group/lpcgem/SingleMuon_Pt30_Eta0To2p5_Extended2023D17_phase2_realistic_1M/GEMCSCAan_crab_SingleMuPt30_MC_1M_20190719_RecoMuNoGEM_xshiftv2/190719_215803/0000/'
#filedir = '/eos/uscms/store/group/lpcgem/SingleMuon_Pt30_Eta0To2p5_Extended2023D17_phase2_realistic_1M/GEMCSCAan_crab_SingleMuPt30_MC_1M_20190719_RecoMuNoGEM_yshiftv2/190720_033627/0000/'
filedir = '/eos/uscms/store/group/lpcgem/SingleMuon_Pt30_Eta0To2p5_Extended2023D17_phase2_realistic_1M/GEMCSCAan_crab_SingleMuPt30_MC_1M_20190719_RecoMuNoGEM_xyshiftv2/190720_033553/0000/'
chain.Add(filedir+'*.root')
#plotdir = "GEMCSCBending_2018C_doubleMuon_singlemuon_plots/"
#plotdir = "GEMCSCBending_2018C_doubleMuon_singlemuon_plots_alignment/"
#plotdir = "GEMCSCBending_2018C_v11_plots_prop_rechit_dphi_normalized/"
#plotdir = "GEMCSCAan_Run2018D_ZMu_323470_324200_prop_rechit_dphi_normalized/"
#plotdir = "GEMCSCBending_2018C_singlemuon_plots_residual_20190125/"

plotdir = "GEMCSCBending_MC_SingleMuon_fixedPt30_GEMReview_20190719_RdPhi_xyshift/"
#plotdir = "GEMCSCBending_MC_SingleMuon_fixedPt100_GEMReview_20190705/"
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
    for chamber in [27, 28,29, 30]:
    #for chamber in [0]:
        for i in range(0, 2):#2layers for GEM
            todrawX = todraw+"[%d]"%i
            #thiscut = cut + "&& has_GE11[%d]>0 && abs(%s)<4"%(i, todrawX) +" && chamber_GE11[%d] == %d"%(i, chamber)
            thiscut = cut + "&& has_GE11[%d]>0 && abs(%s)<4"%(i, todrawX) 
            plotname = os.path.join(plotdir, "2018D_Zmu_GEMCSCbending_rechit_prop_dphi_GE11_GEMlayer%d_chamber%d"%(i, chamber))
            #plot_tree_1D(chain, todraw, thiscut, "#Delta phi between GEM rechit and propagated muon", 100, -0.10, 0.10, text,plotname)
            plot_tree_1D(chain, todraw, thiscut, "Residual [rad]", 80, -0.020, 0.020, text,plotname)
#plotdPhiGEMMuon(chain, "has_MediumID && muonpt>20", "RecoMuon: Medium ID, p_{T}>20 GeV", plotdir)

def plotGEMHitsVsChamber(chain, cut, text, plotdir):
    todraws = ["chamber_GE11", "chamber_propGE11"]
    cuts = ["has_GE11","has_propGE11"]
    legs = ["chamber with GEM rechits","chamber with propagated muon position"]
    for i in range(0, 2):
        todrawlist = []
        cutlist = []
        for j, todraw in enumerate(todraws) :
            todrawlist.append(todraw+"[%d]"%i)
            cutlist.append(cut+"&&"+cuts[j]+"[%d]"%i)
        plotname = os.path.join(plotdir, "2018D_Zmu_GEMCSCbending_GE11_hashits_GEMlayer%d"%(i))
        plot_tree_1D_multiple(chain, todrawlist, cutlist, legs, "GEM Chamber", 4, 27.0, 31.0, text,plotname)

#plotGEMHitsVsChamber(chain, "has_MediumID && muonpt>20", "muon: medium ID", plotdir)
        

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
	plotname = os.path.join(plotdir, "Run2MC_GEMCSCbending_GEMRechit_x_y_gemlayer%d"%i)
	thiscut = cut + " && has_GE11[%d]>0 && rechit_prop_dR_GE11[%d] < 5.0"%(i, i) 
        plot_tree_2D(chain, todrawX, todrawY, thiscut, "GEM Rechit X", 100, -600.0, 600.0,  "GEM Rechit Y", 100, -600.0, 600.0, text, plotname)
    todrawlist = ["rechit_clusterSize_GE11"]
    xbins = [[20, 0,20]]
    xtitles = ["cluster size, GE11"]
    #for itodraw, todraw in enumerate(todrawlist):
    #    for chamber in [27, 28, 29, 30]:
    #        for i in range(0, 2):
    #            thistodraw = todrawlist+"[%d]"%i
    #            thiscut = cut +" && has_GE11[%d]>0 && rechit_prop_dX_GE11[%d] < 2.0 && chamber_GE11[%d]==%d"%(i,i, i, chamber)
    #            plot_tree_1D(chain, thistodraw, thiscut, xtiles[itodraw], xbins[itodraw][0], xbins[itodraw][1], xbins[itodraw][2], text, plotname)

def plotGEMPropagation(chain, cut, text, plotdir):
    todrawX_gem = "prop_x_GE11"
    todrawY_gem = "prop_y_GE11"
    MaxX = 280.0
    for i in range(0, 2):
	todrawX = todrawX_gem + "[%d]"%i
	todrawY = todrawY_gem + "[%d]"%i
	plotname = os.path.join(plotdir, "Run2MC_GEMCSCbending_GEM_prop_x_y_gemlayer%d"%i)
        thiscut = cut
        plot_tree_2D(chain, todrawX, todrawY, thiscut, "X [cm]", 100, -1*MaxX, MaxX,  "Y [cm]", 100, -1*MaxX, MaxX, text, plotname)
	plotname2 = os.path.join(plotdir, "Run2MC_GEMCSCbending_GEM_prop_x_y_gemlayer%d_hasGEMhits"%i)
	thiscut2 = cut + " && has_GE11[%d]>0 && abs(rechit_x_GE11[%d]-prop_x_GE11[%d]) < 5.0"%(i, i, i) 
        plot_tree_2D(chain, todrawX, todrawY, thiscut2, "X [cm]", 100, -1*MaxX, MaxX,  "Y [cm]", 100, -1*MaxX, MaxX, text, plotname2)
	plotname3 = os.path.join(plotdir, "Run2MC_GEMCSCbending_GEM_prop_x_y_gemlayer%d_hasGEMhitsOR"%i)
	#thiscut3 = cut + " && ((has_GE11[0]>0 && rechit_prop_dX_GE11[0] < 5.0)|| (has_GE11[1]>0 && rechit_prop_dX_GE11[1] < 5.0))"
	thiscut3 = cut + "&& (abs(rechit_x_GE11[0]-prop_x_GE11[0]) < 5.0 || abs(rechit_x_GE11[1]-prop_x_GE11[1]) < 5.0)"
        plot_tree_2D(chain, todrawX, todrawY, thiscut3, "X [cm]", 100, -1*MaxX, MaxX,  "Y [cm]", 100, -1*MaxX, MaxX, text, plotname3)



#plotGEMPropagation(chain, "has_TightID && muonpt>20 && prop_x_GE11 < 999.0", "muon p_{T} = 30 GeV, tight ID",plotdir)


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
    todrawlist  = ["dphi_keyCSCRechit_GE11Rechit", "dphi_keyCSCRechit_alignedGE11Rechit"]
    #todrawlist = ["dphi_CSCSeg_GE11Rechit","dphi_CSCSeg_alignedGE11Rechit"]
    todrawY= "muonpt"
    xbin = 90; xmin=-0.045; xmax = 0.045
    ybin= 14; ymin=5.0; ymax=75.0
    for i, todraw in enumerate(todrawlist):
        for ich in range(27, 31):
            for layer in range(0,2):
                todraw_dphi = todraw + "[%d]"%layer
                plotname = os.path.join(plotdir, "2018C_GEMCSCbending_%s_gemchamber%d_layer%d_drcut"%(todraw, ich, layer))
                dRcut = "&& rechit_prop_dR_ME11[2]<5.0 && abs(rechit_prop_dphi_GE11[0])<.02"
                #dRcut = "&& cscseg_prop_dR_st[0]< 2.0 && abs(rechit_prop_dphi_GE11[0])<.02"
                thiscut = cut + " &&  has_GE11[%d]>0 && has_propGE11[%d]>0 && has_ME11[2]>0 "%(layer, layer) +" && chamber_GE11[%d]==%d"%(layer, ich) + dRcut
                #thiscut = cut + " &&  has_GE11[%d]>0 && has_propGE11[%d]>0 && has_cscseg_st[0]>0 "%(layer, layer) +" && chamber_GE11[%d]==%d"%(layer, ich) + dRcut
                thistext = text+" GEM chamber %d, layer %d"%(ich, layer+1)
                plot_tree_2D(chain, todraw_dphi, todrawY, thiscut, "GEM-CSC bending angle", xbin, xmin, xmax,  "Muon p_{T} GeV", ybin, ymin, ymax, thistext, plotname)

#plotdeltaPhi(chain, "has_TightID", "tight ID",plotdir)
#plotdeltaPhiVspt(chain, "has_TightID ", "muon tight ID", plotdir)

def plotGEMalignment(chain, cut, text, plotdir):
    xbin = 80; xmin=-24.0; xmax = 24.0
    #xbin =384/6; xmin=0; xmax = 384
    #ybin= 15*8; ymin=-10.0; ymax= 25*7.0+15.0
    #ybin= 20; ymin=-10.0; ymax= 10.0
    ybin = 15*8+20; ymin = 120.0; ymax = 260;
    ## make residual distribution for even or odd chamber
    for ich in [28,29]:
        for layer in range(0,2):
            plotname = os.path.join(plotdir, "GEMResidual_gemchamber%d_layer%d_drcut_pt30"%( ich, layer))
	    ## same roll
            #dRcut = "&& abs(rechit_prop_dphi_GE11[%d])<.2 && roll_propGE11[%d] == roll_rechitGE11[%d]"%(layer, layer, layer)
            dRcut = "&& abs(rechit_prop_dphi_GE11[%d])<.2 "%(layer) 
	    chambercut = "&& chamber_GE11[%d] == chamber_propGE11[%d]"%(layer, layer)
            thiscut = cut + " &&  has_GE11[%d]>0 && has_propGE11[%d]>0"%(layer, layer) +" && chamber_GE11[%d]%%2==%d"%(layer, ich%2)+dRcut+chambercut
            #thistext = text+" GEM chamber %d, layer %d"%(ich, layer+1)
            #thistext = "GEM chamber %d, layer %d"%(ich, layer+1)
	    evenodd = "odd" if ich%2 == 1 else "even"
            thistext = "GEM %s chamber, layer %d"%(evenodd, layer+1)
	    x="prop_localx_GE11[%d]"%(layer)
	    #y="(prop_localy_GE11[%d]+25.0*(8-roll_GE11[%d]))"%(layer, layer)
	    plotsuffix = "chambercut"
	    y="(prop_localy_GE11[%d]+middle_perp_propGE11[%d])"%(layer, layer)
	    #z = "TMath::Cos(rechit_stripangle_GE11[%d])*(prop_localx_GE11[%d]-rechit_localx_GE11[%d]) - TMath::Sin(rechit_stripangle_GE11[%d])*(prop_localy_GE11[%d]+middle_perp_GE11[%d]-rechit_perp_GE11[%d])"%(layer, layer, layer, layer, layer, layer, layer)
	    #z = "TMath::Cos(rechit_stripangle_GE11[%d])*(prop_localx_GE11[%d]-rechit_localx_GE11[%d]) - TMath::Sin(rechit_stripangle_GE11[%d])*(prop_localy_GE11[%d])"%(layer, layer, layer, layer, layer)
	    z = "(rechit_prop_RdPhi_GE11[%d])"%layer
            plot_tree_2D_alignment(chain, ich, layer, thiscut, x,y,z, xbin, xmin, xmax, ybin, ymin, ymax, thistext, plotname+"_ST_Rdphi"+plotsuffix)
	    #z = "TMath::Cos(rechit_stripangle_GE11[%d])*(prop_localx_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer, layer)
            #plot_tree_2D_alignment(chain, ich, layer, thiscut, x,y,z, xbin, xmin, xmax, ybin, ymin, ymax, thistext, plotname+"_ST_dXcosangle"+plotsuffix)
	    x="propinner_localx_GE11[%d]"%(layer)
	    y="(propinner_localy_GE11[%d]+middle_perp_propGE11[%d])"%(layer, layer)
	    #z = "TMath::Cos(rechit_stripangle_GE11[%d])*(propinner_localx_GE11[%d]-rechit_localx_GE11[%d]) - TMath::Sin(rechit_stripangle_GE11[%d])*(propinner_localy_GE11[%d]+middle_perp_GE11[%d]-rechit_perp_GE11[%d])"%(layer, layer, layer, layer, layer, layer, layer)
	    #z = "TMath::Cos(rechit_stripangle_GE11[%d])*(propinner_localx_GE11[%d]-rechit_localx_GE11[%d]) - TMath::Sin(rechit_stripangle_GE11[%d])*(propinner_localy_GE11[%d])"%(layer, layer, layer, layer, layer)
	    z = "(rechit_propinner_RdPhi_GE11[%d])"%layer
            #plot_tree_2D_alignment(chain, ich, layer, thiscut, x,y,z, xbin, xmin, xmax, ybin, ymin, ymax, thistext, plotname+"_inner_Rdphi"+plotsuffix)
	    #z = "TMath::Cos(rechit_stripangle_GE11[%d])*(propinner_localx_GE11[%d]-rechit_localx_GE11[%d])"%(layer, layer, layer)
            plot_tree_2D_alignment(chain, ich, layer, thiscut, x,y,z, xbin, xmin, xmax, ybin, ymin, ymax, thistext, plotname+"_inner_dXcosangle"+plotsuffix)
    ## make residual distribution for each chamber
    for endcap in (1,3):
	for ich in range(1, 37):
	    for layer in range(0, 2):
		plotname = os.path.join(plotdir, "GEMResidual_endcap%d_gemchamber%d_layer%d_drcut_pt30"%(endcap, ich, layer))
		encapcut = "&& muoneta > 0 " if endcap == 1 else "&& muoneta < 0"
		chambercut = "&& chamber_GE11[%d] == chamber_propGE11[%d] && chamber_GE11[%d] == %d"%(layer, layer, layer, ich)
		dRcut = "&& abs(rechit_prop_dphi_GE11[%d])<.2 "%(layer)
		thiscut = cut + " &&  has_GE11[%d]>0 && has_propGE11[%d]>0"%(layer, layer) + encapcut + chambercut + dRcut
		thistext = "GEM chamber %d, layer %d"%(ich, layer+1)
		plotsuffix=""

		x="prop_localx_GE11[%d]"%(layer)
		y="(prop_localy_GE11[%d]+middle_perp_propGE11[%d])"%(layer, layer)
		z = "(rechit_prop_RdPhi_GE11[%d])"%layer
		plot_tree_2D_alignment(chain, ich, layer, thiscut, x,y,z, xbin, xmin, xmax, ybin, ymin, ymax, thistext, plotname+"_ST_Rdphi"+plotsuffix)
		x="propinner_localx_GE11[%d]"%(layer)
		y="(propinner_localy_GE11[%d]+middle_perp_propGE11[%d])"%(layer, layer)
		z = "(rechit_propinner_RdPhi_GE11[%d])"%layer
		plot_tree_2D_alignment(chain, ich, layer, thiscut, x,y,z, xbin, xmin, xmax, ybin, ymin, ymax, thistext, plotname+"_inner_Rdphi"+plotsuffix)

def plotME11alignment(chain, cut, text, plotdir):
    xbin = 60; xmin = -60.0; xmax = 60
    ybin = 100; ymin = -100.0; ymax = 100.0
    for ich in [1,2]:
        for layer in range(0, 6):
            plotname = os.path.join(plotdir, "GEMResidual_ME11chamber%d_layer%d_drcut_pt30"%( ich, layer))
            dRcut = "&& abs(rechit_prop_dphi_ME11[%d])<.2"%(layer)
            thiscut = cut + " &&  has_ME11[%d]>0 && has_propME11[%d]>0"%(layer, layer) +" && chamber_ME11[%d]%%2==%d"%(layer, ich%2)+dRcut
            thistext = "ME11 chamber %d, layer %d"%(ich, layer+1)
	    x="prop_localx_ME11[%d]"%(layer)
	    y="prop_localy_ME11[%d]"%(layer)
	    z = "(rechit_prop_RdPhi_ME11[%d])"%layer
            plot_tree_2D_alignment(chain, ich, layer, thiscut, x,y,z, xbin, xmin, xmax, ybin, ymin, ymax, thistext, plotname+"_ST_Rdphi")
	    x="propinner_localx_ME11[%d]"%(layer)
	    y="propinner_localy_ME11[%d]"%(layer)
	    z = "(rechit_propinner_RdPhi_ME11[%d])"%layer
            plot_tree_2D_alignment(chain, ich, layer, thiscut, x,y,z, xbin, xmin, xmax, ybin, ymin, ymax, thistext, plotname+"_inner_Rdphi")

	    

plotGEMalignment(chain, "has_MediumID && muonpt>25", "medium ID",plotdir)
#plotME11alignment(chain, "has_MediumID && muonpt>25", "medium ID",plotdir)

ptbin = [10.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 80.0, 100.0, 150.0, 200.0]
myptbin = np.asarray(ptbin)
def plotGEMHitEff_ptbin(chain, dencut, text, plotdir):
    thisplotdir = os.path.join(plotdir, "GEMRechit_Eff_ptbin_run319347_")
    plotGEMHitEff(chain, "muonpt", dencut,  myptbin, "Muon p_{T}^{reco} [GeV]", text, thisplotdir)

#plotGEMHitEff_ptbin(chain, "has_TightID && muoneta < 0 && run == 319347", "Muon tight ID", plotdir)
#plotGEMHitEff_phi(chain,  "has_TightID && muonpt>=25 && muoneta < 0 && hasGEMdata>0", "Muon tight ID, p_{T}^{reco}>25", os.path.join(plotdir, "GEMRechit_Eff_phibin_pt25_"))
##strip
#plotGEMHitEff_phi(chain,  "has_TightID && muonpt>=25 && muoneta < 0 && run == 319347", "Muon tight ID, p_{T}^{reco}>25", os.path.join(plotdir, "GEMRechit_Eff_stripbin_pt25_run319347_"))
#plotME11CSCHitEff(chain, "prop_phi_ME11", "has_TightID && muonpt>=25 && muoneta < 0", 72, -3.1415, 3.1415,  "global #phi", "Muon tight ID, p_{T}^{reco}>25",  os.path.join(plotdir, "ME11Rechit_eff_phibin_pt25_"))
#plotME11CSCHitEff(chain, "chamber_propME11", "has_TightID && muonpt>=25 && muoneta < 0", 36, 1.0, 37.0,  "ME11, chamber", "Muon tight ID, p_{T}^{reco}>25",  os.path.join(plotdir, "ME11Rechit_eff_chamberbin_pt25_"))
#plotCSCSegmentEff(chain, "prop_chamber_st", "has_TightID && muonpt>=25 && muoneta < 0", 36, 1.0, 37.0, "MEX1, chamber", "Muon tight ID, p_{T}^{reco}>25", os.path.join(plotdir, "CSCsegment_eff_chamberbin_pt25_"))

#plot_residual_1D(chain, "has_TightID && muonpt>=25", "residual [cm]", 60, -2.0, 2.0, "tight ID, p_{T}^{reco}>25", os.path.join(plotdir, "GEMalignment_residual_1D_StandaloneMu_fit"))
#plot_residual_1D(chain, "has_TightID && muonpt>=25", "residual [cm]", 60, -2.0, 2.0, "tight ID, p_{T}^{reco}>25", os.path.join(plotdir, "GEMalignment_residualRdphi_1D_inner_fit"))
#plot_residual_1D_v2(chain, "has_TightID && muonpt>=15", "residual [cm]", 50, -5.0, 5.0, "tight ID, p_{T}^{reco}>15", os.path.join(plotdir, "GEMalignment_residual_vfat6"))
