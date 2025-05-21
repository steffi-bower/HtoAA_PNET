import subprocess
import sys,string,math,os
import glob
import numpy as np


#filesPerList=1000
filesPerList=25


#SampleName = sys.argv [1]
SampleName = "2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_Skimmed"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)

if "QCD" in SampleName:
    masses = ['100to200', '200to300','300to500','500to700','700to1000','1000to1500','1500to2000','2000toInf']
    #masses = ['QCD_Pt_15to30_TuneCP5_13TeV_pythia8','QCD_Pt_30to50_TuneCP5_13TeV_pythia8','QCD_Pt_50to80_TuneCP5_13TeV_pythia8','QCD_Pt_80to120_TuneCP5_13TeV_pythia8','QCD_Pt_120to170_TuneCP5_13TeV_pythia8','QCD_Pt_170to300_TuneCP5_13TeV_pythia8','QCD_Pt_300to470_TuneCP5_13TeV_pythia8','QCD_Pt_470to600_TuneCP5_13TeV_pythia8','QCD_Pt_600to800_TuneCP5_13TeV_pythia8','QCD_Pt_800to1000_TuneCP5_13TeV_pythia8','QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8','QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8','QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8','QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8','QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8']
elif "DY" in SampleName:
    masses = ['10to50', '50']
else:
    masses = ['FULL_HT']
    #masses = ['']
for Mass in masses:
    first_step=True

    fileListDir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/fileLists/"+SampleName+"/"+Mass+"/"
    checkAndMakeDir("/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/fileLists/"+SampleName+"/")

    if first_step==True:
        print(fileListDir)
        checkAndMakeDir(fileListDir)
        clearDir(fileListDir)
    #rootFileDir="/eos/uscms/store/user/nbower/Events/"+"QCD_HT"+Mass+"_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/"
    #rootFileDir="/eos/uscms/store/user/nbower/Events/"+"TTJets_2018_Skimmed/"
    #rootFileDir="/eos/uscms/store/user/nbower/Events/ParkingBPH1/ParkingBPH1_Run2018A-05May2019-v1_Skimmed/ParkingBPH1/"
    rootFileDir="/eos/uscms/store/user/nbower/Events/HtoAA_2018_SecondGeneration_Skimmed_BOOSTEDDITAU/12GeV/"
    first_step=False
    nf = 1
    listCounter = 0
    #fu = [y for x in os.walk(rootFileDir) for y in glob(os.path.join(x[0], '*.root'))]        
    #fu = glob.glob("/eos/uscms/store/user/nbower/Events/"+SampleName+"/"+Mass+"/**/*.root", recursive=True)
    fu = []
    for root , dirs, files in os.walk(rootFileDir):
        print (root)
        print (dirs)
        print(files)
        rootdir=root
        #while len(dirs) != 0:
        #    rootdir= (os.path.join(rootdir, dirs[0]))
        #    for root1 , dirs1, files1 in os.walk(rootdir):
        #        dirs = dirs1
        print("Test")
        for file1 in files:
            filestring = root+"/"+file1
            fu.append(filestring)
        #for root1 , dirs1, files1 in os.walk(rootdir):
            #print(root1)
            #print(str(len(files1)))
            #for file1 in files1:
                #filestring = root1+"/"+file1
                #append(filestring)

    for filename in fu:
        filelistIdx=int((nf-1)/filesPerList)
        if nf%filesPerList==1:
            out=open(fileListDir+"/"+SampleName+"_"+str(filelistIdx)+".txt","w")
        out.write("root://cmseos.fnal.gov/"+filename.replace("/eos/uscms","")+"\n")
        nf+=1
    print (str(len(fu)))
