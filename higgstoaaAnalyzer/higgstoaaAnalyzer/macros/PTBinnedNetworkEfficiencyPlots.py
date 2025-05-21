import ROOT
import sys
import subprocess
import string,math,os
import glob
import numpy as np
import tdrstyle, CMS_lumi


label = sys.argv [1]

wps = ["80","85","90"]
networks = ["h_pNetMerged_pt_WP", "h_deepFlavmerged_pt_WP"]
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


inFile = ROOT.TFile.Open(plotfolder+label+"_SUSY_2018_NTuple.root" ,"READ")
JetPT=inFile.Get("h_Merged_pt")
for network in networks:
    for wp in wps:
        
        cutHist=inFile.Get(network+wp)

        EfficiencyHist=ROOT.TEfficiency(cutHist,JetPT)
        EfficiencyHist.SetTitle(" ; p_{T} GeV; Efficiency;")
        EfficiencyHist.Draw()
        c.cd()
        c.Update()
        c.RedrawAxis()
        frame = c.GetFrame()
        frame.Draw()
        c.SaveAs(outDir+network+wp+".png")
        c.Clear()

