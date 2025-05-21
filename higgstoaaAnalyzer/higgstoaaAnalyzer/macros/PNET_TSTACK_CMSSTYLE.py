import ROOT
import sys
import subprocess
import string,math,os
import glob
import numpy as np
import tdrstyle, CMS_lumi

ROOT.gROOT.SetBatch(True)

label = sys.argv [1]
tag = sys.argv [2]
#Datalabel=sys.argv [2]
#hists = ["h_tauE_tauE_Mvis_EG" ,"h_tauE_tauE_Mvis_EGorDoubleEG","h_tauE_tauE_Mvis_noTrig","h_tauMu_tauE_Mvis_SingleMu", "h_tauMu_tauE_Mvis_EGorSingleMu" ,"h_tauMu_tauE_Mvis_MuEGorSingleMu" ,"h_tauMu_tauE_Mvis_noTrig", "h_tauMu_tauMu_Mvis_SingleMu", "h_tauMu_tauMu_Mvis_SingleMuorDoubleMu","h_tauMu_tauMu_Mvis_noTrig"]
#hists = ["h_MET"]
channels = ["tauE_tauMu","tauHad_tauMu","tauHad_tauE"]
titles = {
    "tauE_tauMu":"e#mu ",
    "tauHad_tauE":"e#tau ",
    "tauHad_tauMu":"#mu#tau "
}
variables= [
    ["Mvis","Mvis",[6,0,3]],
    ["eleIso","eleIso",[5,0,5]],
    ["muIso","muIso",[20,0,5]],

    ["b1_ID_Total","b1 Total ID Value",[50,0,1]],
    ["b1_PNetID","b1 PNet ID Value",[50,0,1]],
    ["bMass","bMass",[20,0,20]],
    ["lep1Pt","lep1 Pt (GeV)",[25,0,75]],
    ["lep2Pt","lep2 Pt (GeV)",[25,0,75]],
    ["lepDr","DeltaR (leptons)",[20,0,1.5]],
    ["lep1DRB","DeltaR (bL1)",[20,0,4]],
    ["lep2DRB","DeltaR (bL2)",[20,0,4]],
    ["MET","MET (GeV)",[10,0,100]],
    ["NLep1s","NLep1s",[5,0,5]],
    ["NLep2s","NLep2s",[5,0,5]],
    ["NLep2s","NLep2s",[5,0,5]],
    #["b1_ID_Total","b1 Total ID Value",[1000,0,1]],
    #["b1_PNetID","b1 PNet ID Value",[1000,0,1]],
    
    #["bMass","bMass",[20,0,20]],
    ]
muonTrigs= [("isBPH",ROOT.kMagenta),("isIsoMu",ROOT.kMagenta),("isDoubleMuSS",ROOT.kRed), ("isDoubleMuMass8",ROOT.kBlue),("isDoubleMuMass3p8",ROOT.kGreen),("isDoubleMu",ROOT.kCyan)]
electronTrigs =  [("isBPH",ROOT.kMagenta),("isIsoEle",ROOT.kRed),("isMuonEG",ROOT.kBlue),("isDoubleEG",ROOT.kGreen)]

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 }"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_sqrtS = "33.6fb^{-1}" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod = 9

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.15
plotfolder = "/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/"
outDir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/graphs/"+label+"_"+tag+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)      
checkAndMakeDir(outDir)
#QCDFile =ROOT.TFile.Open(plotfolder+label+"_QCD_BGen_2018_NTuple.root" ,"READ")

TTBarFile = ROOT.TFile.Open(plotfolder+label+"_TTJets_2018_NTuple.root" ,"READ")
WJetstoLNuFile = ROOT.TFile.Open(plotfolder+label+"_WJetstoLNu_2018_Skimmed.root" ,"READ")
WWFile = ROOT.TFile.Open(plotfolder+label+"_WW_2018_Skimmed.root" ,"READ")
WZFile = ROOT.TFile.Open(plotfolder+label+"_WZ_2018_Skimmed.root" ,"READ")
DYJetsFile = ROOT.TFile.Open(plotfolder+label+"_DYJetsToLL_M-50_2018_Skimmed.root" ,"READ")
ZZFile = ROOT.TFile.Open(plotfolder+label+"_ZZ_2018_Skimmed.root" ,"READ")
#BackgroundFile = ROOT.TFile.Open(plotfolder+label+"_Combined.root" ,"READ")

SUSYFile = ROOT.TFile.Open(plotfolder+label+"_SUSY_2018_NTuple.root" ,"READ")
Backgrounds = [

{"file":TTBarFile,"name":"TTBar","color":ROOT.kCyan},
#{"file":QCDFile,"name":"QCD BGen","color":ROOT.kGray},
{"file":WWFile,"name":"WW","color":ROOT.kRed},
{"file":WZFile,"name":"WZ","color":ROOT.kBlue},
{"file":DYJetsFile,"name":"DYJets","color":ROOT.kOrange},
{"file":ZZFile,"name":"ZZ","color":ROOT.kMagenta},
{"file":WJetstoLNuFile,"name":"WJets","color":ROOT.kGreen},

]
#DataFile = ROOT.TFile.Open(plotfolder+Datalabel+".root" ,"READ")

H_ref = 800; 
W_ref = 850; 
W = W_ref
H  = H_ref
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.08*W_ref
#c1 = ROOT.TCanvas("Delta RDelta RN","", 800, 850)
c1 = ROOT.TCanvas("Delta RDelta RN","",50,50, W, H)
c1.SetFillColor(0)
c1.SetBorderMode(0)
c1.SetFrameFillStyle(0)
c1.SetFrameBorderMode(0)
c1.SetLeftMargin( L/W )
c1.SetRightMargin( R/W )
c1.SetTopMargin( T/H )
c1.SetBottomMargin( B/H )
c1.SetTickx(0)
c1.SetTicky(0)


EventSelection=False

def makeVariablePlots():
    integrals=[]
    for channel in channels:
        checkAndMakeDir(outDir+"/"+channel)
        triggers=["isBPH"]
        firststep=True
        for variable in variables:

            
            outFolder=outDir+"/"+channel+"/"+variable[0]+"/"
            checkAndMakeDir(outFolder)
            for trigger in triggers:
                hist="h_"+channel+"_"+variable[0]+"_"+trigger
                print (hist)
                SUSY_TH1F= SUSYFile.Get(hist)
                #Data_TH1F=DataFile.Get(hist)
                #SUSY_TH1F.Scale(33.7e3)
                #SUSY_TH1F.Rebin(2)
                #error_TH1F= BackgroundFile.Get(hist)
                #error_TH1F.Rebin(2)
                if firststep:
                    integrals.append(["SUSY", channel, SUSY_TH1F.Integral()])

                for back in Backgrounds:
                    back["histo"]=back["file"].Get(hist)
                    #back["histo"].Rebin(2)
                    #back["histo"].Scale(33.7e3)
                    if firststep:
                        integrals.append([back["name"], channel, back["histo"].Integral()])

                    back["histo"].SetFillColor(back["color"])
                firststep=False
                Backgrounds_Sorted = sorted(Backgrounds, key=lambda back:back["histo"].Integral(), reverse=True)


                Title = SUSY_TH1F.GetTitle()
                
                Background = ROOT.THStack("Background_"+hist,"")
                Background.SetTitle(" ;Y axis; Events")

                print(channel+"test2")
                for back in Backgrounds_Sorted:
                    print (back["name"]+" Integral = "+str(back["histo"].Integral(2,5))+"\n")
                    Background.Add(back["histo"])
                print ("Signal"+" Integral = "+str(SUSY_TH1F.Integral(2,5))+"\n")
                bkg = Background.GetStack().Last()
                n = SUSY_TH1F.GetNbinsX()
                bkgnEvents=0
                SOB=ROOT.TH1F("signal/sqrt(B)", hist+"_SOB" , n, SUSY_TH1F.GetXaxis().GetXmin(), SUSY_TH1F.GetXaxis().GetXmax())
                bins = []
                for i in range (0,n+1):
                    s=SUSY_TH1F.GetBinContent(i)

                    b=bkg.GetBinContent(i)
                    bkgnEvents+=b
                    if(s>0 and b>0):
                        e = s/(b**.5)
                        SOB.SetBinContent(i,e)
                        bins.append([i,e])
                print("\n")

                print(bins)
                print("\n")

                pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
                #CMS_lumi.CMS_lumi(pad1, iPeriod, iPos)

                pad1.SetBottomMargin(0) # Upper and lower plot are joined
                pad1.SetGridx()         # Vertical grid
                pad1.Draw()
                pad1.cd()
                pad1.SetLogy()

                Background.SetMinimum(.1)
                SUSY_TH1F.GetYaxis().SetTitle("Events")

                signEvents =SUSY_TH1F.Integral()
                #fullSOB= signEvents/(bkgnEvents**.5)
                #print (channel+" "+variable[0]+" "+trigger+ " Signal Vs Background = "+ str(fullSOB))

                #  TCP_l.Draw("same hist e")
                #  TCP_m.Draw("same hist e")
                #  TCP_h.Draw("same hist e")

                #error_TH1F.SetLineColor(ROOT.kBlue)
                SUSY_TH1F.SetMarkerStyle(ROOT.kFullCircle)
                #Background.SetStats(0)
                SUSY_TH1F.SetLineColor(ROOT.kBlack)
                Background.Draw("hist")
                SUSY_TH1F.Draw("same hist e1")

                #error_TH1F.Draw("same hist e1")
                #SUSY_TH1F.Draw("same hist e1")

                l = ROOT.TLegend(0.65,0.7,0.85,0.87)
                for back in Backgrounds_Sorted:
                    l.AddEntry(back["histo"],back["name"],"f")

                l.AddEntry(SUSY_TH1F, "Signal m_{a} = 12 GeV", "l")

                l.Draw("same")

                c1.cd()

                pad2 = ROOT.TPad("pad2", "pad2", 0, 0.1, 1, 0.3)
                pad2.SetTopMargin(0)
                pad2.SetBottomMargin(0.26)
                pad2.SetGridx() # vertical grid
                pad2.Draw()
                pad2.cd()

                SOB.Draw("ep")

                SOB.SetTitle("")
                SOB.SetStats(0)

                # Y axis ratio plot settings
                SOB.GetYaxis().SetTitle("ratio S/#sqrt{B}")

                SOB.GetYaxis().SetNdivisions(505)
                SOB.GetYaxis().SetTitleSize(20)
                SOB.GetYaxis().SetTitleFont(43)
                SOB.GetYaxis().SetTitleOffset(1.55)
                SOB.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                SOB.GetYaxis().SetLabelSize(15)

                # X axis ratio plot settings
                SOB.GetXaxis().SetTitle(titles[channel]+Title)
                SOB.GetXaxis().SetTitleSize(20)
                SOB.GetXaxis().SetTitleFont(43)
                SOB.GetXaxis().SetTitleOffset(4.)
                SOB.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                SOB.GetXaxis().SetLabelSize(15)

                SOB.SetLineWidth(2)
                CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
                c1.SaveAs(outFolder+hist+".png")
                c1.Clear()
        #Selections=["_isBPH_EventSelection","_isBPH_EventSelection_genMatchB"]
        Selections=["_isBPH_EventSelection"]
        if EventSelection:
            for seltype in Selections:
            #for trigger in triggers:
                outFolder = outDir+"/"+channel+"/Event_Selection/"
                checkAndMakeDir(outFolder)
                hist="h_"+channel+seltype
                SUSY_TH1F= SUSYFile.Get(hist)


                for back in Backgrounds:
                    back["histo"]=back["file"].Get(hist)
                    back["histo"].SetFillColor(back["color"])
                Backgrounds_Sorted = sorted(Backgrounds, key=lambda back:back["histo"].Integral(), reverse=True)


                Title = SUSY_TH1F.GetTitle()
                
                Background = ROOT.THStack("Background_"+hist,Title)


                print(channel+"test2")
                for back in Backgrounds_Sorted:
                    print (back["name"]+" Integral = "+str(back["histo"].Integral())+"\n")
                    Background.Add(back["histo"])

                bkg = Background.GetStack().Last()
                n = SUSY_TH1F.GetNbinsX()

                SOB=ROOT.TH1F("signal/sqrt(B)", hist+"_SOB" , n, SUSY_TH1F.GetXaxis().GetXmin(), SUSY_TH1F.GetXaxis().GetXmax())
                for i in range (0,n+1):
                    s=SUSY_TH1F.GetBinContent(i)
                    b=bkg.GetBinContent(i)
                    if(s>0 and b>0):
                        e = s/(b**.5)
                        SOB.SetBinContent(i,e)


                pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
                pad1.SetBottomMargin(0) # Upper and lower plot are joined
                pad1.SetGridx()         # Vertical grid
                pad1.Draw()             # Draw the upper pad: pad1
                pad1.cd()
                pad1.SetLogy()

                Background.SetMinimum(.1)
                Background.SetMinimum()

                Background.Draw("hist")
                #  TCP_l.Draw("same hist e")
                #  TCP_m.Draw("same hist e")
                #  TCP_h.Draw("same hist e")
                SUSY_TH1F.SetLineColor(ROOT.kRed)
                SUSY_TH1F.Draw("same hist e")





                SUSY_TH1F.SetLineWidth(2)

                l = ROOT.TLegend(0.65,0.7,0.85,0.87)
                for back in Backgrounds_Sorted:
                    l.AddEntry(back["histo"],back["name"],"f")

                l.AddEntry(SUSY_TH1F, "Signal m_{a} = 12 GeV", "l")

                l.Draw("same")

                c1.cd()

                pad2 = ROOT.TPad("pad2", "pad2", 0, 0.1, 1, 0.3)
                pad2.SetTopMargin(0)
                pad2.SetBottomMargin(0.2)
                pad2.SetGridx() # vertical grid
                pad2.Draw()
                pad2.cd()

                SOB.Draw("ep")

                SOB.SetTitle("")
                SOB.SetStats(0)

                # Y axis ratio plot settings
                SOB.GetYaxis().SetTitle("ratio S/#sqrt{B}")
                SOB.GetYaxis().SetNdivisions(505)
                SOB.GetYaxis().SetTitleSize(20)
                SOB.GetYaxis().SetTitleFont(43)
                SOB.GetYaxis().SetTitleOffset(1.55)
                SOB.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                SOB.GetYaxis().SetLabelSize(15)

                # X axis ratio plot settings
                #   SOB-GetXaxis().SetTitle("M_{e#mu}")
                SOB.GetXaxis().SetTitleSize(20)
                SOB.GetXaxis().SetTitleFont(43)
                SOB.GetXaxis().SetTitleOffset(4.)
                SOB.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
                SOB.GetXaxis().SetLabelSize(15)

                SOB.SetLineWidth(2)

                c1.SaveAs(outFolder+hist+".png")
                c1.Clear()
    #print("INTEGRALS")
    #chan=""
    #for integral in integrals:
    #    if integral[1]!=chan:
    #        print ("CHANNEL = "+ integral[1])
    #        chan=integral[1]
    #    print (integral[0]+ ": " +str(round(integral[2],2)))
    #print(integrals)
makeVariablePlots()
