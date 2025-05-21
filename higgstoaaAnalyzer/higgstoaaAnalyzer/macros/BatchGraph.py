import ROOT
import sys
import subprocess
import string,math,os
import glob
import numpy as np
import tdrstyle, CMS_lumi
label = sys.argv [1]
normalize = sys.argv[2]

tdrstyle.setTDRStyle()
ROOT.gROOT.SetBatch(True)

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod = 9

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
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
inFile = ROOT.TFile.Open(label+".root" ,"READ")
outDir = "higgstoaaAnalyzer/graphs/"+label+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)      
checkAndMakeDir(outDir)
#clearDir(outDir)
def plotAllSimple():
    TDir=inFile.Get("simple") 

    for h in TDir.GetListOfKeys():
        h = h.ReadObj()
        HistType=h.ClassName()
        HistName=h.GetName()
        hist=TDir.Get(HistName)
        title = hist.GetTitle()
        hist.GetXaxis().SetTitle(title)
        hist.LabelsDeflate()
        hist.SetMinimum(0)
        if(HistType=="TH2F"):
            hist.Draw("COLZ")
        else:
            hist.Draw()

        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        c.cd()
        c.Update()
        c.RedrawAxis()
        frame = c.GetFrame()
        frame.Draw()
        c.SaveAs(outDir+HistName+".png")
        if("selection" in HistName or "nEvent" in HistName or "Trigger" in HistName):
            hist.SetMinimum(1000)
            hist.Draw()
            ROOT.gPad.SetLogy()
            c.SaveAs(outDir+HistName+"Log.png")
            ROOT.gPad.SetLogy(0)

        c.Clear()

        
def plotAllScaled():
    for h in inFile.GetListOfKeys():
        h = h.ReadObj()
        HistType=h.ClassName()
        HistName=h.GetName()
        hist=inFile.Get(HistName)
        title = hist.GetTitle()
        #if("selection" in HistName or "nEvent" in HistName):
        #    print("hi")
        #else:
        #hist.GetXaxis().SetTitle(title)
        hist.LabelsDeflate()
        hist.SetMinimum(0)
        if(HistType=="TH2F"):
            hist.Draw("COLZ")
        else:
            hist.Draw()

        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        c.cd()
        c.Update()
        c.RedrawAxis()
        frame = c.GetFrame()
        frame.Draw()
        c.SaveAs(outDir+HistName+".png")
        if("selection" in HistName or "nEvent" in HistName):
            hist.SetMinimum( 1)
            hist.Draw()
            ROOT.gPad.SetLogy()
            c.SaveAs(outDir+HistName+"Log.png")
            ROOT.gPad.SetLogy(0)

        c.Clear()
def plotAllSkimmed():
    totalevents= inFile.Get("h_nEvents").GetBinContent(2)

    for h in inFile.GetListOfKeys():
        h = h.ReadObj()
        HistType=h.ClassName()
        HistName=h.GetName()
        #if ("EventSel" not in HistName or "gen" in HistName): continue
        hist=inFile.Get(HistName)
        if hist.Integral()!=0 and normalize==1:
            hist.Scale(1/hist.Integral())
        title = hist.GetTitle()
        hist.GetXaxis().SetTitle(title)
        #if (HistType!="TH2F"):
        #    hist.Scale(2.263/totalevents)

        #if("selection" in HistName or "nEvent" in HistName):
        #    print("hi")
        #else:
        #hist.GetXaxis().SetTitle(title)
        hist.LabelsDeflate()
        hist.SetMinimum(0)
        if hist.GetNbinsX()>100:
            hist.Rebin(50)
        if(HistType=="TH2F"):
            #hist.RebinX(4)
            #hist.GetXaxis().SetRange(0,10)
            hist.Draw("COLZ")
        else:
            #hist.Draw("TEXT")
            hist.Draw("h")

        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        c.cd()
        c.Update()
        c.RedrawAxis()
        frame = c.GetFrame()
        frame.Draw()
        c.SaveAs(outDir+HistName+".png")
        if("Selection" in HistName or "nEvent" in HistName or "Mvis" in HistName):
            hist.SetMinimum( 1)
            hist.Draw("TEXT")
            CMS_lumi.CMS_lumi(c, iPeriod, iPos)
            c.cd()
            c.Update()
            c.RedrawAxis()
            frame = c.GetFrame()
            frame.Draw()
            ROOT.gPad.SetLogy()
            c.SaveAs(outDir+HistName+"Log.png")
            ROOT.gPad.SetLogy(0)

        c.Clear()
#plotAllSimple()
#plotAllScaled()
plotAllSkimmed()