import ROOT
import sys
import subprocess
import string,math,os
import ConfigParser
import glob
import numpy as np
import tdrstyle, CMS_lumi

import matplotlib.pylab as plt
import sklearn.metrics as metrics
label = sys.argv [1]


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
inFileBKG = ROOT.TFile.Open('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+"_Background.root" ,"READ")

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
    matchedHist.Scale(1./matchedHist.Integral(1,matchedHist.GetNbinsX()+2))
    FakeHist.Scale(1./FakeHist.Integral(0,matchedHist.GetNbinsX()+2))
    tpr = []
    fpr = []
    nfp_v = []
    ntp_v = []
    wp_80=0.
    wp_85=0.
    wp_90=0.
    wp_95=0.
    for bin in range(1,matchedHist.GetNbinsX()+1):
        ntp = matchedHist.Integral(bin,matchedHist.GetNbinsX()+2)
        
        nfp = FakeHist.Integral(bin,matchedHist.GetNbinsX()+2)
        ntn = FakeHist.Integral(0,bin)
        nfn =matchedHist.Integral(0,bin)
        #print ("Bin:ntp=" + ntp+", nfn"+nfn + ", ntn"+ntn )
        nfp_v.append(nfp)
        ntp_v.append(ntp)
        if (ntp==0) and nfp==0:
            tpr.append(0)
            fpr.append(0)
        elif (nfp+ntn)!=0 and nfn+ntp!=0:
            tpr.append(ntp/(nfn+ntp))
            fpr.append(nfp/(nfp+ntn))
        if tpr[bin-1]>.80:
            wp_80=bin*.001
        if tpr[bin-1]>.85:
            wp_85=bin*.001
        if tpr[bin-1]>.90:
            wp_90=bin*.001
        if tpr[bin-1]>.95:
            wp_95=bin*.001
    
    roc_auc = integrate(fpr,tpr)
    plt.title('H to AA B Jet ROC '+ label)
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.plot(fpr, tpr, 'b')
    plt.legend(loc = 'lower right')
    plt.xlim([0, 1])
    print ("Working points for " +label+":\n 80="+str(wp_80)+";\n 85="+str(wp_85)+";\n 90="+str(wp_90)+";\n 95="+str(wp_95))
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig(outDir+label+"ROC.png")
    plt.xlim([.01, 1])

    plt.ylim([.75, 1])
    #plt.yscale("log")
    plt.xscale("log")
    print 

    plt.savefig(outDir+label+"ROCLogx.png")

    plt.close()


channels = ["tauE_tauE","tauE_tauMu","tauMu_tauMu","tauHad_tauMu","tauHad_tauE"]
variables= [
    ["b1_ID_Total","b1 Total ID Value REPLACEME1 REPLACEME2",[20,0,1]],
    ["b1_PNetID","b1 PNet ID Value REPLACEME1 REPLACEME2",[20,0,1]],

    ]
Channel_HistDict={}
SignalHists={}
BackgroundHists = {}
#for channel in channels:
#    leps = channel.split("_")
#
#    for variable in variables:
#            
#            title = variable[1].replace("REPLACEME1",leps[0])
#            title=title.replace("REPLACEME2",leps[1])
#            SignalHists["h_"+channel+"_"+variable[0]+"_isBPH_genMatchB"]=inFileSig.Get("h_"+channel+"_"+variable[0]+"_isBPH")
#            BackgroundHists["h_"+channel+"_"+variable[0]+"_isBPH"]=inFileBKG.Get("h_"+channel+"_"+variable[0]+"_isBPH")
#            makeROC(SignalHists["h_"+channel+"_"+variable[0]+"_isBPH_genMatchB"],BackgroundHists["h_"+channel+"_"+variable[0]+"_isBPH"], channel+"_"+variable[0]+"_ROC")

def makeTrigEff(preTrig, postTrig, label, max):
    TriggEffHist=ROOT.TH1F("TriggerEff", label,postTrig.GetNbinsX(), 0 , max)

    for bin in range(1,postTrig.GetNbinsX()+1):
        denominator = preTrig.Integral(bin,preTrig.GetNbinsX()+2)
        numerator=postTrig.Integral(bin,preTrig.GetNbinsX()+2)
        if denominator==0:
            TriggEffHist.SetBinContent(bin,0)

        else:  
            TriggEffHist.SetBinContent(bin,numerator/denominator)
    return TriggEffHist

PTTrigEff_sig=makeTrigEff(inFileSig.Get("h_Mu_pT"),inFileSig.Get("h_triggerMu_pT"), "Trigger Efficiency Pt",51)
dBSigTrigEff_sig=makeTrigEff(inFileSig.Get("h_Mu_dBSig"),inFileSig.Get("h_triggerMu_dBSig"), "Trigger Efficiency dBSig",20)
makeROC(inFileSig.Get("h_DeepFlavMerged"),inFileBKG.Get("h_DeepFlav"), "DeepFlavour")
makeROC(inFileSig.Get("h_pNetMerged"),inFileBKG.Get("h_pNetFull"), "PNet")

PTTrigEff_sig.Draw("")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"PTTrigEff_dBsig.png")
c.Clear()

dBSigTrigEff_sig.Draw("")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"dBSigTrigEff_sig.png")

PTTrigEff_bkg=makeTrigEff(inFileBKG.Get("h_Mu_pT"),inFileBKG.Get("h_triggerMu_pT"), "Trigger Efficiency Pt",51)
dBSigTrigEff_bkg=makeTrigEff(inFileBKG.Get("h_Mu_dBSig"),inFileBKG.Get("h_triggerMu_dBSig"), "Trigger Efficiency dBSig",20)

PTTrigEff_bkg.Draw("")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"PTTrigEff_bkg.png")
c.Clear()

dBSigTrigEff_bkg.Draw("")

CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"dBSigTrigEff_bkg.png")
c.Clear()

pnetvdeepflav=inFileSig.Get("h_pNetvDeepFlav_Merged")
pnetvdeepflav.GetYaxis().SetTitle("DeepFlavour")
pnetvdeepflav.GetXaxis().SetTitle("PNet")
pnetvdeepflav.Draw("COLZ")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"2dHistSig.png")
c.Clear()

pnetvdeepflav=inFileBKG.Get("h_pNetvDeepFlav_Full")
pnetvdeepflav.GetYaxis().SetTitle("DeepFlavour")
pnetvdeepflav.GetXaxis().SetTitle("PNet")
pnetvdeepflav.Draw("COLZ")

CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()
c.SaveAs(outDir+"2dHistBkg.png")
c.Clear()