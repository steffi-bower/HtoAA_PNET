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
QCDFile =ROOT.TFile.Open(plotfolder+"20062024_MC_LeadingPNetScore_Matched_TTJets_2018_NTuple.root" ,"READ")

TTBarFile = ROOT.TFile.Open(plotfolder+"20062024_MC_LeadingPNetScore_Matched_TTJets_2018_NTuple.root" ,"READ")

DataFile = ROOT.TFile.Open(plotfolder+"20062024_DATA_LeadingPNetScore_Matched.root" ,"READ")

Background = ROOT.THStack("Background_Hists","")
qcd_pnet=QCDFile.Get("h_pNetFull")
ttjets_pnet=TTBarFile.Get("h_pNetFull")
data_pnet=DataFile.Get("h_pNetFull")
bkgint=(qcd_pnet.Integral(0,qcd_pnet.GetNbinsX()+2)+ttjets_pnet.Integral(0,ttjets_pnet.GetNbinsX()+2))
qcd_pnet.Scale(1./(bkgint))
ttjets_pnet.Scale(1./(bkgint))

qcd_pnet.SetFillColor(ROOT.kGray)
ttjets_pnet.SetFillColor(ROOT.kCyan)
Background.Add(qcd_pnet)
Background.Add(ttjets_pnet)
Background.SetTitle(" ; PNet Score; Jets/Total Jets;")


data_pnet.Scale(1./data_pnet.Integral(0,data_pnet.GetNbinsX()+2))

Background.Draw("hist")
data_pnet.Draw("hist same")

l = ROOT.TLegend(0.65,0.7,0.85,0.87)
l.AddEntry(qcd_pnet,"QCD BGen","f")
l.AddEntry(ttjets_pnet,"TTJets","f")

l.AddEntry(data_pnet, "2018 BPH Data", "l")

l.Draw("same")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)

c.SaveAs(outDir+"PNETSCORES.png")

Background_deep = ROOT.THStack("Background_deep","")

qcd_DeepFlav=QCDFile.Get("h_DeepFlav")
ttjets_DeepFlav=TTBarFile.Get("h_DeepFlav")
data_DeepFlav=DataFile.Get("h_DeepFlav")
qcd_DeepFlav.Rebin(50)
ttjets_DeepFlav.Rebin(50)
data_DeepFlav.Rebin(50)
bkgint=(qcd_DeepFlav.Integral(0,qcd_DeepFlav.GetNbinsX()+2)+ttjets_DeepFlav.Integral(0,ttjets_DeepFlav.GetNbinsX()+2))
qcd_DeepFlav.Scale(1./(bkgint))
ttjets_DeepFlav.Scale(1./(bkgint))

qcd_DeepFlav.SetFillColor(ROOT.kGray)
ttjets_DeepFlav.SetFillColor(ROOT.kCyan)
Background_deep.Add(qcd_DeepFlav)
Background_deep.Add(ttjets_DeepFlav)
Background_deep.SetTitle(" ; DeepFlav Score; Jets/Total Jets;")


data_DeepFlav.Scale(1./data_DeepFlav.Integral(0,data_DeepFlav.GetNbinsX()+2))

Background_deep.Draw("hist")
data_DeepFlav.Draw("hist same")

l = ROOT.TLegend(0.65,0.7,0.85,0.87)
l.AddEntry(qcd_DeepFlav,"QCD BGen","f")
l.AddEntry(ttjets_DeepFlav,"TTJets","f")

l.AddEntry(data_DeepFlav, "2018 BPH Data", "l")

l.Draw("same")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)

c.SaveAs(outDir+"DeepFlavSCORES.png")