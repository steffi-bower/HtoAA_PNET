import ROOT
import sys
import subprocess
import string,math,os
import ConfigParser
import glob
import numpy as np
import tdrstyle, CMS_lumi
import array
import matplotlib.pylab as plt
import time
label = sys.argv [1]


#tdrstyle.setTDRStyle()
ROOT.gROOT.SetBatch(True)

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod = 8

iPos = 11
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
#CMS_lumi.CMS_lumi(c, iPeriod, iPos)
inFile = ROOT.TFile.Open(label+".root" ,"READ")
outDir = "//uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/graphs/"+label+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)      
checkAndMakeDir(outDir)
def makeROC(matchedHist, FakeHist, conditions):
    tpr = []
    fpr = []
    nfp_v = []
    ntp_v = []
    roc_auc=[]
    for bin in range(1,21):
        ntp = matchedHist.Integral(bin,21)
        
        nfp = FakeHist.Integral(bin,21)
        ntn = FakeHist.Integral(1,bin+1)
        nfn =matchedHist.Integral(1,bin+1)
        #print ("Bin:ntp=" + ntp+", nfn"+nfn + ", ntn"+ntn )
        nfp_v.append(nfp)
        ntp_v.append(ntp)
        if (nfp+ntp)!=0:
            tpr.append(ntp/(nfp+ntp))
        else:
            tpr.append(0)
        if nfn+ntn!=0:
            fpr.append(nfn/(nfn+ntn))
        else: fpr.append(0)

    plt.title('Hto AA Deep B Jet ROC (' + conditions+')')
    #plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.plot(fpr, tpr, 'b')
    plt.legend(loc = 'lower right')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig(outDir+"ROC_"+conditions+".png")
    plt.close()

    plt.title('Hto AA Deep B Jet NJets (' + conditions+')')
    #plt.plot(nfp, ntp, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.plot(nfp, ntp, 'b')
    plt.legend(loc = 'lower right')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('Matched bJets')
    plt.xlabel('Fake bJets')
    plt.savefig(outDir+"NJets_"+conditions+".png")
    plt.close()

h_DeepBvsJetPt= inFile.Get("h_DeepBvsJetPt")
#h_DeepBvsJetPt_text= inFile.Get("h_DeepBvsJetPt")
h_DeepBvsJetPt.SetTitle("H to AA Jets;Deep B Score;JetPt;")
#h_DeepBvsJetPt_text.SetMarkerSize(1.8)
h_DeepBvsJetPt.Draw("COLZ")
#h_DeepBvsJetPt_text.Draw("TEXT SAME")
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"h_DeepBvsJetPt.png")
c.Clear()

h_bDrVsTauDr= inFile.Get("h_bDrVsTauDr")
#h_bDrVsTauDr_text= inFile.Get("h_bDrVsTauDr")
h_bDrVsTauDr.SetTitle("H to AA Jets Gen dR;min dR(jet, gen b);min dR(jet, gen Tau);")
#h_bDrVsTauDr_text.SetMarkerSize(1.8)
h_bDrVsTauDr.Draw("COLZ")
#h_bDrVsTauDr_text.Draw("TEXT SAME")
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"h_bDrVsTauDr.png")
c.Clear()

h_bDrVsTauDr_deepbloose= inFile.Get("h_bDrVsTauDr_deepbloose")
#h_bDrVsTauDr_deepbloose_text= inFile.Get("h_bDrVsTauDr_deepbloose")
h_bDrVsTauDr_deepbloose.SetTitle("H to AA Jets Deep B>.0493;min dR(jet, gen b);min dR(jet, gen Tau);")
#h_bDrVsTauDr_deepbloose_text.SetMarkerSize(1.8)
h_bDrVsTauDr_deepbloose.Draw("COLZ")
#h_bDrVsTauDr_deepbloose_text.Draw("TEXT SAME")
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"h_bDrVsTauDr_deepbloose.png")
c.Clear()

h_bDrVsTauDr_deepbloose_BPH= inFile.Get("h_bDrVsTauDr_deepbloose_BPH")
#h_bDrVsTauDr_deepbloose_BPH_text= inFile.Get("h_bDrVsTauDr_deepbloose_BPH")
h_bDrVsTauDr_deepbloose_BPH.SetTitle("H to AA Jets Deep B>.0493 BPH==True;min dR(jet, gen b);min dR(jet, gen Tau);")
#h_bDrVsTauDr_deepbloose_BPH_text.SetMarkerSize(1.8)
h_bDrVsTauDr_deepbloose_BPH.Draw("COLZ")
#h_bDrVsTauDr_deepbloose_BPH_text.Draw("TEXT SAME")
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"h_bDrVsTauDr_deepbloose_BPH.png")
c.Clear()

h_DeepBMatched=inFile.Get("h_DeepBMatched")
h_DeepBMatched.Draw()
#h_bDrVsTauDr_deepbloose_BPH_text.Draw("TEXT SAME")
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"TrueID.png")
c.Clear()

h_DeepBFake=inFile.Get("h_DeepBFake")
h_DeepBFake.Draw()
#h_bDrVsTauDr_deepbloose_BPH_text.Draw("TEXT SAME")
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"FakeID.png")
c.Clear()

makeROC(h_DeepBMatched, h_DeepBFake, "NoTrigger")
h_DeepBMatched_BPH=inFile.Get("h_DeepBMatched_BPH")
h_DeepBFake_BPH=inFile.Get("h_DeepBFake_BPH")
makeROC(h_DeepBMatched_BPH, h_DeepBFake_BPH, "BPH_Events")



