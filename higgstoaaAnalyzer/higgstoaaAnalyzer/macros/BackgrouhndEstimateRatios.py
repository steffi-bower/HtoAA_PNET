import ROOT
import sys
import subprocess
import string,math,os
import glob
import numpy as np
import tdrstyle, CMS_lumi

ROOT.gROOT.SetBatch(True)

label = sys.argv [1]
#hists = ["h_tauE_tauE_Mvis_EG" ,"h_tauE_tauE_Mvis_EGorDoubleEG","h_tauE_tauE_Mvis_noTrig","h_tauMu_tauE_Mvis_SingleMu", "h_tauMu_tauE_Mvis_EGorSingleMu" ,"h_tauMu_tauE_Mvis_MuEGorSingleMu" ,"h_tauMu_tauE_Mvis_noTrig", "h_tauMu_tauMu_Mvis_SingleMu", "h_tauMu_tauMu_Mvis_SingleMuorDoubleMu","h_tauMu_tauMu_Mvis_noTrig"]
#hists = ["h_MET"]
channels = ["tauE_tauMu","tauHad_tauMu","tauHad_tauE"]
titles = {
    "tauE_tauMu":"e#mu",
    "tauHad_tauE":"e#tau",
    "tauHad_tauMu":"#mu#tau"
}
variables= [    
    ["b1_ID_Total","Total ID Value"],
    ["b1_PNetID","PNet ID Value"],
    ["Mvis","M_{vis} GeV"],
    ["bMass","bMass GeV"],
    ["lep1Pt","lep1 p_{T} (GeV)"],
    ["lep2Pt","lep2 p_{T} (GeV)"],
    ["mergedLepPt", "Reco Di#tau  p_{T} (GeV)"],
    ["mergedBPt", "Reco bb  p_{T} (GeV)"]
    #["lepDr","#{Delta}R (leptons)"],
    #["lep1DRB","#{Delta}R (bL1)"],
    #["lep2DRB","#{Delta}R (bL2)"],
    #["MET","MET (GeV)"],
    #["NLep1s","NLep1s",[5,0,5]],
    #["NLep2s","NLep2s",[5,0,5]],

    ]

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 }"
CMS_lumi.writeExtraText = 1
#CMS_lumi.extraText = "Data"
CMS_lumi.lumi_sqrtS = "33.6fb^{-1}" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod = 9

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.15
plotfolder = "/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/"
outDir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/graphs/"+label+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)      
checkAndMakeDir(outDir)

Files={
    "DR_NOM": {"Data":ROOT.TFile.Open(plotfolder+"03042025_DRNom_ReRun_fixed_SIGNAL.root"),
               "TTJets":ROOT.TFile.Open(plotfolder+"17102025_DRNom_MC_ExtraBackgrounds_TTJets_2018_NTuple.root"),
               #"WJetstoLNu":ROOT.TFile.Open(plotfolder+" 17102025_SR_MC_ExtraBackgrounds_WJetstoLNu_2018_Skimmed"),
               #"WZ":ROOT.TFile.Open(plotfolder+" 17102025_SR_MC_ExtraBackgrounds_WZ_2018_Skimmed.root"),
               #"ZZ":ROOT.TFile.Open(plotfolder+" 17102025_SR_MC_ExtraBackgrounds_ZZ_2018_Skimmed.root"),
               #"WW":ROOT.TFile.Open(plotfolder+" 17102025_SR_MC_ExtraBackgrounds_WW_2018_Skimmed.root"),

               #"DYJets":ROOT.TFile.Open(plotfolder+" 17102025_SR_MC_ExtraBackgrounds_DYJetsToLL_M-50_2018_Skimmed.root"),
               "SUSY":ROOT.TFile.Open(plotfolder+"17102025_DRNom_MC_ExtraBackgrounds_SUSY_2018_NTuple.root")
               },
    "DR_ALT": {"Data":ROOT.TFile.Open(plotfolder+"07042025_DRAlt_ReRun_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"21102024_MC_ReversedBidSS_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"21102024_MC_ReversedBidSS_SUSY_2018_NTuple.root")},
    "AR": {"Data":ROOT.TFile.Open(plotfolder+"24042025_AR_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"21102024_MC_ReversedBidOS_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"21102024_MC_ReversedBidOS_SUSY_2018_NTuple.root")},

    #"V_DR_NOM": {"Data":ROOT.TFile.Open(plotfolder+"ParkingBPH_21042025_DRNom_V_emu_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSNOMBIDRevTau_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSNOMBIDRevTau_SUSY_2018_NTuple.root")},
    #"V_DR_ALT": {"Data":ROOT.TFile.Open(plotfolder+"21042025_DRALT_V_emu_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSRevBIDRevTau_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSRevBIDRevTau_SUSY_2018_NTuple.root")},
    #"V_AR": {"Data":ROOT.TFile.Open(plotfolder+"20042025_SR_V_emu_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSRevBIDRevTau_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSRevBIDRevTau_SUSY_2018_NTuple.root")},
    #"V_SR": {"Data":ROOT.TFile.Open(plotfolder+"20042025_AR_V_emu_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSNOMBIDRevTau_genmatch_metfix_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSNOMBIDRevTau_genmatch_metfix_SUSY_2018_NTuple.root")}

    "V_DR_NOM": {"Data":ROOT.TFile.Open(plotfolder+"ParkingBPH_28032025_DRNOMV_Data_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSNOMBIDRevTau_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSNOMBIDRevTau_SUSY_2018_NTuple.root")},
    "V_DR_ALT": {"Data":ROOT.TFile.Open(plotfolder+"ParkingBPH_31032025_DRAltV_ReRun.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSRevBIDRevTau_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSRevBIDRevTau_SUSY_2018_NTuple.root")},
    "V_AR": {"Data":ROOT.TFile.Open(plotfolder+"09042025_AR_V_ActualARLOL_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSRevBIDRevTau_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSRevBIDRevTau_SUSY_2018_NTuple.root")},
    "V_SR": {"Data":ROOT.TFile.Open(plotfolder+"14042025_SR_V_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSNOMBIDRevTau_genmatch_metfix_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSNOMBIDRevTau_genmatch_metfix_SUSY_2018_NTuple.root")}
}


Ratios={"FF":["DR_NOM","DR_ALT"],
        "FF1":["V_DR_NOM","V_DR_ALT"],
        "FF2":["V_SR","V_AR"],
        "Closure_DRNom":["V_DR_NOM","DR_NOM"],
        "Closure_DRALT":["V_DR_ALT","DR_ALT"],
        "Closure_AR":["V_AR","AR"],
        "Transfer_RevID":["AR","DR_ALT"],
        "Transfer_RevID_V":["V_AR","V_DR_ALT"],
        "Transfer_NomID_V":["V_SR","V_DR_NOM"],


        }

H_ref = 800; 
W_ref = 850; 
W = W_ref
H  = H_ref
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.08*W_ref
#c1 = ROOT.TCanvas("Delta RDelta RN","", 800, 850)
c1 = ROOT.TCanvas("Delta RDelta RN","",50,50, W, H)
c1.SetFillColor(0)
c1.SetBorderMode(0)
c1.SetFrameFillStyle(0)
c1.SetFrameBorderMode(0)
c1.SetLeftMargin( L/W )
c1.SetRightMargin( R/W )
c1.SetTopMargin( T/H )
c1.SetBottomMargin( B/H )
c1.SetTickx(0)
c1.SetTicky(0)


EventSelection=False
def makeRatios(Region1,Region2,Factor):

    n = Region1.GetNbinsX()
    r1vr2=ROOT.TH1F("Ratios", Factor+"_r1vr2" , n, Region1.GetXaxis().GetXmin(), Region1.GetXaxis().GetXmax())
    for i in range (0,n+1):
        r1=Region1.GetBinContent(i)

        r2=Region2.GetBinContent(i)
        if(r1>0 and r2>0):
            e = r2/r1
            r1vr2.SetBinContent(i,e)
    return r1vr2
def makeCombined(Region1,Region2,Factor,tag):

    n = Region1.GetNbinsX()
    Combined=ROOT.TH1F("Combined_"+tag, Factor+tag+" combined" , n, Region1.GetXaxis().GetXmin(), Region1.GetXaxis().GetXmax())
    for i in range (0,n+1):
        r1=Region1.GetBinContent(i)

        r2=Region2.GetBinContent(i)

        e = r1-r2
        Combined.SetBinContent(i,e)
    return Combined
Backgrounds={"TTJets":ROOT.kMagenta,"WW":ROOT.kRed,"WZ":ROOT.kBlue,"WJetsToLNu":ROOT.kGreen,"DYJets":ROOT.kCyan}
#def makeStack():

def makeVariablePlots():
    for factor in Ratios.keys():
        checkAndMakeDir(outDir+"/"+factor)

        for channel in channels:
            checkAndMakeDir(outDir+"/"+factor+"/"+channel)
            for variable in variables:
                outFolder=outDir+"/"+factor+"/"+channel
                hist="h_"+channel+"_"+variable[0]+"_isBPH"
                XTitle = variable[1] + " "+titles[channel]
                print (hist)
                histos ={
                    "Data":[Files[Ratios[factor][0]]["Data"].Get(hist),Files[Ratios[factor][1]]["Data"].Get(hist)],
                    "TTJets":[Files[Ratios[factor][0]]["TTJets"].Get(hist),Files[Ratios[factor][1]]["TTJets"].Get(hist)],
                    "Signal":[Files[Ratios[factor][0]]["SUSY"].Get(hist),Files[Ratios[factor][1]]["SUSY"].Get(hist)]
                }

                for h in histos.keys():

                    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
                    #CMS_lumi.CMS_lumi(pad1, iPeriod, iPos)

                    pad1.SetBottomMargin(0) # Upper and lower plot are joined
                    pad1.SetGridx()         # Vertical grid
                    pad1.Draw()
                    pad1.cd()
                    pad1.SetLogy()
                    histos[h][0].SetStats(0)
                    histos[h][0].SetTitle(factor+" "+h)

                    histos[h][0].SetMinimum(.1)
                    histos[h][0].GetYaxis().SetTitle("Events")

                    #  TCP_l.Draw("same hist e")
                    #  TCP_m.Draw("same hist e")
                    #  TCP_h.Draw("same hist e")

                    histos[h][0].SetLineColor(ROOT.kBlue)

                    histos[h][1].SetLineColor(ROOT.kRed)
                    histos[h][0].Draw("hist e1")
                    histos[h][1].Draw("same hist e1")
                    #SUSY_TH1F.Draw("same hist e1")

                    l = ROOT.TLegend(0.65,0.7,0.85,0.87)

                    l.AddEntry(histos[h][0], Ratios[factor][0], "l")
                    l.AddEntry(histos[h][1], Ratios[factor][1], "l")
                    l.Draw("same")

                    c1.cd()

                    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.1, 1, 0.3)
                    pad2.SetTopMargin(0)
                    pad2.SetBottomMargin(0.26)
                    pad2.SetGridx() # vertical grid
                    pad2.Draw()
                    pad2.cd()
                    ratioplot=ROOT.TRatioPlot(histos[h][0],histos[h][1])

                    ratioplot.Draw("ep")

                    #ratioplot.SetStats(0)

                    # Y axis ratio plot settings
                    ratioplot.GetYaxis().SetTitle("Ratio R1/R2")

                    ratioplot.GetYaxis().SetNdivisions(505)
                    ratioplot.GetYaxis().SetTitleSize(20)
                    ratioplot.GetYaxis().SetTitleFont(43)
                    ratioplot.GetYaxis().SetTitleOffset(1.55)
                    ratioplot.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                    ratioplot.GetYaxis().SetLabelSize(15)

                    # X axis ratio plot settings
                    ratioplot.GetXaxis().SetTitle(XTitle)
                    ratioplot.GetXaxis().SetTitleSize(40)
                    ratioplot.GetXaxis().SetTitleFont(43)
                    ratioplot.GetXaxis().SetTitleOffset(4.)
                    ratioplot.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                    ratioplot.GetXaxis().SetLabelSize(15)

                    ratioplot.SetLineWidth(2)
                    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
                    c1.SaveAs(outFolder+hist+"_"+factor+"_"+h+".png")
                    ratioplot.Delete()
                    c1.Clear()
                combinedHist1=makeCombined(histos["Data"][0],histos["TTJets"][0],factor,"1")
                combinedHist2=makeCombined(histos["Data"][1],histos["TTJets"][1],factor,"2")
                ratioplot=ROOT.TRatioPlot(combinedHist1,combinedHist2,factor)

                pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
                #CMS_lumi.CMS_lumi(pad1, iPeriod, iPos)

                pad1.SetBottomMargin(0) # Upper and lower plot are joined
                pad1.SetGridx()         # Vertical grid
                pad1.Draw()
                pad1.cd()
                pad1.SetLogy()
                combinedHist1.SetStats(0)
                combinedHist1.SetTitle(factor+" (Data-MC)")
                combinedHist1.SetMinimum(.1)
                combinedHist1.GetYaxis().SetTitle("Events")

                #  TCP_l.Draw("same hist e")
                #  TCP_m.Draw("same hist e")
                #  TCP_h.Draw("same hist e")

                combinedHist1.SetLineColor(ROOT.kBlue)

                combinedHist2.SetLineColor(ROOT.kRed)
                combinedHist1.Draw("hist e1")
                combinedHist2.Draw("same hist e1")
                #SUSY_TH1F.Draw("same hist e1")

                l = ROOT.TLegend(0.65,0.7,0.85,0.87)

                l.AddEntry(combinedHist1, Ratios[factor][0], "l")
                l.AddEntry(combinedHist2, Ratios[factor][1], "l")
                l.Draw("same")

                c1.cd()

                pad2 = ROOT.TPad("pad2", "pad2", 0, 0.1, 1, 0.3)
                pad2.SetTopMargin(0)
                pad2.SetBottomMargin(0.26)
                pad2.SetGridx() # vertical grid
                pad2.Draw()
                pad2.cd()

                ratioplot.Draw("ep")

                #ratioplot.SetStats(0)

                # Y axis ratio plot settings
                ratioplot.GetYaxis().SetTitle("ratio R1/R2")

                ratioplot.GetYaxis().SetNdivisions(505)
                ratioplot.GetYaxis().SetTitleSize(20)
                ratioplot.GetYaxis().SetTitleFont(43)
                ratioplot.GetYaxis().SetTitleOffset(1.55)
                ratioplot.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                ratioplot.GetYaxis().SetLabelSize(15)

                # X axis ratio plot settings
                ratioplot.GetXaxis().SetTitle(XTitle)
                ratioplot.GetXaxis().SetTitleSize(40)
                ratioplot.GetXaxis().SetTitleFont(43)
                ratioplot.GetXaxis().SetTitleOffset(4.)
                ratioplot.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                ratioplot.GetXaxis().SetLabelSize(15)

                ratioplot.SetLineWidth(2)
                CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
                c1.SaveAs(outFolder+hist+"_"+factor+"_combined.png")
                c1.Clear()
                combinedHist1.Delete()
                combinedHist2.Delete()
                ratioplot.Delete()
                

makeVariablePlots()
