#! /bin/bash

LABEL=$1
HISTS=(h_tauE_TauE_Mvis_EG h_tauE_TauE_Mvis_EGorDoubleEG h_tauE_TauE_Mvis_noTrig h_tauMu_TauE_Mvis_SingleMu h_tauMu_TauE_Mvis_EGorSingleMu h_tauMu_TauE_Mvis_MuEGorSingleMu h_tauMu_TauE_Mvis_noTrig h_tauMu_TauMu_Mvis_SingleMu h_tauMu_TauMu_Mvis_SingleMuorDoubleMu h_tauMu_TauMu_Mvis_noTrig)

for HIST in "${HISTS[@]}"
do
    python /uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/macros/Tstack_Plotter.py $LABEL $HIST
done