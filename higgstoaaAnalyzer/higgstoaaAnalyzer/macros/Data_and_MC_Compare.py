import ROOT
import sys
import subprocess
import string,math,os
import glob
import numpy as np
import tdrstyle, CMS_lumi
label = sys.argv [1]

tdrstyle.setTDRStyle()
ROOT.gROOT.SetBatch(True)

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod = 9

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref
T = 0.08*H_ref
B = 0.15*H_ref 
L = 0.15*W_ref
R = 0.08*W_ref

c = ROOT.TCanvas("c","c",50,50,W,H)
c.SetFillColor(0)
c.SetBorderMode(0)
c.SetFrameFillStyle(0)
c.SetFrameBorderMode(0)
c.SetLeftMargin( L/W )
c.SetRightMargin( R/W )
c.SetTopMargin( T/H )
c.SetBottomMargin( B/H )
c.SetTickx(0)
c.SetTicky(0)
CMS_lumi.CMS_lumi(c, iPeriod, iPos)

plotfolder = "/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/"
outDir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/graphs/"+label+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)      
checkAndMakeDir(outDir)
QCDFile =ROOT.TFile.Open(plotfolder+"12122024_DDT_SSNOMBIDRevTau_QCD_BGen_2018_NTuple.root" ,"READ")

TTBarFile = ROOT.TFile.Open(plotfolder+"12122024_DDT_SSNOMBIDRevTau_TTJets_2018_NTuple.root" ,"READ")
SigFile = ROOT.TFile.Open(plotfolder+"12122024_DDT_SSNOMBIDRevTau_SUSY_2018_NTuple.root" ,"READ")
DataFile = ROOT.TFile.Open(plotfolder+"20112024_Data_NominalBidSS_RevTau_SIGNAL.root" ,"READ")

Background = ROOT.THStack("Background_Hists","")
qcd=QCDFile.Get("h_tauHad_tauMu_Mvis_isBPH")
ttjets=TTBarFile.Get("h_tauHad_tauMu_Mvis_isBPH")
data=DataFile.Get("h_tauHad_tauMu_Mvis_isBPH")
sig=SigFile.Get("h_tauHad_tauMu_Mvis_isBPH")

qcd.SetFillColor(ROOT.kGray)
ttjets.SetFillColor(ROOT.kCyan)

data.SetLineColor(ROOT.kRed)
Background.Add(qcd)
Background.Add(ttjets)
Background.GetXaxis().SetTitle("#mu #tau _{had}M_{vis} (GeV)")
Background.GetYaxis().SetTitle("Events")
data.Draw("hist e")
Background.Draw("hist e")
sig.Draw("hist same e")

l = ROOT.TLegend(0.55,0.7,0.75,0.87)
l.AddEntry(qcd,"QCD BGen","f")
l.AddEntry(ttjets,"TTJets","f")
l.AddEntry(sig, "Signal m_{a} = 12 GeV", "l")
l.AddEntry(data, "2018 BPH Data", "l")
ROOT.gPad.SetLogy()
l.Draw("same")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)

c.SaveAs(outDir+"MVis.png")

