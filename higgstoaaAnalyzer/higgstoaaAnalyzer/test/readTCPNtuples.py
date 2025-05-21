import ROOT

ROOT.gInterpreter.Declare('#include "../interface/JetInfoDS.h"')

inputFile = 'TCPNtuple.root'


stdjets = ROOT.JetInfoDS()
reclusteredjets = ROOT.JetInfoDS()
fchain = ROOT.TChain('tcpNtuples/analysisTree')
fchain.Add(inputFile)

fchain.SetBranchAddress("StdJets", ROOT.AddressOf(stdjets))
fchain.SetBranchAddress("ReclusteredJets", ROOT.AddressOf(reclusteredjets)) 
print(fchain.GetEntries())

for iev in range(fchain.GetEntries()): # Be careful!!!
    fchain.GetEntry(iev)
    if reclusteredjets.size()>0:
        print(iev, reclusteredjets.at(0).pt) 
    if stdjets.size()>0:
        print(iev, stdjets.at(0).pt)
