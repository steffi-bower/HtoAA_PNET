import subprocess
import sys,string,math,os
import ConfigParser
import glob
import numpy as np
#from sampleAndMasses2018 import *

filesPerList= 2


def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)

if __name__ == "__main__":

    samples = ['DYJetsToLL_2018', 'ZZTo4L_2018', 'ZZ_2018', 'WZ_2018', 'WW_2018', 'WJetsToLNu_2018', 'TTJets_2018','QCD_Flat_MINIAOD_2018']
    #samples =  ['QCD_BGen_2018'] 
    for samp in samples:
        Sample=samp

        if Sample=="TTJets_2018":
            masses = ['']
            preSearchString="/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM"
            prefilename="TTJets_2018"
            topFolder=prefilename
            prefix = "root://xrootd.unl.edu/"
        elif Sample=="WJetsToLNu_2018":
            masses = ['']
            preSearchString="/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM"
            prefilename="WJetsToLNu_2018"
            topFolder=prefilename
            prefix = "root://xrootd.unl.edu/"
        elif Sample=="WW_2018":
            masses = ['']
            preSearchString="/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM"
            prefilename="WW_2018"
            topFolder=prefilename
            prefix = "root://xrootd.unl.edu/"
        elif Sample=="WZ_2018":
            masses = ['']
            preSearchString="/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM"
            prefilename="WZ_2018"
            topFolder=prefilename
            prefix = "root://xrootd.unl.edu/"
        elif Sample=="ZZ_2018":
            masses = ['']
            preSearchString="/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM"
            prefilename="ZZ_2018"
            topFolder=prefilename
            prefix = "root://xrootd.unl.edu/"
        elif Sample=="WZTo3LNu_2018":
            masses = ['']
            preSearchString="/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"
            prefilename="WZTo3LNu_2018"
            topFolder=prefilename
            prefix = "root://xrootd.unl.edu/"
        elif Sample=="ZZTo4L_2018":
            masses = ['']
            preSearchString="/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"
            prefilename="ZZTo4L_2018"
            topFolder=prefilename
            prefix = "root://xrootd.unl.edu/"
        elif Sample=="Pileup":
            masses = ['']
            preSearchString="/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW"
            prefilename="Pileup"
            topFolder=prefilename
            prefix = "root://xrootd.unl.edu/"
        elif Sample == "QCD_Flat_MINIAOD_2018":
            masses = ['']
            preSearchString="/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"

            prefilename = "QCD_Flat_MINIAOD_2018"
            prefix = "root://xrootd.unl.edu/"
            topFolder = "QCD_Flat_MINIAOD_2018"
        elif Sample == "QCD_BGen_2018":
            masses = ['100to200','200to300','300to500','500to700','700to1000','1000to1500','1500to2000','2000toInf']
            preSearchString="/QCD_HTREPLACEME_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"

            prefilename = "QCD_BGen_2018"
            prefix = "root://xrootd.unl.edu/"
            topFolder = "QCD_BGen_2018"

        elif Sample == 'DYJetsToLL_2018':
            masses=["10to50",'50']
            preSearchString="/DYJetsToLL_M-REPLACEME_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-vVERSION/MINIAODSIM"
            prefix="root://xrootd.unl.edu/"
            prefilename="DYJetsToLL_M-REPLACEME_2018"
            topFolder='DYJetsToLL_2018'

        else:
            print "Please Specify Sample Name!"
            sys.exit()
        first_step=True
        for mass in masses:
#            fileListDir="./filelists_LM/"+Sample+"/"+mass+"/"
#            checkAndMakeDir("./filelists_LM/"+Sample)
            filename = prefilename.replace("REPLACEME",mass)
            #fileListDir="/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/fileLists/"+topFolder+"/"
            fileListDir="/uscms_data/d3/nbower/FSU/HtoAA/Skimmer/CMSSW_12_1_0_pre3/src/BoostedDiTau/fileLists/"+topFolder+"/" 
            if first_step==True:
                checkAndMakeDir(fileListDir)
                clearDir(fileListDir)
            
            print (mass)
            first_step=False
            fileListDir=fileListDir+mass+"/"
            checkAndMakeDir(fileListDir)
            searchString=preSearchString.replace("REPLACEME",mass)
            if mass == "10to50":
                searchString=searchString.replace("VERSION","1")
            elif mass == "50":
                searchString=searchString.replace("VERSION","2")
            os.system('dasgoclient --query "'+searchString+'"')
            query = 'dasgoclient --query "file dataset='+searchString+'"'
            files=os.popen(query).read().split()
            
            for nf in range(1, len(files)+1):
                filelistIdx=int((nf-1)/filesPerList)
                if nf%filesPerList==1:
                    out=open(fileListDir+filename+"_"+str(filelistIdx)+".txt","w")
                out.write(prefix+files[nf-1]+"\n")
            
