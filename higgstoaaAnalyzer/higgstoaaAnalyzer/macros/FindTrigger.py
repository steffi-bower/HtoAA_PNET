import ROOT
import sys
import subprocess
import string,math,os
import ConfigParser
import glob
import numpy as np
from DataFormats.FWLite import Events, Handle
triggerString = sys.argv [1]

inFile = "root://cmseos.fnal.gov//eos/uscms/store/user/nbower/Events/2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD/FULL_HT/SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_2.root"
f=ROOT.TFile.Open(inFile)

if not f.IsZombie():
    events=Events(inFile)
else:
    print "Can't Open File: "+inFile
    exit()
handleHLT = Handle ('edm::TriggerResults')
labelHLT = ('TriggerResults','','HLT')

for event in events:
    event.getByLabel(labelHLT, handleHLT)
    triggerResults=handleHLT.product()
    names = event.object().triggerNames(triggerResults)
    for itrig in range(len(names)):
        trigger = names.triggerName(itrig)
        if triggerString=="":
            print (trigger)
        elif triggerString in trigger:
            print (trigger)
    break