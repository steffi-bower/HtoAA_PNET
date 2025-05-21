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
QCDFile =ROOT.TFile.Open(plotfolder+"02022025_SR_V_MC_QCD_PtBin_2018_NTuple.root" ,"READ")
TTBarFile = ROOT.TFile.Open(plotfolder+"02022025_SR_V_MC_TTJets_2018_NTuple.root" ,"READ")
SigFile = ROOT.TFile.Open(plotfolder+"02022025_SR_V_MC_SUSY_2018_NTuple.root" ,"READ")

qcd=QCDFile.Get("h_DeepFlav_bb_Fake_100plus")
ttjets=TTBarFile.Get("h_DeepFlav_bb_Fake_100plus")
sig=SigFile.Get("h_DeepFlav_bb_Merged_100plus")
qcd.Scale(1/qcd.Integral())
ttjets.Scale(1/ttjets.Integral())
sig.Scale(1/sig.Integral())
qcd.Rebin(2000)
ttjets.Rebin(2000)
sig.Rebin(2000)
qcd.SetLineColor(ROOT.kOrange)
ttjets.SetLineColor(ROOT.kCyan)
sig.SetLineColor(ROOT.kBlack)
sig.GetXaxis().SetTitle("DeepJet bb Node Score p_{T} > 100 GeV")
sig.GetYaxis().SetTitle("A.U.")
sig.Draw("hist e")
ttjets.Draw("hist same e")
qcd.Draw("hist same e")
l = ROOT.TLegend(0.55,0.7,0.75,0.87)
l.AddEntry(qcd,"QCD BGen","l")
l.AddEntry(ttjets,"TTJets","l")
l.AddEntry(sig, "Signal m_{a} = 12 GeV", "l")
#ROOT.gPad.SetLogy()
l.Draw("same")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)

c.SaveAs(outDir+"deepFlav_bb_100plus.png")

