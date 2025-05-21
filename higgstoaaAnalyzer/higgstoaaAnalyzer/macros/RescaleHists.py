import ROOT
import sys
import Cross_Sections
import os
import subprocess

analysislabel = sys.argv [1]
skimmed = sys.argv [2]
era = sys.argv [3]
samples = ["QCD","SUSY","TTJets","WZ","WJets","WZ","DY","DYLowMass"]
os.popen("dos2unix /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/macros/HaddByBin.sh")
if era == "2018":
    #samples = ['SUSY_2018', 'DYJetsToLL_2018', 'WZTo3LNu_2018', 'ZZTo4L_2018', 'ZZ_2018', 'WZ_2018', 'WW_2018', 'WJetsToLNu_2018', 'TTJets_2018']
    #samples = ['SUSY_2018', 'DYJetsToLL_2018', 'WZTo3LNu_2018', 'ZZTo4L_2018', 'ZZ_2018', 'WZ_2018', 'WJetsToLNu_2018', 'TTJets_2018']
    #samples = ['SUSY_2018', 'DYJetsToLL_2018',  'ZZ_2018', 'WZ_2018', 'WJetsToLNu_2018', 'TTJets_2018']
    #samples = ['SUSY_2018', 'DYJetsToLL_M-50_2018',  'ZZ_2018', 'WZ_2018', 'WJetstoLNu_2018', 'TTJets_2018','QCD_BGen_2018','WW_2018']
    samples=['SUSY_2018','TTJets_2018']
    #samples=['QCD_PtBin_2018','SUSY_2018','TTJets_2018']
def RescaleHist_Skimmed(samp_mass):
    Lumi=41.5e3

    if samp_mass=="QCD":
        xsecs_dict=Cross_Sections.QCD_2017_xsecs
    if samp_mass=="SUSY":
        xsecs_dict=Cross_Sections.SUSY_xsecs
    if samp_mass=="TTJets":
        xsecs_dict=Cross_Sections.TTBar_xsecs
    if samp_mass=="WZ":
        xsecs_dict=Cross_Sections.WZ_xsecs
    if samp_mass=="WJets":
        xsecs_dict=Cross_Sections.WJetstoLL_xsecs
    if samp_mass=="DY":
        xsecs_dict=Cross_Sections.DY_xsecs
    if samp_mass=="DYLowMass":
        xsecs_dict=Cross_Sections.DY_LowMass_xsecs
    if samp_mass == "QCD_BGen_2018":
        xsecs_dict=Cross_Sections.QCD_BFilter_2018_xsecs    
    if samp_mass == "QCD_PtBin_2018":
        xsecs_dict=Cross_Sections.QCD_PtBin_2018_xsecs

    file_dict = {}
    label=analysislabel+"_"+samp_mass
    os.popen("dos2unix /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/macros/HaddByBin.sh")
    os.popen('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/macros/HaddByBin.sh '+samp_mass+ ' '+label+' '+"1" )
    #build A dictionary with all files mapped to their given ptbin
    filedir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder/"
    #build a list of histograms and thier associated types
    OutHists={}
    i=0
    firstFile=True
    print(samp_mass)
    for ptbin in xsecs_dict:
        print(ptbin)
        infile =ROOT.TFile.Open(filedir+ptbin+".root" ,"READ")
        nEvents_Integral = infile.Get('h_nEvent_tauHad_tauE').Integral(0,1)
        nEvents_Integral_Full = infile.Get('h_nEvent_tauHad_tauE').Integral()
        #nEvents_Bin_content= infile.Get('simple/h_nEvent_tauE_tauE').GetBinContent("Total Events")
        print("Integral NEvents = " + str(nEvents_Integral)+ "PTBin = "+str(ptbin))
        print("Integral Scale Factor = "+str(xsecs_dict[ptbin]/nEvents_Integral*Lumi))
        print("Full NEvents = " + str(nEvents_Integral_Full))
        #print("BinContent Scale Factor = "+str(xsecs_dict[ptbin]/nEvents_Bin_content*Lumi))
        
        for h in infile.GetListOfKeys():
            h = h.ReadObj()
            HistType=h.ClassName()
            HistName=h.GetName()
            hist=infile.Get(HistName)
            hist.Scale(xsecs_dict[ptbin]/nEvents_Integral*Lumi)
            if firstFile==True:
                OutHists[HistName]=hist.Clone()
                OutHists[HistName].SetDirectory(0)
            else: OutHists[HistName].Add(hist)


        firstFile=False
    OutFile =ROOT.TFile( '/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+'.root',"RECREATE")
    for histname in OutHists:
        OutHists[histname].Write()
    OutFile.Close()
    os.popen("rm -rf /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder/*")
    os.popen("rm -rf /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder")

def RescaleHist_WholeMilk(samp_mass):
    Lumi=41.5e3

    if samp_mass=="QCD":
        xsecs_dict=Cross_Sections.QCD_2017_xsecs
    if samp_mass=="SUSY":
        xsecs_dict=Cross_Sections.SUSY_xsecs
    if samp_mass=="TTJets":
        xsecs_dict=Cross_Sections.TTBar_xsecs
    if samp_mass=="WZ":
        xsecs_dict=Cross_Sections.WZ_xsecs
    if samp_mass=="WJets":
        xsecs_dict=Cross_Sections.WJetstoLL_xsecs
    if samp_mass=="DY":
        xsecs_dict=Cross_Sections.DY_xsecs
    if samp_mass=="DYLowMass":
        xsecs_dict=Cross_Sections.DY_LowMass_xsecs

    file_dict = {}
    label=analysislabel+"_"+samp_mass
    os.popen("dos2unix /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/macros/HaddByBin.sh")
    os.popen('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/macros/HaddByBin.sh '+samp_mass+ ' '+label+" 0" )
    #build A dictionary with all files mapped to their given ptbin
    filedir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder/"
    #build a list of histograms and thier associated types
    OutHists={}
    i=0
    firstFile=True
    print(samp_mass)
    for ptbin in xsecs_dict:
        print(ptbin)
        infile =ROOT.TFile.Open(filedir+ptbin+".root" ,"READ")
        nEvents_Integral = infile.Get('simple/h_nEvent_tauE_tauE').Integral(0,1)
        nEvents_Integral_Full = infile.Get('simple/h_nEvent_tauE_tauE').Integral()
        #nEvents_Bin_content= infile.Get('simple/h_nEvent_tauE_tauE').GetBinContent("Total Events")
        print("Integral NEvents = " + str(nEvents_Integral)+ "PTBin = "+str(ptbin))
        print("Integral Scale Factor = "+str(xsecs_dict[ptbin]/nEvents_Integral*Lumi))
        print("Full NEvents = " + str(nEvents_Integral_Full))
        #print("BinContent Scale Factor = "+str(xsecs_dict[ptbin]/nEvents_Bin_content*Lumi))
        TDir=infile.Get("simple")
        for h in TDir.GetListOfKeys():
            h = h.ReadObj()
            HistType=h.ClassName()
            HistName=h.GetName()
            hist=TDir.Get(HistName)
            hist.Scale(xsecs_dict[ptbin]/nEvents_Integral*Lumi)
            if firstFile==True:
                OutHists[HistName]=hist.Clone()
                OutHists[HistName].SetDirectory(0)
            else: OutHists[HistName].Add(hist)


        firstFile=False
    OutFile =ROOT.TFile( '/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+'.root',"RECREATE")
    for histname in OutHists:
        OutHists[histname].Write()
    OutFile.Close()
    os.popen("rm -rf /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder/*")
    os.popen("rm -rf /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder")
def RescaleHist_18_WholeMilk(samp_mass):
    if samp_mass=="WZTo3LNu_2018":
        xsecs_dict=Cross_Sections.WZTo3LNu_2018_xsecs
    if samp_mass=="ZZTo4L_2018":
        xsecs_dict=Cross_Sections.ZZTo4L_2018_xsecs
    if samp_mass=="ZZ_2018":
        xsecs_dict=Cross_Sections.ZZ_2018_xsecs
    if samp_mass=="WZ_2018":
        xsecs_dict=Cross_Sections.WZ_2018_xsecs
    if samp_mass=="WW_2018":
        xsecs_dict=Cross_Sections.WW_2018_xsecs
    if samp_mass=="DYJetsToLL_M-50_2018":
        xsecs_dict=Cross_Sections.DYJetsToLL_2018_xsecs
    if samp_mass=="WJetsToLNu_2018":
        xsecs_dict=Cross_Sections.WJetsToLNu_2018_xsecs
    if samp_mass=="TTJets_2018":
        xsecs_dict=Cross_Sections.TTJets_2018_xsecs
    if samp_mass=="QCD_Flat_MINIAOD_2018":
        xsecs_dict=Cross_Sections.QCD_Flat_2018_xsecs
    if samp_mass == "SUSY_2018":
        xsecs_dict=Cross_Sections.SUSY_2018_xsecs
    if samp_mass == "QCD_BGen_2018":
        xsecs_dict=Cross_Sections.QCD_BFilter_2018_xsecs

    label=analysislabel+"_"+samp_mass
    print ("test")
    os.popen("dos2unix /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/macros/HaddByBin.sh")
    os.popen('/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/macros/HaddByBin.sh '+samp_mass+ ' '+label+" 0 2018" )
    #build A dictionary with all files mapped to their given ptbin
    filedir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder/"
    #build a list of histograms and thier associated types
    OutHists={}
    i=0
    firstFile=True
    print(samp_mass)
    for ptbin in xsecs_dict:
        print(ptbin)
        infile =ROOT.TFile.Open(filedir+ptbin+".root" ,"READ")
        nEvents_Integral = infile.Get('simple/h_nEvent_tauE_tauE').Integral(0,1)
        nEvents_Integral_Full = infile.Get('simple/h_nEvent_tauE_tauE').Integral()
        #nEvents_Bin_content= infile.Get('simple/h_nEvent_tauE_tauE').GetBinContent("Total Events")

        #print("BinContent Scale Factor = "+str(xsecs_dict[ptbin]/nEvents_Bin_content*Lumi))
        TDir=infile.Get("simple")
        for h in TDir.GetListOfKeys():
            h = h.ReadObj()
            HistType=h.ClassName()
            HistName=h.GetName()
            hist=TDir.Get(HistName)
            if "Trigger" in HistName:
                Lumi = 1
            else:
                Lumi = 59.83e3 # Taken from https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM (Luminosity POG)

            hist.Scale(xsecs_dict[ptbin]/nEvents_Integral*Lumi)
            if firstFile==True:
                OutHists[HistName]=hist.Clone()
                OutHists[HistName].SetDirectory(0)
            else: OutHists[HistName].Add(hist)


        firstFile=False
    OutFile =ROOT.TFile( '/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+'.root',"RECREATE")
    for histname in OutHists:
        OutHists[histname].Write()
    OutFile.Close()
    os.popen("rm -rf /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder/*")
    os.popen("rm -rf /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder")
def RescaleHist_18_Skimmed(samp_mass):
    if samp_mass=="WZTo3LNu_2018":
        xsecs_dict=Cross_Sections.WZTo3LNu_2018_xsecs
    if samp_mass=="ZZTo4L_2018":
        xsecs_dict=Cross_Sections.ZZTo4L_2018_xsecs
    if samp_mass=="ZZ_2018":
        xsecs_dict=Cross_Sections.ZZ_2018_xsecs
    if samp_mass=="WZ_2018":
        xsecs_dict=Cross_Sections.WZ_2018_xsecs
    if samp_mass=="WW_2018":
        xsecs_dict=Cross_Sections.WW_2018_xsecs
    if samp_mass=="DYJetsToLL_M-50_2018":
        xsecs_dict=Cross_Sections.DYJetsToLL_2018_xsecs
    if samp_mass=="WJetstoLNu_2018":
        xsecs_dict=Cross_Sections.WJetsToLNu_2018_xsecs
    if samp_mass=="TTJets_2018":
        xsecs_dict=Cross_Sections.TTJets_2018_xsecs
    if samp_mass=="QCD_Flat_MINIAOD_2018":
        xsecs_dict=Cross_Sections.QCD_Flat_2018_xsecs
    if samp_mass == "SUSY_2018":
        xsecs_dict=Cross_Sections.SUSY_2018_xsecs
    if samp_mass == "QCD_BGen_2018":
        xsecs_dict=Cross_Sections.QCD_BFilter_2018_xsecs
    if samp_mass == "QCD_PtBin_2018":
        xsecs_dict=Cross_Sections.QCD_PtBin_2018_xsecs
    if samp_mass=="QCD_PtBin_2018" or samp_mass=="SUSY_2018" or samp_mass=="QCD_BGen_2018" or samp_mass=="TTJets_2018":
        label=analysislabel+"_"+samp_mass+"_NTuple"
    else:
        label=analysislabel+"_"+samp_mass+"_Skimmed"
    print ("test")
    os.popen("dos2unix /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/macros/HaddByBin.sh")
    cmd=['/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/macros/HaddByBin.sh' ,samp_mass, label, str(1), str(2018)]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='') # process line here

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, p.args)
    #build A dictionary with all files mapped to their given ptbin
    filedir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder/"
    #build a list of histograms and thier associated types
    OutHists={}
    i=0
    firstFile=True
    print(samp_mass)
    for ptbin in xsecs_dict:
        print(ptbin)
        infile =ROOT.TFile.Open(filedir+ptbin+".root" ,"READ")
        totalevents= infile.Get("h_nEvents").GetBinContent(2)
        print ("TotalEvents "+ samp_mass+" " + ptbin+ " "+str(totalevents))
        #nEvents_Bin_content= infile.Get('simple/h_nEvent_tauE_tauE').GetBinContent("Total Events")

        #print("BinContent Scale Factor = "+str(xsecs_dict[ptbin]/nEvents_Bin_content*Lumi))
        #TDir=infile.Get("simple")
        for h in infile.GetListOfKeys():
            h = h.ReadObj()
            HistType=h.ClassName()
            HistName=h.GetName()
            hist=infile.Get(HistName)
            #if "Trigger" in HistName:
            #    Lumi = 1
            #else:
            #    Lumi = 59.83e3 # Taken from https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM (Luminosity POG)

            hist.Scale(xsecs_dict[ptbin]/totalevents)
            if "Mvis" in HistName:
                print("SCALE FOR " + samp_mass+ " " + ptbin)
                print(xsecs_dict[ptbin]/totalevents)

                print(HistName+" Integral  = ")
                print (hist.Integral())
            if firstFile==True:
                OutHists[HistName]=hist.Clone()
                OutHists[HistName].SetDirectory(0)
            else: OutHists[HistName].Add(hist)


        firstFile=False
    OutFile =ROOT.TFile( '/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/'+label+'.root',"RECREATE")
    for histname in OutHists:
        OutHists[histname].Write()
    OutFile.Close()
    os.popen("rm -rf /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder/*")
    os.popen("rm -rf /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder")
#RescaleHist('SUSY')
#RescaleHist('DYLowMass')
for sample in samples:
    if era =="2017":
        if skimmed=="1":
            RescaleHist_Skimmed(sample)
        else:
            RescaleHist_WholeMilk(sample)
    elif era == "2018":
        if skimmed == "1":
            RescaleHist_18_Skimmed(sample)
        else:
            RescaleHist_18_WholeMilk(sample)
        
