#!/bin/tcsh

setenv CMSSW_BASE /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/                    
cd $CMSSW_BASE/src/higgstoaaAnalyzer 

tar  --exclude="$CMSSW_BASE/src/higgstoaaAnalyzer/higgstoaaAnalyzer/graphs/*" --exclude="$CMSSW_BASE/src/higgstoaaAnalyzer/higgstoaaAnalyzer/plots/*" --exclude="*.root" --exclude="*.pdf" --exclude="*.gif" --exclude=.git --exclude="*.log" --exclude="*stderr" --exclude="*stdout" --exclude='*.png' --exclude="*tar*" -zcvf ../../../CMSSW.tgz ../../../CMSSW_12_4_20/

eosrm /eos/uscms/store/user/nbower/CMSSW.tgz
set LABEL = $1 #Label of our analysis
setenv ANA_LABEL $LABEL
@ RUNSIG = $2 #enter 1 to just run over signal
xrdcp ../../../CMSSW.tgz root://cmseos.fnal.gov//eos/uscms/store/user/nbower/CMSSW.tgz
dos2unix Run_condor_config.sh
#setenv SAMPLE SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD
#setenv SAMPLE SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_AOD
#setenv SAMPLE DYJetsToLL_M-50_2017_v9
#setenv SAMPLE WJetsToLNu_2017_MINIAOD 
#setenv SAMPLE QCD_HTBinned_TuneCP5_PSWeights_13TeV-RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1 
#setenv SAMPLE WZ_2017_MINIAOD 
#setenv SAMPLE TTJets_2017_v9_MINIAOD 
echo $LABEL
setenv ANALYSIS 1_3_QCD
set STDSAMPS =  (2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_Skimmed ZZ_2018_Skimmed WZ_2018_Skimmed WW_2018_Skimmed WJetstoLNu_2018_Skimmed DYJetsToLL_M-50_2018_Skimmed TTJets_2018_Skimmed)
#set STDSAMPS =  (2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_Skimmed TTJets_2018_NTuple)
#set STDSAMPS =  (2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_Skimmed )

set STDNAME = (SUSY_2018_NTuple ZZ_2018_Skimmed WZ_2018_Skimmed WW_2018_Skimmed WJetstoLNu_2018_Skimmed DYJetsToLL_M-50_2018_Skimmed TTJets_2018_NTuple)
#set STDNAME = (SUSY_2018_NTuple TTJets_2018_NTuple)
#set STDNAME = (SUSY_2018_NTuple )

set DYBINS = (10to50 50)
set QCDBins = (100to200 200to300 300to500 500to700 700to1000 1000to1500 1500to2000 2000toInf)
set STDBINS = (FULL_HT)
echo $RUNSIG
#echo $LABEL" : "$(date +%D)"\n" 

#set FILE = "./higgstoaaAnalyzer/fileLists/"$SAMPLE"/*"
@ BOOL=1
if ($RUNSIG == $BOOL) then
    setenv ANALYSIS $LABEL"_SIGNAL"
    setenv MEMORY 8000
    setenv SAMPLE ParkingBPH
    setenv HTBIN FULL_HT
    mkdir -p  "/eos/uscms/store/user/nbower/plots/"$SAMPLE"/"$ANALYSIS"/"$HTBIN
    echo $HTBIN
    set FILE = "./higgstoaaAnalyzer/fileLists/"$SAMPLE"/FULL_HT/*"
    #set FILE = "/eos/uscms/store/user/nbower/Events/"$SAMPLE"/"$HTBIN"/*" 
    @ N=1
    foreach DIR ($FILE)
        echo $DIR
        setenv INFI $DIR
        setenv JOBNUM $N
        setenv JOBNAME $SAMPLE"_"$HTBIN"_"$ANALYSIS"_"$N 
        @ N+=1
        condor_submit ./condor_Skimmed_2018.jdl  
    end
    setenv INSAMPS "ParkingBPH"
    python3 higgstoaaAnalyzer/python/MyArgs.py
else
    @ I=1
    setenv INSAMPS ""
    setenv MEMORY 8000
    foreach SAMP($STDSAMPS)
        setenv INSAMPS "$INSAMPS, $SAMP"  
        echo $STDNAME[$I]
        setenv ANALYSIS $LABEL"_"$STDNAME[$I]
        @ I+=1
        setenv SAMPLE $SAMP
        setenv HTBIN FULL_HT
        mkdir -p  "/eos/uscms/store/user/nbower/plots/"$SAMPLE"/"$ANALYSIS"/"$HTBIN
        echo $HTBIN
        echo $SAMPLE
        set FILE = "./higgstoaaAnalyzer/fileLists/"$SAMPLE"/"$HTBIN"/*"
        @ N=1
        foreach DIR ($FILE)
            echo $DIR
            setenv INFI $DIR
            setenv JOBNUM $N
            setenv JOBNAME $SAMPLE"_"$HTBIN"_"$ANALYSIS"_"$N 
            @ N+=1
            condor_submit ./condor_Skimmed_2018.jdl     
        end
    end
    echo $INSAMPS
    #setenv ANALYSIS $LABEL"_QCD_BGen_2018_NTuple"
    #setenv SAMPLE 'QCD_PtBin_2018'
    #setenv ANALYSIS $LABEL"_QCD_PtBin_2018_NTuple"
    #setenv SAMPLE 'QCD_BGen_2018_NTuple'
    #foreach BIN (15to30 30to50 50to80 80to120 120to170 170to300 300to470 470to600 600to800 800to1000 1000to1400 1400to1800)
    #foreach BIN (100to200 200to300 300to500 500to700 700to1000 1000to1500 1500to2000 2000toInf)
    #     setenv HTBIN $BIN
    #     mkdir -p  "/eos/uscms/store/user/nbower/plots/"$SAMPLE"/"$ANALYSIS"/"$HTBIN
    #     echo $HTBIN
    #     set FILE = "./higgstoaaAnalyzer/fileLists/"$SAMPLE"/"$HTBIN"/*"
    #     @ N=1
    #     foreach DIR ($FILE)
    #         echo $DIR
    #         setenv INFI $DIR
    #         setenv JOBNUM $N
    #         setenv JOBNAME $SAMPLE"_"$HTBIN"_"$ANALYSIS"_"$N 
    #         @ N+=1
    #         condor_submit ./condor_Skimmed_2018.jdl     
    #     end
    # end
    #setenv INSAMPS "$INSAMPS, $SAMPLE"  

    python3 higgstoaaAnalyzer/python/MyArgs.py


endif


