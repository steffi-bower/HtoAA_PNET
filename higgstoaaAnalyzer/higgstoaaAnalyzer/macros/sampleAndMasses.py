#Sample = 'QCD_MINIAOD'
#Sample = 'DYJetsToLL_94X'
#Sample = 'DYJetsToLL'
#Sample = 'DYJetsToLLNLO'
#Sample = 'TTJets'
#Sample = 'ST'
#Sample = 'Diboson'
#Sample = 'QCD_AOD'
#Sample = 'QCD_Mu'
#Sample = 'DYJetsToQQ'
#Sample = 'ZJetsToQQ'
#Sample = 'WJetsToQQ'
#Sample = 'DYJetsToLL_10-50'
#Sample="DYJetsToLL2018"
isHad = True
isCopy=True
version="vplots"
isGen=False
if Sample == 'TCP':
    masses=['m10', 'm30', 'm50']
    prefix="root://cmseos.fnal.gov//store/user/mwulansa/DIS/TCP/OutputMiniAODSIM/"
#if Sample == 'TCP':
#    masses=['m10','m50']
#    prefix="root://cmseos.fnal.gov/"

    
elif Sample == 'DYJetsToLL':
    masses=['']
    preSearchString="/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM"
    prefix="root://xrootd.unl.edu/"
    prefilename="DYJetsToLL_M-50_2017_v9"
    topFolder=prefilename
elif Sample == 'DYJetsToLL_10-50':
    masses=['']
    preSearchString="/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM"
    prefix="root://xrootd.unl.edu/"
    prefilename="DYJetsToLL_M-10To50_2017_v9"
    topFolder=prefilename

    
elif Sample == 'TTJets':
    masses=["Dilept"]
    preSearchString="/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM"
    prefix="root://xrootd.unl.edu/"
    prefilename="TTJets_2017_v9_MINIAOD"
    topFolder=prefilename




elif Sample == 'WJetsToLNu':
    masses = ['']
    preSearchString="/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM"
    prefilename="WJetsToLNu_2017_MINIAOD"
    topFolder=prefilename
    prefix = "root://xrootd.unl.edu/"
elif Sample=="WZ":
    masses = ['']
    preSearchString="/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM"
    prefilename="WZ_2017_MINIAOD"
    topFolder=prefilename
    prefix = "root://xrootd.unl.edu/"

elif Sample=="Pileup":
    masses = ['']
    preSearchString="/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW"
    prefilename="Pileup"
    topFolder=prefilename
    prefix = "root://xrootd.unl.edu/"

elif Sample == "QCD_MINIAOD":
    masses = ['50to100', '100to200', '200to300','300to500','500to700','700to1000','1000to1500','1500to2000','2000toInf']
    preSearchString="/QCD_HTREPLACEME_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM"
    prefilename = "QCD_HTREPLACEME_TuneCP5_PSWeights_13TeV-RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1"
    prefix = "root://cmsxrootd.fnal.gov/"
    topFolder = "QCD_HTBinned_TuneCP5_PSWeights_13TeV-RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1"
elif Sample == 'DYJetsToLL2018':
    masses=['']
    preSearchString="/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"
    prefix="root://xrootd.unl.edu/"
    prefilename="DYJetsToLL_M-50_2018_v9"
    topFolder=prefilename
else:
    print "Please Specify Sample Name!"
    sys.exit()

    

