import ROOT
import sys
import subprocess
import string,math,os
import glob
import numpy as np
import mplhep as hep
import matplotlib.colors as mcolors

import matplotlib.pylab as plt
import sklearn.metrics as metrics
import tdrstyle, CMS_lumi

label = sys.argv [1]
ROOT.gROOT.SetBatch(True)

hep.style.use(hep.style.ROOT)
hep.cms.label('', data=False, year=2018)
tdrstyle.setTDRStyle()

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
inFileSig = ROOT.TFile.Open('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+"_SUSY_2018_NTuple"+".root" ,"READ")
#inFileQCD = ROOT.TFile.Open('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+"_QCD_BGen_2018_NTuple"+".root" ,"READ")
inFileQCD = ROOT.TFile.Open('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+"_QCD_PtBin_2018_NTuple"+".root" ,"READ")
inFileTTJets = ROOT.TFile.Open('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+"_TTJets_2018_NTuple"+".root" ,"READ")

outDir = "higgstoaaAnalyzer/graphs/"+label+"_ROCs/"
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

h={}
bkgs=[["ttjets",inFileTTJets],["qcd",inFileQCD]]
tags=["_bb_"]
ptbins=["10to40","40to100","100plus"]
#ptbins = [""]
#tags = [""]
#sigs=[["ttjets",inFileTTJets],["qcd",inFileQCD]]
sigs=[["sig",inFileSig]]




def makeROC_vecs(matchedHist, FakeHist):
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



    roc_auc = integrate(fpr,tpr)*-1
    return (tpr,fpr,roc_auc)
for pt in ptbins:
    pnetbkghists = []
    pnetsighists = []
    for bkg in bkgs:
        pnetbkghists.append(bkg[1].Get("h_pNetFake_"+pt))
        pnetbkghists[-1].GetXaxis().SetTitle(pnetbkghists[-1].GetTitle()+" " +bkg[0])
        pnetbkghists[-1].Draw("hist e")
        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        c.SaveAs(outDir+"h_pNetFake_"+pt+"_"+bkg[0]+".png")
        c.Clear()
        pnetbkghists.append(bkg[1].Get("h_pNetMerged_"+pt))
        pnetbkghists[-1].GetXaxis().SetTitle(pnetbkghists[-1].GetTitle()+" " +bkg[0])
        pnetbkghists[-1].Draw("hist e")
        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        c.SaveAs(outDir+"h_pNetMerged_"+pt+"_"+bkg[0]+".png")
        c.Clear()
    for sig in sigs:

        pnetsighists.append(sig[1].Get("h_pNetMerged_"+pt))
        pnetsighists[-1].GetXaxis().SetTitle(pnetbkghists[-1].GetTitle()+" " +sig[0])
        pnetsighists[-1].Draw("hist e")
        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        c.SaveAs(outDir+"h_pNetMerged_"+pt+"_"+sig[0]+".png")
        c.Clear()
    PNetBackground=ROOT.TH1F("PNetBackground", "PNetBackground ",50000, 0 , 1)
    pnetSIG=ROOT.TH1F("pnetSIG", "pnetSIG ",50000, 0 , 1)
    for bin in range(1,PNetBackground.GetNbinsX()+1):
        binContentBKG=0
        binContentSig=0

        for bkg in pnetbkghists:
            binContentBKG+=bkg.GetBinContent(bin)
        for sig in pnetsighists:
            binContentSig+=sig.GetBinContent(bin)
        PNetBackground.SetBinContent(bin,binContentBKG)
        pnetSIG.SetBinContent(bin,binContentSig)
    pnetSIG.Draw()
    CMS_lumi.CMS_lumi(c, iPeriod, iPos)
    c.SaveAs(outDir+"pnetsig"+pt+".png")
    c.Clear()
    PNetBackground.Draw()
    CMS_lumi.CMS_lumi(c, iPeriod, iPos)
    c.SaveAs(outDir+"pnetBackground"+pt+".png")
    c.Clear()
    PNET_tpr,PNET_fpr, PNET_auc=makeROC_vecs(pnetSIG, PNetBackground)

    for tag in tags:
        deepbkghists=[]
        deepsighists=[]
        for bkg in bkgs:
            deepbkghists.append(bkg[1].Get("h_DeepFlav"+tag+"Fake_"+pt))
            deepbkghists[-1].GetXaxis().SetTitle(deepbkghists[-1].GetTitle()+" " +bkg[0])
            deepbkghists[-1].Draw("hist e")
            CMS_lumi.CMS_lumi(c, iPeriod, iPos)
            c.SaveAs(outDir+"h_DeepFlav"+tag+"Fake_"+pt+"_"+bkg[0]+".png")
            c.Clear()

            deepbkghists.append(bkg[1].Get("h_DeepFlav"+tag+"Merged_"+pt))
            deepbkghists[-1].GetXaxis().SetTitle(deepbkghists[-1].GetTitle()+" " +bkg[0])
            deepbkghists[-1].Draw("hist e")
            CMS_lumi.CMS_lumi(c, iPeriod, iPos)
            c.SaveAs(outDir+"h_DeepFlav"+tag+"Merged_"+pt+"_"+bkg[0]+".png")
            c.Clear()

        for sig in sigs:

            deepsighists.append(sig[1].Get("h_DeepFlav"+tag+"Merged_"+pt))
            deepsighists[-1].GetXaxis().SetTitle(deepsighists[-1].GetTitle()+" " +sig[0])
            deepsighists[-1].Draw("hist e")
            CMS_lumi.CMS_lumi(c, iPeriod, iPos)
            c.SaveAs(outDir+"h_DeepFlav"+tag+"Merged_"+pt+"_"+sig[0]+".png")
            c.Clear()

        print("h_DeepFlav"+tag+"Merged_"+pt)
        DeepFlavourBackground=ROOT.TH1F("DeepFlavourBackground"+tag, "DeepFlavour Background"+tag,50000, 0 , 1)
        deepsighist=ROOT.TH1F("deepsighist"+tag, "DeepFlavour Background",50000, 0 , 1)

        for bin in range(1,DeepFlavourBackground.GetNbinsX()+1):
            binContentBKG=0
            binContentSig=0
            for bkg in deepbkghists:
                
                binContentBKG+=bkg.GetBinContent(bin)
            for sig in deepsighists:
                binContentSig+=sig.GetBinContent(bin)
            
            DeepFlavourBackground.SetBinContent(bin,binContentBKG)
            deepsighist.SetBinContent(bin,binContentSig)
        deepsighist.Draw()
        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        c.SaveAs(outDir+"deepsighist"+tag+pt+".png")
        c.Clear()
        DeepFlavourBackground.Draw()
        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        c.SaveAs(outDir+"DeepFlavourBackground"+tag+pt+".png")
        c.Clear()
        DFLAV_tpr,DFLAV_fpr, DFLAV_auc=makeROC_vecs(deepsighist, DeepFlavourBackground)
        wp80DFLAV= DFLAV_tpr.index(min(DFLAV_tpr, key=lambda x:abs(x-.80)))
        wp85DFLAV= DFLAV_tpr.index(min(DFLAV_tpr, key=lambda x:abs(x-.85)))
        wp90DFLAV= DFLAV_tpr.index(min(DFLAV_tpr, key=lambda x:abs(x-.90)))

        wp80PNET= PNET_tpr.index(min(PNET_tpr, key=lambda x:abs(x-.80)))
        wp85PNET= PNET_tpr.index(min(PNET_tpr, key=lambda x:abs(x-.85)))
        wp90PNET= PNET_tpr.index(min(PNET_tpr, key=lambda x:abs(x-.90)))
        print("PNET WP: 80%=" + str(wp80PNET)+", 85%="+ str(wp85PNET)+", 90%="+ str(wp90PNET))
        print("DeepFLAV"+tag.strip("_")+ " WP: 80%=" + str(wp80DFLAV)+", 85%="+ str(wp85DFLAV)+", 90%="+ str(wp90DFLAV))
        hep.style.use(hep.style.ROOT)
        hep.cms.label('', data=False, year=2018)
        plt.plot(DFLAV_tpr, DFLAV_fpr, 'tab:cyan', label = 'DeepJet bb  (AUC = %0.3f)' % DFLAV_auc)
        plt.plot(PNET_tpr, PNET_fpr, 'xkcd:crimson', label = 'ParticleNet (AUC = %0.3f)' % PNET_auc)
        plt.legend(loc = 'lower right')

        plt.grid(axis='x', color='0.95')

        plt.grid(axis='y', color='0.95')
        plt.xlim([0, 1])
        plt.ylim([.0001, 1])
        plt.yscale('log')
        plt.ylabel('Mistagging Rate (Background Jets)')
        plt.xlabel('Tagging Efficiency (Merged b-jets) ('+pt+')')
        plt.savefig(outDir+label+"_"+tag+"_"+pt+"_ROC.png")
        plt.close()
        scores=np.linspace(0, 1, 50001)
        plt.plot(DFLAV_tpr,scores, 'tab:cyan', label = 'DeepJet bb TPR')
        plt.plot(DFLAV_fpr,scores, 'xkcd:crimson', label = 'DeepJet bb FPR')
        plt.legend(loc = 'lower right')

        plt.grid(axis='x', color='0.95')

        plt.grid(axis='y', color='0.95')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        #plt.yscale('log')
        plt.ylabel('Rate ')
        plt.xlabel('Deep Flavor Score ' +pt) 
        plt.savefig(outDir+"DEEPFLAVTPRFPR"+tag+"_"+pt+"_ROC.png")
        plt.close()

        plt.plot(PNET_tpr,scores, 'tab:cyan', label = 'Pnet TPR')
        plt.plot(PNET_fpr,scores, 'xkcd:crimson', label = 'PNet FPR')
        plt.legend(loc = 'lower right')

        plt.grid(axis='x', color='0.95')

        plt.grid(axis='y', color='0.95')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        #plt.yscale('log')
        plt.ylabel('Rate ')
        plt.xlabel('PNET Score ' +pt) 
        plt.savefig(outDir+"PNETTPRFPR"+"_"+pt+"_ROC.png")
        plt.close()

            
            
            
            
