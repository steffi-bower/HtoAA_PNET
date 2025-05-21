#! /bin/bash

FILELIST=$1
ANALYSIS=$2
SKIMMED=$3
ERA=$4
OUTDIR=/uscms_data/d3/nbower/FSU/HtoAA/Analyzer/CMSSW_10_6_26/src/higgstoaaAnalyzer/higgstoaaAnalyzer/TempDir/
mkdir -p ${OUTDIR}
echo "${ERA}"
echo "${MASS}"
FILESTOADD=""
echo "${PTBINS}"
cat $FILELIST
while read line; do 
    xrdcp ${line} ./filein_${i}.root 
done < $FILELIST
for BIN in "${PTBINS[@]}"
do
    echo "${FILEDIR}/${ANALYSIS}/${BIN}/"
    echo "${OUTDIR}${BIN}.root"
    ls ${FILEDIR}/${ANALYSIS}/${BIN}/
    hadd -f ${OUTDIR}.root ${FILEDIR}/${ANALYSIS}/${BIN}/*
done
