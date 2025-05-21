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
plots=["Mvis","bMass","bDRl","DiTauPt","lepDR","MET","Trigger","BPH_Trigger","nEvent", "bPt","nB","nE","nTau","nMu"]
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
QCDFile =ROOT.TFile.Open(plotfolder+label+"_QCD_BGen_2018.root" ,"READ")
DYFile = ROOT.TFile.Open(plotfolder+label+"_DYJetsToLL_2018.root" ,"READ") 
WZFile = ROOT.TFile.Open(plotfolder+label+"_WZ_2018.root" ,"READ")
WJetsFile= ROOT.TFile.Open(plotfolder+label+"_WJetsToLNu_2018.root" ,"READ")
TTBarFile = ROOT.TFile.Open(plotfolder+label+"_TTJets_2018.root" ,"READ")
ZZTo4LFile = ROOT.TFile.Open(plotfolder+label+"_ZZTo4L_2018.root" ,"READ")
ZZFile = ROOT.TFile.Open(plotfolder+label+"_ZZ_2018.root" ,"READ")
WWFile = ROOT.TFile.Open(plotfolder+label+"_WW_2018.root" ,"READ")
WZTo3LNuFile = ROOT.TFile.Open(plotfolder+label+"_WZTo3LNu_2018.root" ,"READ")
SUSYFile = ROOT.TFile.Open(plotfolder+label+"_SUSY_2018.root" ,"READ")
Backgrounds = [

{"file":DYFile,"name":"DY_m-10","color":ROOT.kRed},
{"file":WZFile,"name":"WZ","color":ROOT.kBlue},
{"file":WJetsFile,"name":"WJets","color":ROOT.kGreen},
{"file":TTBarFile,"name":"TTBar","color":ROOT.kCyan},
{"file":QCDFile,"name":"QCD BGen","color":ROOT.kGray},
{"file":WWFile,"name":"WW","color":ROOT.kOrange}
]
c1 = ROOT.TCanvas("Delta RDelta RN","", 800, 850)





def makePlots(channel):
    for plot in plots:
        checkAndMakeDir(outDir+plot+"/")

        for sign in signs:

            hist = "h_"+channel+"_"+plot+"_"+sign
            
            if plot == "nEvent":
                if channel=="tauMu_tauE":
                    hist = "h_"+plot+"_tauE_tauMu"
                else:
                    hist = "h_"+plot+"_"+channel
            print(hist)
            SUSY_TH1F= SUSYFile.Get(hist)


            for back in Backgrounds:
                back["histo"]=back["file"].Get(hist)
                back["histo"].SetFillColor(back["color"])
            Backgrounds_Sorted = sorted(Backgrounds, key=lambda back:back["histo"].Integral(), reverse=True)


            Title = SUSY_TH1F.GetTitle()
            
            Background = ROOT.THStack("Background_"+channel+"_"+sign+"_"+plot,Title)


            print(channel+"test2")
            for back in Backgrounds_Sorted:
                print (back["name"]+" Integral = "+str(back["histo"].Integral())+"\n")
                Background.Add(back["histo"])

            bkg = Background.GetStack().Last()
            n = SUSY_TH1F.GetNbinsX()

            SOB=ROOT.TH1F("signal/sqrt(B)", plot , n, SUSY_TH1F.GetXaxis().GetXmin(), SUSY_TH1F.GetXaxis().GetXmax())
            for i in range (0,n+1):
                s=SUSY_TH1F.GetBinContent(i)
                b=bkg.GetBinContent(i)
                if(s>0 and b>0):
                    e = s/(b**.5)
                    SOB.SetBinContent(i,e)


            pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
            pad1.SetBottomMargin(0) # Upper and lower plot are joined
            pad1.SetGridx()         # Vertical grid
            pad1.Draw()             # Draw the upper pad: pad1
            pad1.cd()
            pad1.SetLogy()

            Background.SetMinimum(.1)

            Background.Draw("hist")
            #  TCP_l.Draw("same hist e")
            #  TCP_m.Draw("same hist e")
            #  TCP_h.Draw("same hist e")

            SUSY_TH1F.Draw("same hist e")



            SUSY_TH1F.SetLineColor(ROOT.kBlack)


            SUSY_TH1F.SetLineWidth(2)

            l = ROOT.TLegend(0.65,0.7,0.85,0.87)
            for back in Backgrounds_Sorted:
                l.AddEntry(back["histo"],back["name"],"f")

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