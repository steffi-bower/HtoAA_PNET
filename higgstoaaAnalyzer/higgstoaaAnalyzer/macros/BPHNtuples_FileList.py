import os
import subprocess
import sys,string,math,os
import glob
filesPerList=45

file_dict = {}
QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8=[]
QCD_Pt_120to170_TuneCP5_13TeV_pythia8=[]
QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8=[]
QCD_Pt_15to30_TuneCP5_13TeV_pythia8=[]
QCD_Pt_170to300_TuneCP5_13TeV_pythia8=[]
QCD_Pt_300to470_TuneCP5_13TeV_pythia8=[]
QCD_Pt_30to50_TuneCP5_13TeV_pythia8=[]
QCD_Pt_470to600_TuneCP5_13TeV_pythia8=[]
QCD_Pt_50to80_TuneCP5_13TeV_pythia8=[]
QCD_Pt_600to800_TuneCP5_13TeV_pythia8=[]
QCD_Pt_800to1000_TuneCP5_13TeV_pythia8=[]
QCD_Pt_80to120_TuneCP5_13TeV_pythia8=[]
QCD_Pt_15To20_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
QCD_Pt_20To50_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
QCD_Pt_50To80_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
QCD_Pt_80To120_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
QCD_Pt_120To170_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
QCD_Pt_170To300_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
QCD_Pt_300To470_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
QCD_Pt_470To600_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
QCD_Pt_600To800_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
QCD_Pt_800To1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
QCD_Pt_1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8=[]
###
#Datasets={
#    "QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8":QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_120to170_TuneCP5_13TeV_pythia8":QCD_Pt_120to170_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8":QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_15to30_TuneCP5_13TeV_pythia8":QCD_Pt_15to30_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_170to300_TuneCP5_13TeV_pythia8":QCD_Pt_170to300_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_300to470_TuneCP5_13TeV_pythia8":QCD_Pt_300to470_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_30to50_TuneCP5_13TeV_pythia8":QCD_Pt_30to50_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_470to600_TuneCP5_13TeV_pythia8":QCD_Pt_470to600_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_50to80_TuneCP5_13TeV_pythia8":QCD_Pt_50to80_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_600to800_TuneCP5_13TeV_pythia8":QCD_Pt_600to800_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_800to1000_TuneCP5_13TeV_pythia8":QCD_Pt_800to1000_TuneCP5_13TeV_pythia8,
#    "QCD_Pt_80to120_TuneCP5_13TeV_pythia8":QCD_Pt_80to120_TuneCP5_13TeV_pythia8,
#}

QCD_HT1000to1500_BGenFilter_TuneCP5_13TeV_madgraph_pythia8=[]
QCD_HT100to200_BGenFilter_TuneCP5_13TeV_madgraph_pythia8=[]
QCD_HT200to300_BGenFilter_TuneCP5_13TeV_madgraph_pythia8=[]
QCD_HT300to500_BGenFilter_TuneCP5_13TeV_madgraph_pythia8=[]
QCD_HT500to700_BGenFilter_TuneCP5_13TeV_madgraph_pythia8=[]
QCD_HT700to1000_BGenFilter_TuneCP5_13TeV_madgraph_pythia8=[]
QCD_HT1500to2000_BGenFilter_TuneCP5_13TeV_madgraph_pythia8=[]
QCD_HT2000toInf_BGenFilter_TuneCP5_13TeV_madgraph_pythia8=[]

Datasets={
    "QCD_HT1000to1500_BGenFilter_TuneCP5_13TeV-madgraph-pythia8":(QCD_HT1000to1500_BGenFilter_TuneCP5_13TeV_madgraph_pythia8,"1000to1500"),
    "QCD_HT100to200_BGenFilter_TuneCP5_13TeV-madgraph-pythia8":(QCD_HT100to200_BGenFilter_TuneCP5_13TeV_madgraph_pythia8,"100to200"),
    "QCD_HT200to300_BGenFilter_TuneCP5_13TeV-madgraph-pythia8":(QCD_HT200to300_BGenFilter_TuneCP5_13TeV_madgraph_pythia8,"200to300"),
    "QCD_HT300to500_BGenFilter_TuneCP5_13TeV-madgraph-pythia8":(QCD_HT300to500_BGenFilter_TuneCP5_13TeV_madgraph_pythia8,"300to500"),
    "QCD_HT500to700_BGenFilter_TuneCP5_13TeV-madgraph-pythia8":(QCD_HT500to700_BGenFilter_TuneCP5_13TeV_madgraph_pythia8,"500to700"),
    "QCD_HT700to1000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8":(QCD_HT700to1000_BGenFilter_TuneCP5_13TeV_madgraph_pythia8,"700to1000"),
    "QCD_HT1500to2000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8":(QCD_HT1500to2000_BGenFilter_TuneCP5_13TeV_madgraph_pythia8,"1500to2000"),
    "QCD_HT2000toInf_BGenFilter_TuneCP5_13TeV-madgraph-pythia8":(QCD_HT2000toInf_BGenFilter_TuneCP5_13TeV_madgraph_pythia8,"2000toInf"),

}

def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)

SampleName="QCD_BGen_2018_NTuples"
fileListDir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src//higgstoaaAnalyzer/higgstoaaAnalyzer/fileLists/"
Datasets=["DYJetsToLL_M-50_2018_Skimmed",
          "WJetstoLNu_2018_Skimmed",
          "WZ_2018_Skimmed",
          "WW_2018_Skimmed",
          "ZZ_2018_Skimmed",
          "TTJets_2018_Skimmed"
          ]
#Datasets=["ParkingBPH1","ParkingBPH2","ParkingBPH3","ParkingBPH4","ParkingBPH5","ParkingBPH6"]

for ds in Datasets:
    files=[]
    checkAndMakeDir(fileListDir+ds)

    subDataset= os.popen("xrdfs root://cmsio2.rc.ufl.edu/ ls -r /store/test/xrootd/T2_US_Florida/store/user/nbower/Events/"+ds).read()
    print(str("xrdfs root://cmsio2.rc.ufl.edu/ ls -r /store/test/xrootd/T2_US_Florida/store/user/nbower/Events/"+ds))
    for sd in subDataset.splitlines():
        eras= os.popen("xrdfs root://cmsio2.rc.ufl.edu/ ls -r "+ sd.rstrip()).read()
        for era in eras.splitlines():
            dates= os.popen("xrdfs root://cmsio2.rc.ufl.edu/ ls -r "+ era.rstrip()).read()
            for date in dates.splitlines():
                steps= os.popen("xrdfs root://cmsio2.rc.ufl.edu/ ls -r "+ date.rstrip()).read()
                for step in steps.splitlines():
                    print (step)
                    files+=os.popen("xrdfs root://cmsio2.rc.ufl.edu/ ls -r "+ step.rstrip()).read().splitlines()

    nf = 1
    checkAndMakeDir(fileListDir+ds+"/FULL_HT/")
    for file in files:
        
        filelistIdx=int((nf-1)/filesPerList)

        if nf%filesPerList==1:
            out=open(fileListDir+ds+"/FULL_HT/"+ds+"_"+str(filelistIdx)+".txt","w")
        out.write("root://cmsio2.rc.ufl.edu/"+file.replace("","")+"\n")
        nf+=1

