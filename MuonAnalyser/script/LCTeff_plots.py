import ROOT
import random
import os
import sys
import numpy as np
import array
import math

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


xmin=0
xmax=60
xbins=30
BINM=22
#binLow = [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,12.0,14.0,16.0,18.0,20.0,24.0,28.0,32.0,36.0,42.0,50.0,60.0]
binLow = [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,12.0,14.0,16.0,18.0,20.0,24.0,28.0,32.0,36.0,42.0,50.0]
ptbins = np.asarray(binLow)
	
def gethist1D(chain, den, todraw, x_bins):
	
    xBins = int(x_bins[1:-1].split(',')[0])
    xminBin = float(x_bins[1:-1].split(',')[1])
    xmaxBin = float(x_bins[1:-1].split(',')[2])
    h1 = ROOT.TH1F("h1","h1",xBins,xminBin,xmaxBin)
    chain.Draw("fabs(%s) >> h1"%todraw,den)
    #print "gethist1D, den ",den
    #h1.Print("ALL")
    return h1
		



def draw2Dplots_1(ch, xaxis, yaxis, x_bins, y_bins, xtitle, ytitle,cuts, text, picname):

    xBins = int(x_bins[1:-1].split(',')[0])
    xminBin = float(x_bins[1:-1].split(',')[1])
    xmaxBin = float(x_bins[1:-1].split(',')[2])
    yBins = int(y_bins[1:-1].split(',')[0])
    yminBin = float(y_bins[1:-1].split(',')[1])
    ymaxBin = float(y_bins[1:-1].split(',')[2])

    todrawb0 = "%s"%yaxis+":"+"%s>>b0"%xaxis
    
    c0 = ROOT.TCanvas("c0","c0")
    c0.SetGridx()
    c0.SetGridy()
    c0.SetTickx()
    c0.SetTicky()
    b0 = ROOT.TH2F("b0","b0",xBins,xminBin,xmaxBin,yBins,yminBin,ymaxBin)
    b0.GetXaxis().SetTitle("%s"%xtitle)
    b0.GetYaxis().SetTitle("%s"%ytitle)
    b0.GetXaxis().SetTitleSize(.04)
    b0.GetYaxis().SetTitleSize(.04)
    #b0.SetTitle("#scale[1.4]{#font[61]{CMS}} #font[52]{ preliminary}"+"  "*15+"Run=281976")
    title = "#scale[1.4]{#font[61]{CMS}} #font[42]{ Internal}"+"  "*15+"2018RunA, ZMu"
    b0.SetTitle(title)
    #b0.SetTitle("%s Vs %s,%s"%(ytitle0, xtitle, st_title)) 
    #b1.SetTitleFont(62)
    b0.SetTitleSize(0.05)
    #b1.SetMaximum(30)
    b0.SetStats(0)
    #hasxy = "&& fabs(%s)>0 && fabs(%s)>0"%(xaxis, yaxis0)
    ch.Draw(todrawb0,cuts,"colz")
    print "todraw ",todrawb0, " cut ",cuts

    #tex1 = TLatex(0.35,.8,"#splitline{%s}{%.1f<|#eta|<%.1f,20<p_{T}<50}"%(st_title,etamin,etamax))
    #tex1 = ROOT.TLatex(0.15,.8,"%s"%(text))
    tex1 = ROOT.TLatex(0.2,.8,"%s"%(text))
    tex1.SetTextSize(0.05)
    tex1.SetTextFont(62)
    tex1.SetNDC()
    tex1.Draw("same")
    c0.SaveAs("%s"%picname+".png")
    c0.SaveAs("%s"%picname+".pdf")
    c0.SaveAs("%s"%picname+".C")

def draw1D_compare(chs, xaxis_list, x_bins, xtitle, legs, cuts, text, picname):

    xBins = int(x_bins[1:-1].split(',')[0])
    xminBin = float(x_bins[1:-1].split(',')[1])
    xmaxBin = float(x_bins[1:-1].split(',')[2])
    color = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2,ROOT.kMagenta+2, ROOT.kCyan+2]
    maker = [20,21,22,23,33]
    title = "#scale[1.4]{#font[61]{CMS}} #font[42]{ Internal}"+"  "*15+"2018RunA, ZMu"
    #title = "#scale[1.4]{#font[61]{CMS}} #font[52]{ Simulation preliminary}"+"  "*15+"0 PU"
    hs1 = ROOT.THStack("hs1","%s"%title)
    hs2 = ROOT.THStack("hs2","%s"%title)
    legend = ROOT.TLegend(0.6,0.5,0.85,0.7)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetTextFont(42)
    legend.SetTextSize(.05)
    i=0
    for ch in chs:
	print "todraw ","%s>>hist%d"%(xaxis_list[i], i)," cut ",cuts[i]
	hist = ROOT.TH1F("hist%d"%i,"hist%d"%i, xBins, xminBin, xmaxBin)
	ch.Draw("%s>>hist%d"%(xaxis_list[i], i),cuts[i])
	ROOT.SetOwnership(hist, False)
	hist.SetLineColor(color[i])
	hist.SetLineWidth(2)
	hs1.Add(hist)
	hs2.Add(hist.Scale(1.0/hist.Integral()))
	legend.AddEntry(hist, "%s"%legs[i],"l")
	i +=1

    c0 = ROOT.TCanvas("c0","c0")
    c0.SetGridx()
    c0.SetGridy()
    c0.SetTickx()
    c0.SetTicky()
    c0.SetLogy()
    hs1.SetMinimum(.0001)
    hs1.Draw("nostackhist") 
    hs1.GetHistogram().GetXaxis().SetTitle("%s"%xtitle)
    hs1.GetHistogram().GetXaxis().SetTitleSize(.05)
    hs1.GetHistogram().GetYaxis().SetTitle("Normalized to unity")
    hs1.GetHistogram().GetYaxis().SetTitleSize(.05)
    #hs1.GetHistogram().GetYaxis().SetRangeUser(.001,2)
    #legend.Draw("same")
    tex1 = ROOT.TLatex(0.2,.8,"%s"%(text))
    tex1.SetTextSize(0.05)
    tex1.SetTextFont(62)
    tex1.SetNDC()
    tex1.Draw("same")
    c0.SaveAs("%s"%picname+".png")
    c0.SaveAs("%s"%picname+".pdf")
    c0.SaveAs("%s"%picname+".C")

    """
    c1 = ROOT.TCanvas("c1","c1")
    c1.SetGridx()
    c1.SetGridy()
    c1.SetTickx()
    c1.SetTicky()
    hs2.Draw("nostack") 
    hs2.GetHistogram().GetXaxis().SetTitle("%s"%xtitle)
    hs2.GetHistogram().GetYaxis().SetTitle("Normalized to unity")
    legend.Draw("same")
    tex1.SetNDC()
    tex1.Draw("same")
    c1.SaveAs("%s"%picname+"_normalized.png")
    c1.SaveAs("%s"%picname+"_normalized.C")
    """


cscstations = [ [0,0], 
                [1,1], [1,2], [1,3],
                [2,1], [2,2],
                [3,1], [3,2],
                [4,1], [4,2],]
chambernames = ["all",
		"ME1/1","ME1/2","ME1/3",
		"ME2/1","ME2/2",
		"ME3/1","ME3/2",
		"ME4/1","ME4/2",]


def drawPlots_CSCChambertype_1D(chs, cuts, xaxis_list, xbins, xtitle, legs, text, outputdir, plotsuffix):
    Endcaps = {'positive': 'CSCEndCapPlus','negative': '!CSCEndCapPlus','all':"1"}
    for key in Endcaps:
      cap = Endcaps[key]  
      ichamber = 0
      for x in cscstations:
        cuts_new = []
        xaxis_listnew  = []
        text_new = ""
        if x==[0,0]:
            #not possible here
            #detid = " && %s"%(cap)
            #for cut in cuts:
            #    cuts_new.append(cut + detid)
            #text_new = text+", all %s CSC chambers"%key
            #draw1D_compare(chs, xaxis_list, xbins, xtitle, legs, cuts_new, text_new, outputdir+"Zmass_probemuon_%s_all%sCSCs"%(plotsuffix, key))
            ichamber +=1
            continue
        station = x[0]
        ring = x[1]
        detid = "&& %s  && CSCRg%d == %d"%( cap, station, ring)
	if station == 1 and ring == 1:
	    detid = "&& %s  && (CSCRg%d == 1 || CSCRg%d == 4)"%( cap, station, station)
	else:
	   ichamber +=1
	   continue

        for xaxis in xaxis_list:
            xaxis_listnew.append(xaxis+"%d"%station)
            cut = cuts+"&& CSCDxyTTSeg%d < 50.0 && CSCDxyTTLCT%d < 50.0"%(station, station)
            cuts_new.append(cut + detid)
        text_new = text+",%s %s"%(key, chambernames[ichamber])
        draw1D_compare(chs, xaxis_listnew, xbins, xtitle, legs, cuts_new, text_new, outputdir+"Zmass_probemuon_%s_st%d_ring%d_%s"%(key, station, ring, plotsuffix))
        if station == 1 and (ring == 1 or ring == 4) and key != 'all':
            for ich in range(1, 37):
                cuts_new = []
                xaxis_listnew  = []
                text_new = ""
                detid = "&& %s  && CSCRg%d == %d && CSCCh%d == %d"%( cap, station, ring, station, ich)
                for xaxis in xaxis_list:
                    xaxis_listnew.append(xaxis+"%d"%station)
                    cut = cuts + " && CSCDxyTTSeg%d < 50.0 && CSCDxyTTLCT%d < 50.0"%(station, station)
                    cuts_new.append(cut + detid)
                text_new = text+",%s %s_%d"%(key, chambernames[ichamber], ich)
                draw1D_compare(chs, xaxis_listnew, xbins, xtitle, legs, cuts_new, text_new, outputdir+"Zmass_probemuon_%s_st%d_ring%d_ch%d_%s"%(key, station, ring, ich, plotsuffix))

        ichamber +=1



#######################################################
#file1 = "TPEHists_run2016H_v1_281976.root"


chain = ROOT.TChain("aodDump/Fraction")
#chain.Add("CSCeff_SingleMuon_2018A_v1_1.root")
chain.Add("/eos/uscms/store/user/tahuang/SingleMuon/LCTeffAan_Run2018A_ZMu_306926_20180724/180726_135048/0000/CSCeff_SingleMuon_2018A_v1*root")
chain.Add("/eos/uscms/store/user/tahuang/SingleMuon/LCTeffAan_Run2018A_ZMu_306926_20180724/180726_135048/0001/CSCeff_SingleMuon_2018A_v1*root")


outputdir = "CSCeff_SingleMuon_2018A_v1_plots_matchWin/"
os.system("mkdir -p "+outputdir)

allvars = ["N_seg_inChamber", "CSCDxyTTLCT", "CSCDxyTTSeg","CSCLCTkeyStrip","CSCLCTkeyWG", "CSCLCTmatchWin"]
xtitles = ["#CSCsegment in chamber", "#Delta R(projected, LCT) [cm]", "#Delta R(projected, CSCSeg) [cm]", "LCT keyStrip", "LCT WG", "ALCT arrival BX in CLCT match window [BX]"]
xbinsall = ["(6, -0.5, 5.5)","(50, 0.0, 50.0)","(50, 0.0, 50)","(161, 0.5, 160.5)","(97,-0.5, 96.5)","(8, -0.5, 7.5)"]

cuts = "tracks_pt > 5"
for ivar, var in enumerate(allvars):
    if var != "CSCLCTmatchWin":
       continue
    xaxis_list = [var]
    xbins = xbinsall[ivar]
    xtitle = xtitles[ivar]
    legs = [""]
    text = var
    plotsuffix = var
    drawPlots_CSCChambertype_1D([chain], cuts, xaxis_list, xbins, xtitle, legs, text, outputdir, plotsuffix)





