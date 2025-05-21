#! /bin/bash

MASS=$1
ANALYSIS=$2
SKIMMED=$3
ERA=$4
OUTDIR=/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_12_4_20/src/higgstoaaAnalyzer/higgstoaaAnalyzer/HaddFolder/
mkdir -p ${OUTDIR}
echo "${ERA}"
echo "${MASS}"

if [[ ${ERA} = 2017 ]]
then
    if [[ ${SKIMMED} = 1 ]]
    then
        if [[ ${MASS} = "QCD" ]]
        then
            PTBINS=(50to100 100to200 200to300 300to500  500to700 700to1000 1000to1500 1500to2000 2000toInf)
            FILEDIR=/store/user/nbower/plots/QCD_HTBinned_TuneCP5_PSWeights_13TeV-RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/
        elif [[ ${MASS} = "SUSY" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/
        elif [[ ${MASS} = "TTJets" ]]
        then 
            PTBINS=(FULL_HT)
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_Skimmed_LowPT/
            FILEDIR=/store/user/nbower/plots/TTJets_2017_v9_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/
        elif [[ ${MASS} = "WZ" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WZ_2017_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/
        elif [[ ${MASS} = "DY" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/DYJetsToLL_M-50_2017_v9/ 
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/
        elif [[ ${MASS} = "DYLowMass" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/DYJetsToLL_M-10To50_2017_v9/ 
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/

        elif [[ ${MASS} = "WJets" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WJetsToLNu_2017_MINIAOD/   
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/
        fi
    else

        if [[ ${MASS} = "QCD" ]]
        then
            PTBINS=(50to100 100to200 200to300 300to500  500to700 700to1000 1000to1500 1500to2000 2000toInf)
            FILEDIR=/store/user/nbower/plots/QCD_HTBinned_TuneCP5_PSWeights_13TeV-RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1_Skimmed/
        elif [[ ${MASS} = "SUSY" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_Skimmed/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/
        elif [[ ${MASS} = "TTJets" ]]
        then 
            PTBINS=(FULL_HT)
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_Skimmed_LowPT/
            FILEDIR=/store/user/nbower/plots/TTJets_2017_v9_MINIAOD_Skimmed/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/
        elif [[ ${MASS} = "WZ" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WZ_2017_MINIAOD_Skimmed/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/
        elif [[ ${MASS} = "DY" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/DYJetsToLL_M-50_2017_v9_Skimmed/ 
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/
        elif [[ ${MASS} = "DYLowMass" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/DYJetsToLL_M-10To50_2017_v9_Skimmed/ 
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/

        elif [[ ${MASS} = "WJets" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WJetsToLNu_2017_MINIAOD_Skimmed/   
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD/
            #FILEDIR=/store/user/nbower/plots/TCP_m_30_w_1_htj_BINNED_slc6_amd64_gcc630_MINIAOD_LooseLowPT_Drp1_pdgID/
        fi
        
    fi

elif [[ ${ERA} = 2018 ]]
then
    if [[ ${SKIMMED} = 0 ]]
    then
        if [[ ${MASS} = "SUSY_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD/   
        elif [[ ${MASS} = "WZTo3LNu_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WZTo3LNu_2018/   
        elif [[ ${MASS} = "ZZTo4L_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/ZZTo4L_2018/   
        elif [[ ${MASS} = "ZZ_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/ZZ_2018/   
        elif [[ ${MASS} = "ZZ_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/ZZ_2018/   
        elif [[ ${MASS} = "WZ_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WZ_2018/   
        
        elif [[ ${MASS} = "WJetsToLNu_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WJetsToLNu_2018/   
        elif [[ ${MASS} = "TTJets_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/TTJets_2018/   
        
        elif [[ ${MASS} = "QCD_Flat_MINIAOD_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/QCD_Flat_MINIAOD_2018/   
        elif [[ ${MASS} = "WW_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WW_2018/   
        elif [[ ${MASS} = "QCD_BGen_2018" ]]
        then 
            PTBINS=(100to200 200to300 300to500 500to700 700to1000 1000to1500 1500to2000 2000toInf)
            FILEDIR=/store/user/nbower/plots/QCD_BGen_2018/  
        elif [[ ${MASS} = "DYJetsToLL_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/DYJetsToLL_M-50_2018_Skimmed/   
        fi
    else
        if [[ ${MASS} = "SUSY_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_Skimmed/   
        elif [[ ${MASS} = "WZTo3LNu_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WZTo3LNu_2018_NTuple/   
        elif [[ ${MASS} = "ZZTo4L_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/ZZTo4L_2018_NTuple/   
        elif [[ ${MASS} = "ZZ_2018" ]]

        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/ZZ_2018_Skimmed/   
        elif [[ ${MASS} = "WZ_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WZ_2018_Skimmed/   
        
        elif [[ ${MASS} = "WJetstoLNu_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WJetstoLNu_2018_Skimmed/   
        elif [[ ${MASS} = "TTJets_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/TTJets_2018_NTuple/   
        
        elif [[ ${MASS} = "QCD_Flat_MINIAOD_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/QCD_Flat_MINIAOD_2018_NTuple/   
        elif [[ ${MASS} = "WW_2018" ]]
        then 
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/WW_2018_Skimmed/   
        elif [[ ${MASS} = "QCD_BGen_2018" ]]
        then 
            PTBINS=(100to200 200to300 300to500 500to700 700to1000 1000to1500 1500to2000 2000toInf)
            FILEDIR=/store/user/nbower/plots/QCD_BGen_2018_NTuple/ 
        elif [[ ${MASS} = "QCD_PtBin_2018" ]]
        then 
            PTBINS=(15to30 30to50 50to80 80to120 120to170 170to300 300to470 470to600 600to800 800to1000 1000to1400 1400to1800)
            FILEDIR=/store/user/nbower/plots/QCD_PtBin_2018/  
        elif [[ ${MASS} = "DYJetsToLL_M-50_2018" ]]
        then 
            echo "TEST"
            PTBINS=(FULL_HT)
            FILEDIR=/store/user/nbower/plots/DYJetsToLL_M-50_2018_Skimmed/   
        fi
    fi 
fi
echo "${PTBINS}"
for BIN in "${PTBINS[@]}"
do
    echo "${FILEDIR}/${ANALYSIS}/${BIN}/"
    echo "${OUTDIR}${BIN}.root"
    ls ${FILEDIR}/${ANALYSIS}/${BIN}/
    mkdir ${OUTDIR}/${ANALYSIS}
    xrdcp -r root://cmseos.fnal.gov/${FILEDIR}/${ANALYSIS}/${BIN}/ ${OUTDIR}/${ANALYSIS}/
    hadd -f ${OUTDIR}${BIN}.root ${OUTDIR}/${ANALYSIS}/${BIN}/*
done
