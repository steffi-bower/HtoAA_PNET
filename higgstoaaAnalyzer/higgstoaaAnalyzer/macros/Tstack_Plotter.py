import ROOT
import sys
import subprocess
import string,math,os
import ConfigParser
import glob
import numpy as np
ROOT.gROOT.SetBatch(True)

label = sys.argv [1]
tag = sys.argv [2]
#hists = ["h_tauE_tauE_Mvis_EG" ,"h_tauE_tauE_Mvis_EGorDoubleEG","h_tauE_tauE_Mvis_noTrig","h_tauMu_tauE_Mvis_SingleMu", "h_tauMu_tauE_Mvis_EGorSingleMu" ,"h_tauMu_tauE_Mvis_MuEGorSingleMu" ,"h_tauMu_tauE_Mvis_noTrig", "h_tauMu_tauMu_Mvis_SingleMu", "h_tauMu_tauMu_Mvis_SingleMuorDoubleMu","h_tauMu_tauMu_Mvis_noTrig"]
#hists = ["h_MET"]
signs=["OS","SS"]
plots=["Mvis","bMass","bDRl","DiTauPt","lepDR","MET"]
channels=["tauE_tauE","tauMu_tauMu","tauMu_tauE","tauHad_tauE","tauHad_tauMu"]

plotfolder = "/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/"
outDir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/graphs/"+label+"_"+tag+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)      
checkAndMakeDir(outDir)
QCDFile =ROOT.TFile.Open(plotfolder+label+"_QCD.root" ,"READ")
DYFile = ROOT.TFile.Open(plotfolder+label+"_DY_Full.root" ,"READ") 
WZFile = ROOT.TFile.Open(plotfolder+label+"_WZ.root" ,"READ")
WJetsFile= ROOT.TFile.Open(plotfolder+label+"_WJets.root" ,"READ")
TTBarFile = ROOT.TFile.Open(plotfolder+label+"_TTJets.root" ,"READ")
SUSYFile = ROOT.TFile.Open(plotfolder+label+"_SUSY.root" ,"READ")
c1 = ROOT.TCanvas("Delta RDelta RN","", 800, 850)

checkAndMakeDir(outDir+"NEvents"+"/")




def makePlots(channel):
    for plot in plots:
        checkAndMakeDir(outDir+plot+"/")

        for sign in signs:
            if ("tauHad" in channel):
                hist = "h_"+channel+"_"+plot
            else:
                hist = "h_"+channel+"_"+plot+"_"+sign
            print(hist)
            QCD_TH1F= QCDFile.Get(hist)
            QCD_TH1F.SetFillColor(ROOT.kOrange)
            n = 1
            if (QCD_TH1F.GetNbinsX()%2==0):
                n = 2
            elif((QCD_TH1F.GetNbinsX()%3==0)):
                n=3
            QCD_TH1F.Rebin(n)
            SUSY_TH1F= SUSYFile.Get(hist)
            SUSY_TH1F.Rebin(n)
            DY_TH1F= DYFile.Get(hist)
            DY_TH1F.SetFillColor(ROOT.kRed)
            DY_TH1F.Rebin(n)
            WJets_TH1F= WJetsFile.Get(hist)
            WJets_TH1F.SetFillColor(ROOT.kGreen)
            WJets_TH1F.Rebin(n)      
            TTBar_TH1F= TTBarFile.Get(hist)
            TTBar_TH1F.SetFillColor(ROOT.kBlue)
            TTBar_TH1F.Rebin(n)
            WZ_TH1F= WZFile.Get(hist)
            WZ_TH1F.SetFillColor(ROOT.kCyan)
            WZ_TH1F.Rebin(n)
            Title = SUSY_TH1F.GetTitle()
            
            Background = ROOT.THStack("Background_"+channel+"_"+sign+"_"+plot,Title)
            #if(channel=="tauE_tauE" or "tauMu_tauMu"):
            #    print(channel+"test1")
            #    Background.Add(DY_TH1F)
            #    Background.Add(TTBar_TH1F)
            #    Background.Add(QCD_TH1F)
            #    Background.Add(WJets_TH1F)
            #    Background.Add(WZ_TH1F)

            print(channel+"test2")
            Background.Add(DY_TH1F)

            Background.Add(TTBar_TH1F)
            Background.Add(QCD_TH1F)
            Background.Add(WJets_TH1F)
            Background.Add(WZ_TH1F)
            bkg = Background.GetStack().Last()
            n = SUSY_TH1F.GetNbinsX()

            SOB=ROOT.TH1F("signal/sqrt(B)", plot , n, SUSY_TH1F.GetXaxis().GetXmin(), SUSY_TH1F.GetXaxis().GetXmax())
            for i in range (0,n):
                s=SUSY_TH1F.GetBinContent(i)
                b=bkg.GetBinError(i)
                if(s>0 and b>0):
                    e = s/b
                    SOB.SetBinContent(i,e)


            pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
            pad1.SetBottomMargin(0) # Upper and lower plot are joined
            pad1.SetGridx()         # Vertical grid
            pad1.Draw()             # Draw the upper pad: pad1
            pad1.cd()
            pad1.SetLogy()

            Background.SetMinimum(1)

            Background.Draw("hist")
            #  TCP_l.Draw("same hist e")
            #  TCP_m.Draw("same hist e")
            #  TCP_h.Draw("same hist e")

            SUSY_TH1F.Draw("same hist e")



            SUSY_TH1F.SetLineColor(ROOT.kBlack)


            SUSY_TH1F.SetLineWidth(2)

            l = ROOT.TLegend(0.65,0.7,0.85,0.87)
            l.AddEntry(TTBar_TH1F, "TTJets", "f")
            l.AddEntry(QCD_TH1F, "QCD_FullHT", "f")
            l.AddEntry(WZ_TH1F, "WZ", "f")
            l.AddEntry(DY_TH1F, "DYJetsToLL_M-10", "f")
            l.AddEntry(WJets_TH1F, "WJets", "f")

            #  l.AddEntry(TCP_l, "TCP m_{a} = 50 GeV (HT-0to100)", "l")
            #  l.AddEntry(TCP_m, "TCP m_{a} = 50 GeV (HT-1000to400)", "l")
            #  l.AddEntry(TCP_h, "TCP m_{a} = 50 GeV (HT-400toInf)", "l")
            l.AddEntry(SUSY_TH1F, "Signal m_{a} = 12 GeV", "l")

            l.Draw("same")

            c1.cd()

            pad2 = ROOT.TPad("pad2", "pad2", 0, 0.1, 1, 0.3)
            pad2.SetTopMargin(0)
            pad2.SetBottomMargin(0.2)
            pad2.SetGridx() # vertical grid
            pad2.Draw()
            pad2.cd()

            SOB.Draw("ep")

            SOB.SetTitle("")
            SOB.SetStats(0)

            # Y axis ratio plot settings
            SOB.GetYaxis().SetTitle("ratio S/#sqrt{B}")
            SOB.GetYaxis().SetNdivisions(505)
            SOB.GetYaxis().SetTitleSize(20)
            SOB.GetYaxis().SetTitleFont(43)
            SOB.GetYaxis().SetTitleOffset(1.55)
            SOB.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
            SOB.GetYaxis().SetLabelSize(15)

            # X axis ratio plot settings
            #   SOB-GetXaxis().SetTitle("M_{e#mu}")
            SOB.GetXaxis().SetTitleSize(20)
            SOB.GetXaxis().SetTitleFont(43)
            SOB.GetXaxis().SetTitleOffset(4.)
            SOB.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
            SOB.GetXaxis().SetLabelSize(15)

            SOB.SetLineWidth(2)

            c1.SaveAs(outDir+plot+"/"+hist+".png")
            c1.Clear()


for chan in channels:
    makePlots(chan)