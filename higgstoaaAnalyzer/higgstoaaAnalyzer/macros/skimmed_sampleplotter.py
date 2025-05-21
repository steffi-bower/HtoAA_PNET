import ROOT
import sys
import subprocess
import string,math,os
import ConfigParser
import glob
import numpy as np
import tdrstyle, CMS_lumi
label = sys.argv [1]
if label == "help" or label == "-help" or label == "-h" or label == "h":
    print "Enter the title of the root stored in your local dir. You can enter it either filename or filename.root"
    exit()
if ".root" in label:
    label = label.replace(".root","")

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
inFile = ROOT.TFile.Open(label+".root" ,"READ")
outDir = "//uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/graphs/"+label+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)      
checkAndMakeDir(outDir)
plotting_variables=["Mvis","bMass",'EventSelection','l1Iso','l2Iso','l1Pt','l2Pt','l1dB','l2dB','l1dB_sig','l2dB_sig']

totalevents= inFile.Get("h_nEvents").GetBinContent(2)
channels = ["tauE_tauE","tauE_tauMu","tauMu_tauMu","tauHad_tauMu","tauHad_tauE"]
variables= [["Mvis","Mvis",[15,2,17]],["bMass","bMass",[20,0,20]],["bDRl","bDrl",[45,0,5]],["lepDR","lepDR",[20,0,1.2]],["DiTauPt","DiTauPt",[50,0,200]],["l1Iso","REPLACEME1 Iso",[20,0,1]],["l2Iso","REPLACEME2 Iso",[20,0,1]],["l1Pt","REPLACEME1 Pt",[10,0,50]],["l2Pt","REPLACEME2 Pt",[10,0,50]],["l1dB","REPLACEME1 dB",[10,0,.5]],["l2dB","REPLACEME2 dB",[10,0,.5]],["l1dB_sig","REPLACEME1 dB Significance",[10,0,20]],["l2dB_sig", "REPLACEME2 dB Significance",[10,0,20]]]
#variables= [["Mvis","Mvis",[15,2,17]],["bMass","bMass",[20,0,20]],["bDRl","bDrl",[45,0,5]],["lepDR","lepDR",[20,0,1.2]],["DiTauPt","DiTauPt",[50,0,200]],["l1Iso","REPLACEME1 Iso",[20,0,1]],["l2Iso","REPLACEME2 Iso",[20,0,1]],["l1Pt","REPLACEME1 Pt",[10,0,50]],["l2Pt","REPLACEME2 Pt",[10,0,50]],["l1dB","REPLACEME1 dB",[10,0,.5]],["l2dB","REPLACEME2 dB",[10,0,.5]],["l1dB_sig","REPLACEME1 dB Significance",[10,0,20]],["l2dB_sig", "REPLACEME2 dB Significance",[10,0,20]],["MET","MET",[25,0,250]],["l1dB_sig_bMatched","REPLACEME1 dB Significance bMatched",[10,0,20]],["l2dB_sig_bMatched", "REPLACEME2 dB Significance bMatched",[10,0,20]]]

#muonTrigs= [("isIsoMu",ROOT.kMagenta),("isDoubleMuSS",ROOT.kRed), ("isDoubleMuMass8",ROOT.kBlue),("isDoubleMuMass3p8",ROOT.kGreen),("isDoubleMu",ROOT.kCyan)]
muonTrigs= [("isIsoMu",ROOT.kMagenta)]
electronTrigs =  [("isIsoEle",ROOT.kRed),("isMuonEG",ROOT.kBlue),("isDoubleEG",ROOT.kGreen)]

def getHistMax(hist):
    return hist[0].GetMaximum()
def StandardPlots():
    for channel in channels:
        for variable in variables:
            outFolder=outDir+"/"+variable[0]
            checkAndMakeDir(outFolder)
            variableHists=[]
            leps = channel.split("_")
            CMS_lumi.CMS_lumi(c, iPeriod, iPos)
            l = ROOT.TLegend(0.65,0.7,0.85,0.87)
            variableHists.append((inFile.Get("h_"+channel+"_"+variable[0]+"_isBPH"),("isBPH",ROOT.kBlack)))
            #if "tauE" in channel:
            #    for trigger in electronTrigs:
            #        variableHists.append((inFile.Get("h_"+channel+"_"+variable[0]+"_"+trigger[0]),trigger))
            #elif "Mu" in channel:
            #    for trigger in muonTrigs:
            #        variableHists.append((inFile.Get("h_"+channel+"_"+variable[0]+"_"+trigger[0]),trigger))
            variableHists.sort(key=getHistMax)
            isfirst = True
            for hist in variableHists:
                if variable[0] == "EventSelection":
                    hist[0].SetMinimum(0.1)
                else:
                    hist[0].SetMinimum(0)
                hist[0].Scale(2.263/totalevents)
                hist[0].SetLineColor(hist[1][1])
                l.AddEntry(hist[0],hist[1][0],"l")
                
                if isfirst:
                    if variable[0] == "EventSelection":
                        ROOT.gPad.SetLogy()
                    else:
                        ROOT.gPad.SetLogy(0)
                    title = hist[0].GetTitle()
                    hist[0].GetXaxis().SetTitle(title)
                    hist[0].LabelsDeflate()
                    #hist[0].Draw()


                    hist[0].Draw("TEXT")
                    isfirst=False

                else:
                    hist[0].Draw("SAME")
            #l.Draw()
            c.cd()
            c.Update()
            c.RedrawAxis()
            frame = c.GetFrame()
            frame.Draw()
            c.SaveAs(outFolder+"/"+channel+"_"+variable[0]+".png")
            c.Clear()
        if "tauE" in channel:
                triggers = electronTrigs
        elif "Mu" in channel:
                triggers = muonTrigs
        ROOT.gPad.SetLogy()
        leps = channel.split("_")
        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        l = ROOT.TLegend(0.65,0.7,0.85,0.87)
        outFolder=outDir+"/EventSelection/"
        checkAndMakeDir(outFolder)
        eventSelectionHists=[]
        eventSelectionHists.append((inFile.Get("h_"+channel+"_isBPH_EventSelection"),("isBPH",ROOT.kBlack)))
        for trigger in triggers:
            eventSelectionHists.append((inFile.Get("h_"+channel+"_"+trigger[0]+"_EventSelection"),trigger))

        eventSelectionHists.sort(key=getHistMax)
        isfirst = True
        for hist in eventSelectionHists:
            hist[0].SetMinimum(0.1)
            print (" there are "+ str(hist[0].Integral()) +"entries for "+ hist[1][0])
            hist[0].Scale(2.263/totalevents)
            hist[0].SetLineColor(hist[1][1])
            l.AddEntry(hist[0],hist[1][0],"l")
            
            if isfirst:

                title = hist[0].GetTitle()
                hist[0].GetXaxis().SetTitle(title)
                hist[0].LabelsDeflate()

                hist[0].Draw()
                isfirst=False
            else:

                hist[0].Draw("SAME")
        l.Draw()
        c.cd()
        c.Update()
        c.RedrawAxis()
        frame = c.GetFrame()
        frame.Draw()
        c.SaveAs(outFolder+"/"+channel+"_EventSelection.png")
        c.Clear()

def OverlapPlots():
    for channel in channels:
        for variable in variables:
            ROOT.gPad.SetLogy(0)

            if "tauE" in channel:
                    triggers = electronTrigs
            elif "Mu" in channel:
                    triggers = muonTrigs
            outFolder=outDir+"/"+variable[0]
            checkAndMakeDir(outFolder)
            leps = channel.split("_")
            CMS_lumi.CMS_lumi(c, iPeriod, iPos)
            #variableHists.append((inFile.Get("h_"+channel+"_"+variable[0]+"_isBPH"),("isBPH",ROOT.kBlack)))

            for trigger in triggers:
                print ("h_"+channel+"_"+variable[0]+"_"+trigger[0]+"_AND_isBPH")

                l = ROOT.TLegend(0.65,0.7,0.85,0.87)

                hist_AND=inFile.Get("h_"+channel+"_"+variable[0]+"_"+trigger[0]+"_AND_isBPH")
                hist_AND.SetFillColor(ROOT.kOrange)
                hist_BPH=inFile.Get("h_"+channel+"_"+variable[0]+"_NOT"+trigger[0]+"_isBPH")

                hist_BPH.SetFillColor(ROOT.kYellow)
                hist_trigger=inFile.Get("h_"+channel+"_"+variable[0]+"_"+trigger[0]+"_NOTisBPH")
                hist_trigger.SetFillColor(ROOT.kRed)
                title = hist_AND.GetTitle()

                Stack = ROOT.THStack("h_"+channel+"_"+variable[0]+"_"+trigger[0],"")
                totalentries=hist_AND.GetEntries()+hist_BPH.GetEntries()+hist_trigger.GetEntries()
                hist_AND.Scale(1/totalentries)
                hist_BPH.Scale(1/totalentries)
                hist_trigger.Scale(1/totalentries)
                Stack.Add(hist_AND)
                Stack.Add(hist_BPH)
                Stack.Add(hist_trigger)
                #Stack.GetXaxis().SetTitle(title)
                #Stack.LabelsDeflate()
                l.AddEntry(hist_AND,"Both","f")
                l.AddEntry(hist_BPH,"isBPH !"+trigger[0],"f")
                l.AddEntry(hist_trigger,trigger[0]+" !isBPH","f")
                Stack.Draw("hist")

                l.Draw()
                c.cd()
                c.Update()
                c.RedrawAxis()
                frame = c.GetFrame()
                frame.Draw()
                c.SaveAs(outFolder+"/"+channel+"_"+variable[0]+"_"+trigger[0]+".png")
                c.Clear()


            ROOT.gPad.SetLogy()
            leps = channel.split("_")
            CMS_lumi.CMS_lumi(c, iPeriod, iPos)
            outFolder=outDir+"/EventSelection/"
            checkAndMakeDir(outFolder)
            for trigger in triggers:
                CMS_lumi.CMS_lumi(c, iPeriod, iPos)

                hist=inFile.Get("h_"+channel+"_"+trigger[0]+"_EventSelection")

                hist.SetMinimum(0.1)
                
                title = hist.GetTitle()
                hist.GetXaxis().SetTitle(title)
                hist.LabelsDeflate()

                hist.Draw("TEXT")

                c.cd()
                c.Update()
                c.RedrawAxis()
                frame = c.GetFrame()
                frame.Draw()
                c.SaveAs(outFolder+"/"+channel+"_"+trigger[0]+"_EventSelection.png")
                c.Clear()


OverlapPlots()
#StandardPlots()
                
generalPlots=["h_std_electron_selection","h_muon_selection","h_eCtau_selection","h_muCtau_selection","h_bJet_selection", "h_nEvents","h_bMatchedMu_PT","h_bMatchedE_PT","h_bMatchedMu_dBSig","h_bMatchedE_dBSig","h_nBGenE","h_nBGenMu","h_nStepstoNull","h_Btagger","h_trigger_debug","h_nullMom","h_BtriggerMu_bMatched_pt_dB","h_BtriggerMu_tauMatched_pt_dB","h_nBtriggerMu"]
ROOT.gPad.SetLogy(0)
checkAndMakeDir(outDir+"/GeneralHist/")
for plot in generalPlots:
    hist = inFile.Get(plot)
    title = hist.GetTitle()
    #hist.GetXaxis().SetTitle(title)
    hist.LabelsDeflate()
    HistType=hist.ClassName()

    if(HistType=="TH2F"):
        hist.Draw("COLZ")
    else:
        hist.Draw("TEXT")
    CMS_lumi.CMS_lumi(c, iPeriod, iPos)

    c.cd()
    c.Update()
    c.RedrawAxis()
    frame = c.GetFrame()
    frame.Draw()
    c.SaveAs(outDir+"/GeneralHist/"+plot+".png") 
    c.Clear()