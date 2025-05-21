#Sample = 'QCD_MINIAOD'
#Sample = 'DYJetsToLL_94X'
#Sample = 'DYJetsToLL'
#Sample = 'DYJetsToLLNLO'
#Sample = 'TTJets'
#Sample = 'DYJetsToLL2018'
#Sample = 'WZTo3LNu_2018'
#Sample = 'ZZTo4L_2018'
#Sample = 'ZZ_2018'
#Sample = 'WZ_2018'
#Sample = 'WW_2018'
#Sample = 'WJetsToLNu_2018'
#Sample = 'TTJets_2018'
#Sample="DYJetsToLL2018"
isHad = True
isCopy=True
version="vplots"
isGen=False
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
    prefilename="ZZ_2018"
    topFolder=prefilename
    prefix = "root://xrootd.unl.edu/"
elif Sample=="Pileup":
    masses = ['']
    preSearchString="/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW"
    prefilename="Pileup"
    topFolder=prefilename
    prefix = "root://xrootd.unl.edu/"
elif Sample == "QCD_MINIAOD_2018":
    masses = ['50to100', '100to200', '200to300','300to500','500to700','700to1000','1000to1500','1500to2000','2000toInf']
    preSearchString="/QCD_HTREPLACEME_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM"
    prefilename = "QCD_HTREPLACEME_TuneCP5_PSWeights_13TeV-RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1"
    prefix = "root://cmsxrootd.fnal.gov/"
    topFolder = "QCD_HTBinned_TuneCP5_PSWeights_13TeV-RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1"

elif Sample == 'DYJetsToLL2018':
    masses=["4to50_HT-100to200",'50']
    preSearchString="/DYJetsToLL_M-REPLACEME_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"
    prefix="root://xrootd.unl.edu/"
    prefilename="DYJetsToLL_M-REPLACEME_2018"
    topFolder=prefilename.replace

else:
    print "Please Specify Sample Name!"
    sys.exit()

    

