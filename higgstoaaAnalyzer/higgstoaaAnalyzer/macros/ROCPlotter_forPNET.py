import ROOT
import sys
import subprocess
import string,math,os
import ConfigParser
import glob
import numpy as np
import tdrstyle, CMS_lumi
import mplhep as hep

import matplotlib.pylab as plt
import sklearn.metrics as metrics
label = sys.argv [1]
hep.style.use(hep.style.ROOT)
hep.CMS.label(, data=False, lumi=50, year=2017)

tdrstyle.setTDRStyle()
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
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
inFileSig = ROOT.TFile.Open('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+"_SUSY_2018_NTuple"+".root" ,"READ")
inFileQCD = ROOT.TFile.Open('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+"_QCD_BGen_2018_NTuple"+".root" ,"READ")
inFileTTJets = ROOT.TFile.Open('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+"_TTJets_2018_NTuple"+".root" ,"READ")

outDir = "higgstoaaAnalyzer/graphs/"+label+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)   
checkAndMakeDir(outDir)
#clearDir(outDir)
def integrate(x,y):
    auc = 0
    for i in range(1,len(y)):
        width=x[i]-x[i-1]
        triangle=width*(y[i]-y[i-1])/2
        rectangle=width*y[i-1]
        auc+=(triangle+rectangle)
    return auc  
def makeROC(matchedHist, FakeHist, label):
    matchedHist.Scale(1./matchedHist.Integral(0,matchedHist.GetNbinsX()+2))
    FakeHist.Scale(1./FakeHist.Integral(0,matchedHist.GetNbinsX()+2))
    tpr = []
    fpr = []
    nfp_v = []
    ntp_v = []
    nfn_v = []
    ntn_v = []
    for bin in range(0,matchedHist.GetNbinsX()+1):
        ntp = matchedHist.Integral(bin,matchedHist.GetNbinsX()+2)
        
        nfp = FakeHist.Integral(bin,matchedHist.GetNbinsX()+2)
        ntn = FakeHist.Integral(0,bin)
        nfn =matchedHist.Integral(0,bin)
        #print ("Bin:ntp=" + ntp+", nfn"+nfn + ", ntn"+ntn )
        nfp_v.append(nfp)
        ntp_v.append(ntp)
        ntn_v.append(ntn)
        nfn_v.append(nfn)
        if (ntp==0) and nfp==0:
            tpr.append(0)
            fpr.append(0)
        elif (nfn+ntp)!=0 and nfp+ntn!=0:
            tpr.append(ntp/(nfn+ntp))
            fpr.append(nfp/(nfp+ntn))
        

    print (nfp_v[0])
    print (ntp_v[0])
    print (nfn_v[0])
    print (ntn_v[0])
    print (fpr[0])
    print (tpr[0])
    roc_auc = integrate(fpr,tpr)*-1
    plt.title('H to AA B Jet ROC '+ label)
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.plot(fpr, tpr, 'b')
    plt.legend(loc = 'lower right')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig(outDir+label+"ROC.png")
    plt.close()

    plt.title('Hto AA  B Jet NJets '+ label)
    #plt.plot(nfp, ntp, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.plot(nfp, ntp, 'b')
    plt.legend(loc = 'lower right')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('Merged Signal B Jets')
    plt.xlabel('Background Jets')
    plt.savefig(outDir+label+"NJets.png")
    plt.close()
h={}
h["h_nEvents_sig"]=inFileSig.Get("h_nEvents")
h["h_negOne_eta_sig"]=inFileSig.Get("h_negOne_eta")
h["h_NOTnegOne_eta_sig"]=inFileSig.Get("h_NOTnegOne_eta")
h["h_pNetFull_sig"]=inFileSig.Get("h_pNetFull")


h["h_pNetMerged_DoubleMatch_sig"]=inFileSig.Get("h_pNetMerged_DoubleMatch")
h["h_pNetResolved_sig"]=inFileSig.Get("h_pNetResolved")
h["h_pNetTaus_sig"]=inFileSig.Get("h_pNetTaus")
h["h_pNetUnMatched_sig"]=inFileSig.Get("h_pNetUnMatched")

h["h_DeepFlavMerged_DoubleMatch_sig"]=inFileSig.Get("h_DeepFlavMerged_DoubleMatch")
h["h_DeepFlavResolved_sig"]=inFileSig.Get("h_DeepFlavResolved")
h["h_DeepFlavTaus_sig"]=inFileSig.Get("h_DeepFlavTaus")
h["h_DeepFlavUnMatched_sig"]=inFileSig.Get("h_DeepFlavUnMatched")


h["h_nEvents_qcd"]=inFileQCD.Get("h_nEvents")
h["h_negOne_eta_qcd"]=inFileQCD.Get("h_negOne_eta")
h["h_NOTnegOne_eta_qcd"]=inFileQCD.Get("h_NOTnegOne_eta")
h["h_pNetFull_qcd"]=inFileQCD.Get("h_pNetFull")


h["h_pNetMerged_DoubleMatch_qcd"]=inFileQCD.Get("h_pNetMerged_DoubleMatch")
h["h_pNetResolved_qcd"]=inFileQCD.Get("h_pNetResolved")
h["h_pNetTaus_qcd"]=inFileQCD.Get("h_pNetTaus")
h["h_pNetUnMatched_qcd"]=inFileQCD.Get("h_pNetUnMatched")

h["h_DeepFlavMerged_DoubleMatch_qcd"]=inFileQCD.Get("h_DeepFlavMerged_DoubleMatch")
h["h_DeepFlavResolved_qcd"]=inFileQCD.Get("h_DeepFlavResolved")
h["h_DeepFlavTaus_qcd"]=inFileQCD.Get("h_DeepFlavTaus")
h["h_DeepFlavUnMatched_qcd"]=inFileQCD.Get("h_DeepFlavUnMatched")

h["h_nEvents_ttjets"]=inFileTTJets.Get("h_nEvents")
h["h_negOne_eta_ttjets"]=inFileTTJets.Get("h_negOne_eta")
h["h_NOTnegOne_eta_ttjets"]=inFileTTJets.Get("h_NOTnegOne_eta")
h["h_pNetFull_ttjets"]=inFileTTJets.Get("h_pNetFull")


h["h_pNetMerged_DoubleMatch_ttjets"]=inFileTTJets.Get("h_pNetMerged_DoubleMatch")
h["h_pNetResolved_ttjets"]=inFileTTJets.Get("h_pNetResolved")
h["h_pNetTaus_ttjets"]=inFileTTJets.Get("h_pNetTaus")
h["h_pNetUnMatched_ttjets"]=inFileTTJets.Get("h_pNetUnMatched")

h["h_DeepFlavMerged_DoubleMatch_ttjets"]=inFileTTJets.Get("h_DeepFlavMerged_DoubleMatch")
h["h_DeepFlavResolved_ttjets"]=inFileTTJets.Get("h_DeepFlavResolved")
h["h_DeepFlavTaus_ttjets"]=inFileTTJets.Get("h_DeepFlavTaus")
h["h_DeepFlavUnMatched_ttjets"]=inFileTTJets.Get("h_DeepFlavUnMatched")

types=["Merged_DoubleMatch","Resolved","Taus","UnMatched"]
bkgs=["ttjets","qcd"]
DeepFlavourBackground=ROOT.TH1F("DeepFlavourBackground", "DeepFlavour Background",1000, 0 , 1)
for bin in range(1,DeepFlavourBackground.GetNbinsX()+1):
    binContent=0
    for type in types:
        for bkg in bkgs:
            binContent+=h["h_DeepFlav"+type+"_"+bkg].GetBinContent(bin)
    DeepFlavourBackground.SetBinContent(bin,binContent)

PNetBackground=ROOT.TH1F("PNetBackground", "PNet Background",1000, 0 , 1)
for bin in range(1,PNetBackground.GetNbinsX()+1):
    binContent=0
    for type in types:
        for bkg in bkgs:
            binContent+=h["h_pNet"+type+"_"+bkg].GetBinContent(bin)
    PNetBackground.SetBinContent(bin,binContent)

makeROC(h["h_pNetMerged_DoubleMatch_sig"], PNetBackground, "PNet")
makeROC(h["h_DeepFlavMerged_DoubleMatch_sig"], DeepFlavourBackground, "DeepFlav")


#PNetBackground.Rebin(50)
PNetBackground.SetMinimum( 1)
PNetBackground.Draw("")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
ROOT.gPad.SetLogy()
c.SaveAs(outDir+"PNETBACKGround_Log.png")
ROOT.gPad.SetLogy(0)
c.Clear()
#DeepFlavourBackground.Rebin(50)
DeepFlavourBackground.SetMinimum( 1)
DeepFlavourBackground.Draw("")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
ROOT.gPad.SetLogy()
c.SaveAs(outDir+"DeepFlavourBackground_Log.png")
ROOT.gPad.SetLogy(0)
c.Clear()

#h["h_pNetMerged_DoubleMatch_sig"].Rebin(50)
h["h_pNetMerged_DoubleMatch_sig"].SetMinimum( 1)
h["h_pNetMerged_DoubleMatch_sig"].Draw("")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
ROOT.gPad.SetLogy()
c.SaveAs(outDir+"PNETSig_Log.png")
ROOT.gPad.SetLogy(0)
c.Clear()
#h["h_DeepFlavMerged_DoubleMatch_sig"].Rebin(50)
h["h_DeepFlavMerged_DoubleMatch_sig"].SetMinimum( 1)
h["h_DeepFlavMerged_DoubleMatch_sig"].Draw("")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
ROOT.gPad.SetLogy()
c.SaveAs(outDir+"DeepFlavourSig_Log.png")
ROOT.gPad.SetLogy(0)
c.Clear()