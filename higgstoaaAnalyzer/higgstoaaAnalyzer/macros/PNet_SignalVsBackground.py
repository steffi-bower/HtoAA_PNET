import ROOT
import sys
from ctypes import c_double
import subprocess
import string,math,os
import glob
import numpy as np
ROOT.gROOT.SetBatch(True)

label = sys.argv [1]
tag = sys.argv [2]
#hists = ["h_tauE_tauE_Mvis_EG" ,"h_tauE_tauE_Mvis_EGorDoubleEG","h_tauE_tauE_Mvis_noTrig","h_tauMu_tauE_Mvis_SingleMu", "h_tauMu_tauE_Mvis_EGorSingleMu" ,"h_tauMu_tauE_Mvis_MuEGorSingleMu" ,"h_tauMu_tauE_Mvis_noTrig", "h_tauMu_tauMu_Mvis_SingleMu", "h_tauMu_tauMu_Mvis_SingleMuorDoubleMu","h_tauMu_tauMu_Mvis_noTrig"]
#hists = ["h_MET"]
channels = ["tauE_tauE","tauE_tauMu","tauMu_tauMu","tauHad_tauMu","tauHad_tauE"]
channels = ["tauE_tauMu","tauHad_tauMu","tauHad_tauE"]
variables= [

    ["b1_ID_Total","b1 Total ID Value",[1000,0,1]],
    ["b1_PNetID","b1 PNet ID Value",[1000,0,1]],
    ["Mvis","Mvis",[20,0,20]],
    ["bMass","bMass",[20,0,20]],
    ["lep1Pt","lep1 Pt (GeV)",[25,0,75]],
    ["lep2Pt","lep2 Pt (GeV)",[25,0,75]],
    ["lepDr","DeltaR (leptons)",[20,0,1.5]],
    ["lep1DRB","DeltaR (bL1)",[20,0,4]],
    ["lep2DRB","DeltaR (bL2)",[20,0,4]],
    ["MET","MET (GeV)",[10,0,100]],
    ["NLep1s","NLep1s",[5,0,5]],
    ["NLep2s","NLep2s",[5,0,5]],
    ["eleIso","eleIso",[5,0,5]],
    ["muIso","muIso",[20,0,5]],
    

    ]
muonTrigs= [("isBPH",ROOT.kMagenta),("isIsoMu",ROOT.kMagenta),("isDoubleMuSS",ROOT.kRed), ("isDoubleMuMass8",ROOT.kBlue),("isDoubleMuMass3p8",ROOT.kGreen),("isDoubleMu",ROOT.kCyan)]
electronTrigs =  [("isBPH",ROOT.kMagenta),("isIsoEle",ROOT.kRed),("isMuonEG",ROOT.kBlue),("isDoubleEG",ROOT.kGreen)]


plotfolder = "/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/"
outDir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/graphs/"+label+"_"+tag+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)      
checkAndMakeDir(outDir)
#QCDFile =ROOT.TFile.Open(plotfolder+label+"_QCD_PtBin_2018_NTuple.root" ,"READ")
QCDFile =ROOT.TFile.Open(plotfolder+label+"_QCD_BGen_2018_NTuple.root" ,"READ")

TTBarFile = ROOT.TFile.Open(plotfolder+label+"_TTJets_2018_NTuple.root" ,"READ")
SUSYFile = ROOT.TFile.Open(plotfolder+label+"_SUSY_2018_NTuple.root" ,"READ")
Backgrounds = [

{"file":TTBarFile,"name":"TTBar","color":ROOT.kCyan},
{"file":QCDFile,"name":"QCD BGen","color":ROOT.kGray},
]
c1 = ROOT.TCanvas("Delta RDelta RN","", 800, 850)





def makeVariablePlots():
    integrals=[]
    errors = []
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
                #SUSY_TH1F.Scale(33.7e3)
                if "Mvis" in hist:

                    integral= SUSY_TH1F.IntegralAndError(4,11,x_err)
                    integrals.append(["SUSY", channel, integral,x_err])
                if firststep:
                    x_err = c_double(0.)

                for back in Backgrounds:
                    back["histo"]=back["file"].Get(hist)
                    #back["histo"].Scale(33.7e3)
                    if "Mvis" in hist:
                        integral=back["histo"].IntegralAndError(4,11,x_err)
                        integrals.append([back["name"], channel, integral,x_err])

                    if firststep:
                        x_err = c_double(0.)


                    back["histo"].SetFillColor(back["color"])
                firststep=False
                Backgrounds_Sorted = sorted(Backgrounds, key=lambda back:back["histo"].Integral(), reverse=True)


                Title = SUSY_TH1F.GetTitle()
                
                Background = ROOT.THStack("Background_"+hist,Title)


                print(channel+"test2")
                for back in Backgrounds_Sorted:
                    print (back["name"]+" Integral = "+str(back["histo"].Integral())+"\n")
                    Background.Add(back["histo"])

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
                pad1.SetBottomMargin(0) # Upper and lower plot are joined
                pad1.SetGridx()         # Vertical grid
                pad1.Draw()             # Draw the upper pad: pad1
                pad1.cd()
                pad1.SetLogy()

                Background.SetMinimum(.1)
                signEvents =SUSY_TH1F.Integral(4,11)
                QCDEvents =SUSY_TH1F.Integral(4,11)
                TTJEvents =SUSY_TH1F.Integral(4,11)
                fullSOB= signEvents/(bkgnEvents**.5)
                print (channel+" "+variable[0]+" "+ " Signal Vs Background = "+ str(fullSOB))

                Background.Draw("hist")
                #  TCP_l.Draw("same hist e")
                #  TCP_m.Draw("same hist e")
                #  TCP_h.Draw("same hist e")

                SUSY_TH1F.Draw("same hist e")



                SUSY_TH1F.SetLineColor(ROOT.kBlack)


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
        #Selections=["_isBPH_EventSelection","_isBPH_EventSelection_genMatchB"]
        Selections=["_isBPH_EventSelection"]
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

            SUSY_TH1F.Draw("same hist e")



            SUSY_TH1F.SetLineColor(ROOT.kBlack)


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
    print("INTEGRALS")
    chan=""
    for integral in integrals:
        if integral[1]!=chan:
            print ("CHANNEL = "+ integral[1])
            chan=integral[1]
        print (integral[0]+ ": " +str(round(integral[2],2))+" +- " +str(integral[3]))
    print(integrals)
makeVariablePlots()