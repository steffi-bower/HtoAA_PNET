import ROOT
import sys
import subprocess
import string,math,os
import glob
import numpy as np
import tdrstyle, CMS_lumi

ROOT.gROOT.SetBatch(True)

label = sys.argv [1]
tag = sys.argv [2]
#hists = ["h_tauE_tauE_Mvis_EG" ,"h_tauE_tauE_Mvis_EGorDoubleEG","h_tauE_tauE_Mvis_noTrig","h_tauMu_tauE_Mvis_SingleMu", "h_tauMu_tauE_Mvis_EGorSingleMu" ,"h_tauMu_tauE_Mvis_MuEGorSingleMu" ,"h_tauMu_tauE_Mvis_noTrig", "h_tauMu_tauMu_Mvis_SingleMu", "h_tauMu_tauMu_Mvis_SingleMuorDoubleMu","h_tauMu_tauMu_Mvis_noTrig"]
#hists = ["h_MET"]

histos= [
    "h_ditauID",
    "h_NdiTau",
    "h_taupt",
    "h_diTau_b1_PNetID",
    "h_diTau_Mvis",
    "h_diTau_bMass",
    "h_diTau_tauDRB",
    "h_diTau_MET",
    "h_diTau_NEles",
    "h_diTau_NMus"
    ]
muonTrigs= [("isBPH",ROOT.kMagenta),("isIsoMu",ROOT.kMagenta),("isDoubleMuSS",ROOT.kRed), ("isDoubleMuMass8",ROOT.kBlue),("isDoubleMuMass3p8",ROOT.kGreen),("isDoubleMu",ROOT.kCyan)]
electronTrigs =  [("isBPH",ROOT.kMagenta),("isIsoEle",ROOT.kRed),("isMuonEG",ROOT.kBlue),("isDoubleEG",ROOT.kGreen)]

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 }"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_sqrtS = "33.6fb^{-1}" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod = 9

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.15
plotfolder = "/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/"
outDir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/graphs/"+label+"_"+tag+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)      
checkAndMakeDir(outDir)
QCDFile =ROOT.TFile.Open(plotfolder+label+"_QCD_BGen_2018_NTuple.root" ,"READ")

TTBarFile = ROOT.TFile.Open(plotfolder+label+"_TTJets_2018_NTuple.root" ,"READ")

SUSYFile = ROOT.TFile.Open(plotfolder+label+"_SUSY_2018_NTuple.root" ,"READ")
Backgrounds = [

{"file":TTBarFile,"name":"TTBar","color":ROOT.kCyan},
{"file":QCDFile,"name":"QCD BGen","color":ROOT.kGray},
]
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

def makeVariablePlots():
    integrals=[]
    for hist in histos:
                print (hist)
                SUSY_TH1F=SUSYFile.Get(hist)
                firststep=True
                if firststep:
                    integrals.append(["SUSY", "DiTau", SUSY_TH1F.Integral()])

                for back in Backgrounds:
                    back["histo"]=back["file"].Get(hist)
                    #back["histo"].Scale(33.7e3)
                    if firststep:
                        integrals.append([back["name"], "DiTau", back["histo"].Integral()])

                    back["histo"].SetFillColor(back["color"])
                firststep=False
                Backgrounds_Sorted = sorted(Backgrounds, key=lambda back:back["histo"].Integral(), reverse=True)


                Title = SUSY_TH1F.GetTitle()
                
                Background = ROOT.THStack("Background_"+hist,"")
                Background.SetTitle(" ;Y axis; Events")

                for back in Backgrounds_Sorted:
                    print (back["name"]+" Integral = "+str(back["histo"].Integral(2,5))+"\n")
                    Background.Add(back["histo"])
                print ("Signal"+" Integral = "+str(SUSY_TH1F.Integral(2,5))+"\n")
                bkg = Background.GetStack().Last()
                n = SUSY_TH1F.GetNbinsX()
                bkgnEvents=0
                SOB=ROOT.TH1F("signal/sqrt(B)", hist+"_SOB" , n, SUSY_TH1F.GetXaxis().GetXmin(), SUSY_TH1F.GetXaxis().GetXmax())
                bins = []
                for i in range (0,n+1):
                    s=SUSY_TH1F.GetBinContent(i)

                    b=bkg.GetBinContent(i)
                    bkgnEvents+=b
                    if(s>0 and b>0):
                        e = s/(b**.5)
                        SOB.SetBinContent(i,e)
                        bins.append([i,e])


                pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
                #CMS_lumi.CMS_lumi(pad1, iPeriod, iPos)

                pad1.SetBottomMargin(0) # Upper and lower plot are joined
                pad1.SetGridx()         # Vertical grid
                pad1.Draw()
                pad1.cd()
                pad1.SetLogy()

                Background.SetMinimum(.1)
                SUSY_TH1F.GetYaxis().SetTitle("Events")

                signEvents =SUSY_TH1F.Integral()
                fullSOB= signEvents/(bkgnEvents**.5)

                #  TCP_l.Draw("same hist e")
                #  TCP_m.Draw("same hist e")
                #  TCP_h.Draw("same hist e")

                SUSY_TH1F.SetMarkerStyle(ROOT.kFullCircle)
                SUSY_TH1F.SetLineColor(ROOT.kBlack)
                Background.Draw("hist")

                SUSY_TH1F.Draw("same hist e1")

                #SUSY_TH1F.Draw("same hist e1")

                l = ROOT.TLegend(0.65,0.7,0.85,0.87)
                for back in Backgrounds_Sorted:
                    l.AddEntry(back["histo"],back["name"],"f")

                l.AddEntry(SUSY_TH1F, "Signal m_{a} = 12 GeV", "l")

                l.Draw("same")

                c1.cd()

                pad2 = ROOT.TPad("pad2", "pad2", 0, 0.1, 1, 0.3)
                pad2.SetTopMargin(0)
                pad2.SetBottomMargin(0.26)
                pad2.SetGridx() # vertical grid
                pad2.Draw()
                pad2.cd()

                SOB.Draw("ep")

                SOB.SetStats(0)

                # Y axis ratio plot settings
                SOB.GetYaxis().SetTitle("ratio S/#sqrt{B}")
                SOB.GetXaxis().SetTitle(Title)

                SOB.GetYaxis().SetNdivisions(505)
                SOB.GetYaxis().SetTitleSize(20)
                SOB.GetYaxis().SetTitleFont(43)
                SOB.GetYaxis().SetTitleOffset(1.55)
                SOB.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                SOB.GetYaxis().SetLabelSize(15)

                # X axis ratio plot settings
                SOB.GetXaxis().SetTitle()
                SOB.GetXaxis().SetTitleSize(20)
                SOB.GetXaxis().SetTitleFont(43)
                SOB.GetXaxis().SetTitleOffset(4.)
                SOB.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                SOB.GetXaxis().SetLabelSize(15)

                SOB.SetLineWidth(2)
                CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
                c1.SaveAs(outDir+hist+".png")
                c1.Clear()
 
    #print("INTEGRALS")
    #chan=""
    #for integral in integrals:
    #    if integral[1]!=chan:
    #        print ("CHANNEL = "+ integral[1])
    #        chan=integral[1]
    #    print (integral[0]+ ": " +str(round(integral[2],2)))
    #print(integrals)
makeVariablePlots()
