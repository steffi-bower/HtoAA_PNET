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
    #["lep1Pt","lep1 p_{T} (GeV)"],
    #["lep2Pt","lep2 p_{T} (GeV)"],
    #["mergedLepPt", "Reco Di#tau  p_{T} (GeV)"],
    #["mergedBPt", "Reco bb  p_{T} (GeV)"]
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
    "AR": {"Data":ROOT.TFile.Open(plotfolder+"07052025_AR_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"21102024_MC_ReversedBidOS_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"21102024_MC_ReversedBidOS_SUSY_2018_NTuple.root")},

    # "V_DR_NOM": {"Data":ROOT.TFile.Open(plotfolder+"ParkingBPH_21042025_DRNom_V_emu_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSNOMBIDRevTau_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSNOMBIDRevTau_SUSY_2018_NTuple.root")},
    # "V_DR_ALT": {"Data":ROOT.TFile.Open(plotfolder+"21042025_DRALT_V_emu_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSRevBIDRevTau_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_SSRevBIDRevTau_SUSY_2018_NTuple.root")},
    # "V_AR": {"Data":ROOT.TFile.Open(plotfolder+"20042025_AR_V_emu_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSRevBIDRevTau_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSRevBIDRevTau_SUSY_2018_NTuple.root")},
    # "V_SR": {"Data":ROOT.TFile.Open(plotfolder+"20042025_SR_V_emu_SIGNAL.root"),"TTJets":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSNOMBIDRevTau_genmatch_metfix_TTJets_2018_NTuple.root"),"SUSY":ROOT.TFile.Open(plotfolder+"12122024_DDT_OSNOMBIDRevTau_genmatch_metfix_SUSY_2018_NTuple.root")}

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

    r1vr2=ROOT.TH1F("Ratios_"+Factor, "" , n, Region1.GetXaxis().GetXmin(), Region1.GetXaxis().GetXmax())
    r1vr2.SetStats(0)
    for i in range (0,n+1):
        r1=Region1.GetBinContent(i)
        e1=Region1.GetBinError(i)

        r2=Region2.GetBinContent(i)
        e2=Region2.GetBinError(i)

        if(r1>0 and r2>0):
            r = r1/r2
            error= r*((e1/r1)**2+(e2/r2)**2)**.5
            r1vr2.SetBinContent(i,r)
            r1vr2.SetBinError(i,error)
    return r1vr2
def makeCombined(Region1,Region2,Factor,tag):

    n = Region1.GetNbinsX()
    Combined=ROOT.TH1F("Combined_"+tag, Factor+tag+" combined" , n, Region1.GetXaxis().GetXmin(), Region1.GetXaxis().GetXmax())
    for i in range (0,n+1):
        r1=Region1.GetBinContent(i)
        e1=Region1.GetBinError(i)

        r2=Region2.GetBinContent(i)
        e2=Region2.GetBinError(i)

        Combined.SetBinContent(i,r1-r2)
        Combined.SetBinError(i,(e1**2+e2**2)**.5)

    return Combined
Backgrounds={"TTJets":ROOT.kMagenta,"WW":ROOT.kRed,"WZ":ROOT.kBlue,"WJetsToLNu":ROOT.kGreen,"DYJets":ROOT.kCyan}
#def makeStack():

def makeVariablePlots():
    ff_hists={}
    for factor in Ratios.keys():
        checkAndMakeDir(outDir+"/"+factor)
        ff_hists[factor]={}

        for channel in channels:
            checkAndMakeDir(outDir+"/"+factor+"/"+channel)
            ff_hists[factor][channel]={}

            for variable in variables:
                outFolder=outDir+"/"+factor+"/"+channel+"/"
                hist="h_"+channel+"_"+variable[0]+"_isBPH"
                XTitle = variable[1] + " "+titles[channel]
                histos ={
                    "Data":[Files[Ratios[factor][0]]["Data"].Get(hist),Files[Ratios[factor][1]]["Data"].Get(hist)],
                    "TTJets":[Files[Ratios[factor][0]]["TTJets"].Get(hist),Files[Ratios[factor][1]]["TTJets"].Get(hist)],
                    "Signal":[Files[Ratios[factor][0]]["SUSY"].Get(hist),Files[Ratios[factor][1]]["SUSY"].Get(hist)]
                }
                histos["Combined"]=[makeCombined(histos["Data"][0],histos["TTJets"][0],factor,"1"),makeCombined(histos["Data"][1],histos["TTJets"][1],factor,"2")]

                for h in histos.keys():
                    ff_hists[factor][channel][variable[0]]={}

                    print(h)
                    histos[h][0].SetStats(0)
                    histos[h][0].SetTitle(" ")

                    histos[h][0].SetMinimum(.1)
                    histos[h][0].GetYaxis().SetTitle("Events")
                    histos[h][0].GetYaxis().SetNdivisions(505)
                    histos[h][0].GetYaxis().SetTitleSize(23)
                    histos[h][0].GetYaxis().SetTitleFont(43)
                    histos[h][0].GetYaxis().SetTitleOffset(1.45)
                    histos[h][0].GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                    histos[h][0].GetYaxis().SetLabelSize(18)

                    # X axis ratio plot settings

                    histos[h][0].GetXaxis().SetTitle(XTitle)
                    histos[h][0].LabelsDeflate()

                    #  TCP_l.Draw("same hist e")
                    #  TCP_m.Draw("same hist e")
                    #  TCP_h.Draw("same hist e")
                    if "mergedLepPt"==variable[0]:
                        histos[h][0].GetXaxis().SetRangeUser(0,110)
                        histos[h][1].GetXaxis().SetRangeUser(0,110)
                    if "mergedBPt"==variable[0]:
                        histos[h][0].GetXaxis().SetRangeUser(0,250)
                        histos[h][1].GetXaxis().SetRangeUser(0,250)
                    ff_hists[factor][channel][variable[0]][h]=makeRatios(histos[h][0],histos[h][1] ,factor+variable[0]+channel)
                    ff_hists[factor][channel][variable[0]][h].GetXaxis().SetTitle(XTitle)
                    ff_hists[factor][channel][variable[0]][h].GetYaxis().SetTitle("Ratio")
                    #ff_hists[factor][channel][variable[0]].LabelsDeflate()

                    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
                    pad1.SetBottomMargin(0) # Upper and lower plot are joined
                    pad1.SetGridx()         # Vertical grid
                    pad1.Draw()             # Draw the upper pad: pad1
                    pad1.cd()
                    pad1.SetLogy()
                    histos[h][0].SetLineColor(ROOT.kBlue)
                    
                    histos[h][1].SetLineColor(ROOT.kRed)
                    histos[h][0].Draw("hist E")
                    histos[h][1].Draw("same hist E")
                    l = ROOT.TLegend(0.65,0.7,0.85,0.87)

                    l.AddEntry(histos[h][0], Ratios[factor][0], "l")
                    l.AddEntry(histos[h][1], Ratios[factor][1], "l")
                    l.Draw("same")
                    c1.cd()

                    pad2 = ROOT.TPad("pad2", "pad2", 0, 0, 1, 0.3)
                    pad2.SetTopMargin(0)
                    pad2.SetBottomMargin(0.2)
                    pad2.SetGridx() # vertical grid
                    pad2.GetFrame().SetY1(0)
                    pad2.GetFrame().SetY2(3.5)
                    pad2.Draw()
                    pad2.cd()
                    SOB=makeRatios(histos[h][0],histos[h][1] ,"tmp")
                    SOB.Draw("ep")

                    SOB.SetTitle("")
                    SOB.SetStats(0)
                    SOB.SetMinimum(0)
                    SOB.SetMaximum(5)
                    # Y axis ratio plot settings
                    SOB.GetYaxis().SetTitle("Ratio")
                    SOB.GetYaxis().SetNdivisions(505)
                    SOB.GetYaxis().SetTitleSize(23)
                    SOB.GetYaxis().SetTitleFont(43)
                    SOB.GetYaxis().SetTitleOffset(1.45)
                    SOB.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                    SOB.GetYaxis().SetLabelSize(18)

                    # X axis ratio plot settings
                    SOB.GetXaxis().SetTitle(XTitle)
                    SOB.GetXaxis().SetTitleSize(23)
                    SOB.GetXaxis().SetTitleFont(43)
                    SOB.GetXaxis().SetTitleOffset(3)
                    SOB.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                    SOB.GetXaxis().SetLabelSize(18)

                    SOB.SetLineWidth(2)
                    #SUSY_TH1F.Draw("same hist e1")
                    # ratioplot=ROOT.TRatioPlot(histos[h][0],histos[h][1])



                    # ratioplot.Draw("")
                    # ratioplot.GetUpperPad().SetLogy()
                    # ratioplot.GetLowerRefYaxis().SetTitle("Ratio")
                    # ratioplot.GetLowerPad().GetFrame().SetY1(0)
                    # ratioplot.GetLowerPad().GetFrame().SetY2(3.5)
                    # ratioplot.GetUpperPad().cd()


                    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
                    c1.SaveAs(outFolder+hist+"_"+factor+"_"+h+".png")
                    SOB.Delete()
                    c1.Clear()
              
                
    checkAndMakeDir(outDir+"/FakeFactorPlots/")
    checkAndMakeDir(outDir+"/Closure/")
    checkAndMakeDir(outDir+"/Transfer/")
    for channel in channels:
        for variable in variables:
            for h in ff_hists["FF"][channel][variable[0]].keys():
                ff_hists["FF"][channel][variable[0]][h].GetYaxis().SetTitle("Fake Factor")
                ff_hists["FF"][channel][variable[0]][h].SetLineColor(ROOT.kRed)
                ff_hists["FF1"][channel][variable[0]][h].SetLineColor(ROOT.kBlue)
                ff_hists["FF2"][channel][variable[0]][h].SetLineColor(ROOT.kOrange)
                ff_hists["FF"][channel][variable[0]][h].Draw(" e")
                ff_hists["FF1"][channel][variable[0]][h].Draw("same  e")
                ff_hists["FF2"][channel][variable[0]][h].Draw("same  e")
                l = ROOT.TLegend(0.75,0.7,0.85,0.87)
                l.AddEntry(ff_hists["FF"][channel][variable[0]][h],"FF", "l")
                l.AddEntry(ff_hists["FF1"][channel][variable[0]][h],"FF1", "l")
                l.AddEntry(ff_hists["FF2"][channel][variable[0]][h],"FF2", "l")
                l.Draw("same")


                CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
                c1.SaveAs(outDir+"/FakeFactorPlots/"+channel+"_"+variable[0]+"_FakeFactors.png")
                c1.Clear()
                ff_hists["Closure_DRNom"][channel][variable[0]][h].GetYaxis().SetTitle("Validation/Nominal Iso")
                ff_hists["Closure_DRNom"][channel][variable[0]][h].SetLineColor(ROOT.kRed)
                ff_hists["Closure_DRALT"][channel][variable[0]][h].SetLineColor(ROOT.kBlue)
                ff_hists["Closure_AR"][channel][variable[0]][h].SetLineColor(ROOT.kOrange)
                ff_hists["Closure_DRNom"][channel][variable[0]][h].Draw(" e")
                ff_hists["Closure_DRALT"][channel][variable[0]][h].Draw("same  e")
                ff_hists["Closure_AR"][channel][variable[0]][h].Draw("same  e")
                l = ROOT.TLegend(0.75,0.7,0.85,0.87)
                l.AddEntry(ff_hists["Closure_DRNom"][channel][variable[0]][h],"DRNom", "l")
                l.AddEntry(ff_hists["Closure_DRALT"][channel][variable[0]][h],"DRLT", "l")
                l.AddEntry(ff_hists["Closure_AR"][channel][variable[0]][h],"AR", "l")
                l.Draw("same")


                CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
                c1.SaveAs(outDir+"/Closure/"+channel+"_"+variable[0]+"_ValidationCHECKS.png")
                c1.Clear()            
                ff_hists["Transfer_RevID"][channel][variable[0]][h].GetYaxis().SetTitle("OS/SS")

                ff_hists["Transfer_RevID"][channel][variable[0]][h].SetLineColor(ROOT.kRed)
                ff_hists["Transfer_RevID_V"][channel][variable[0]][h].SetLineColor(ROOT.kBlue)
                ff_hists["Transfer_NomID_V"][channel][variable[0]][h].SetLineColor(ROOT.kOrange)

                ff_hists["Transfer_RevID"][channel][variable[0]][h].Draw(" e")
                ff_hists["Transfer_RevID_V"][channel][variable[0]][h].Draw("same  e")
                ff_hists["Transfer_NomID_V"][channel][variable[0]][h].Draw("same  e")
                l = ROOT.TLegend(0.75,0.7,0.85,0.87)
                l.AddEntry(ff_hists["Transfer_RevID"][channel][variable[0]][h],"RevBID", "l")
                l.AddEntry(ff_hists["Transfer_RevID_V"][channel][variable[0]][h],"RevBID V", "l")
                l.AddEntry(ff_hists["Transfer_NomID_V"][channel][variable[0]][h],"NomBID V", "l")
                l.Draw("same")


                CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
                c1.SaveAs(outDir+"/Transfer/"+channel+"_"+variable[0]+"_OSVSS.png")
                c1.Clear()

makeVariablePlots()
