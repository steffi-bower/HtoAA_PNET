#Usage: ./runOffGridpack.sh gridpack_file.tar.xz

#For lxplus
# export X509_USER_PROXY=$1
# voms-proxy-info -all
# voms-proxy-info -all -file $1
set -e
export BASEDIR=`pwd`


SAMPLENAME=$4
JOBNUM=$2
NAME=$1


export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

## Loading the latest CMSSW version in consistent with 
export SCRAM_ARCH=el8_amd64_gcc10



xrdcp root://cmseos.fnal.gov//eos/uscms/store/user/nbower/CMSSW.tgz ./CMSSW.tgz 
tar -xf CMSSW.tgz  
rm CMSSW.tgz 
cd CMSSW_12_4_20/src/higgstoaaAnalyzer/
xrdcp root://cmseos.fnal.gov//eos/uscms/store/user/nbower/2018_ElectronLoose.root ./ 
scramv1 b ProjectRename
eval `scram runtime -sh`
scram b -j 4
ls

FILELIST=$3
HTBIN=$5
cat $FILELIST
i=1 
REPLACEWITH="root://cmsio2.rc.ufl.edu/"
REPLACE="root://cmsxrootd.fnal.gov/"
while read line; do 
    file=${line/${REPLACE}/${REPLACEWITH}}
    xrdcp ${file} ./higgstoaaAnalyzer/python/filein_${i}.root
    i=$((i+1))
done < $FILELIST  
cd higgstoaaAnalyzer/python/ 
#xrdcp root://cmseos.fnal.gov/${FILELIST} ./filein.root 

#cmsRun higgstoaaAnalyzer/python/higgstoaaAnalyzer_cfg.py
#python 2018higgstoaa_NtupleAnalyzer.py
#python PNetJetIDStudies.py
#python3 PNet_EventLEvelTest.py
python3 htoAA_Analyzer_200824.py
echo "root://cmseos.fnal.gov//eos/uscms/store/user/nbower/plots/${SAMPLENAME}/${NAME}/${SAMPLENAME}_${NAME}_${JOBNUM}.root"
xrdcp ./Outfile.root root://cmseos.fnal.gov//eos/uscms/store/user/nbower/plots/${SAMPLENAME}/${NAME}/${HTBIN}/${SAMPLENAME}_${NAME}_${JOBNUM}.root

cd ../../..
rm -rf CMS*

echo "ALL Done"
