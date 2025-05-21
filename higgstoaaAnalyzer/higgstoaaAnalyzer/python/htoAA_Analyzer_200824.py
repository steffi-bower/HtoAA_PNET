import ROOT,sys,os
from array import array
import numpy as np
from EventSelection_PNet_ScaleFactors import *
from ParticleSelection_PNet import *
import MyArgs

#from Cuts_2018 import *
####create the dataspace from the ntuples for our various objects. These throw errors because i believe this method of declaration is a bit outdated, but it works fine

ROOT.gInterpreter.Declare('#include "../interface/JetInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/MuonInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/ElectronInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/TauInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/GenParticleInfoDS.h"')

location = os.getcwd() 
MyArgs.init()






if test:
    inputFileList = ["file:/eos/uscms/store/user/nbower/Events/2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_Skimmed/FULL_HT/2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_Skimmed_7.root", "file:/eos/uscms/store/user/nbower/Events/2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_Skimmed/FULL_HT/2018_SUSYGluGluToHToAA_AToBB_AToTauTau_M-12_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8_MINIAOD_Skimmed_1.root"]
else:
    query = "ls *.root"
    infiles=os.popen(query).read().split()
    inputFileList=[]

    for line in infiles:
        inputFileList.append("file:"+location+"/"+line)
        print ("file:"+location+"/"+line)
out=ROOT.TFile.Open("Outfile.root",'recreate')

channels = ["tauE_tauMu","tauHad_tauMu","tauHad_tauE"]
variables= [
    ["b1_ID_Total","b1 Total ID Value",[50,0,1]],
    ["b1_PNetID","b1 PNet ID Value",[50,0,1]],
    ["Mvis","Mvis",[20,0,20]],
    ["bMass","bMass",[20,0,20]],

    ["lep1Pt","lep1 Pt (GeV)",[25,0,75]],
    ["lep2Pt","lep2 Pt (GeV)",[25,0,75]],
    ["lepDr","DeltaR (leptons)",[20,0,1.5]],
    ["lep1DRB","DeltaR (bL1)",[20,0,4]],
    ["lep2DRB","DeltaR (bL2)",[20,0,4]],
    ["MET","MET (GeV)",[10,0,100]],
    ["NLep1s","NLep1s",[5,0,5]],
    ["NLep2s","NLep2s",[5,0,5]],
    ["NLep2s","NLep2s",[5,0,5]],
    ["eleIso","eleIso",[5,0,5]],
    ["muIso","muIso",[20,0,5]],
    
    ]

ptbins=[0,10, 20, 35, 50, 65, 80, 106, 141, 186, 247, 326, 432]

Channel_HistDict={}
for channel in channels:
    leps = channel.split("_")
    for variable in variables:
            title = variable[1].replace("REPLACEME1",leps[0])
            title=title.replace("REPLACEME2",leps[1])
            Channel_HistDict["h_"+channel+"_"+variable[0]+"_isBPH"]=ROOT.TH1F("h_"+channel+"_"+variable[0]+"_isBPH", title,variable[2][0],variable[2][1],variable[2][2])
            Channel_HistDict["h_"+channel+"_"+variable[0]+"_isBPH"].Sumw2()
    Channel_HistDict["h_"+channel+"_mergedLepPt_isBPH"]=ROOT.TH1F("h_"+channel+"_mergedLepPt_isBPH", "Reco TauPT " + leps[0]+ leps[1] ,12,array('f',ptbins))
    Channel_HistDict["h_"+channel+"_mergedBPt_isBPH"]=ROOT.TH1F("h_"+channel+"_mergedBPt_isBPH", "Reco BPT " + leps[0]+ leps[1] ,12,array('f',ptbins))
    Channel_HistDict["h_"+channel+"_mergedLepPt_isBPH"].Sumw2()
    Channel_HistDict["h_"+channel+"_mergedBPt_isBPH"].Sumw2()
EventSelection_HistDict={}
for channel in channels:
    
    EventSelection_HistDict["h_"+channel+"_isBPH_EventSelection"]=ROOT.TH1F("h_"+channel+"_isBPH_EventSelection","",3,0,3)
    EventSelection_HistDict["h_"+channel+"_isBPH_EventSelection"]
    EventSelection_HistDict["h_"+channel+"_isBPH_EventSelection"].Sumw2()
ParticleSelection_HistDict={}
ParticleSelection_HistDict["h_std_electron_selection"]=ROOT.TH1F("h_std_electron_selection", "StdElectron Cuts", 3,0,3)
ParticleSelection_HistDict['h_muon_selection']=ROOT.TH1F("h_muon_selection", "Muon Cuts", 3,0,3)
ParticleSelection_HistDict['h_eCtau_selection']=ROOT.TH1F("h_eCtau_selection", "e Clean Tau Cuts", 3,0,3)
ParticleSelection_HistDict['h_muCtau_selection']=ROOT.TH1F("h_muCtau_selection", "Mu Clean Tau Cuts", 3,0,3)
ParticleSelection_HistDict['h_bJet_selection']=ROOT.TH1F("h_bJet_selection", "b Jet Cuts", 3,0,3)
ParticleSelection_HistDict["h_jetSelection"]=ROOT.TH1F("h_jetSelection", "Jet Selection", 4,0,4)


for key in ParticleSelection_HistDict.keys():
    ParticleSelection_HistDict[key].Sumw2()
    ParticleSelection_HistDict[key].SetCanExtend(ROOT.TH1.kAllAxes)
pi = np.pi
fchain = ROOT.TChain('tcpNtuples/analysisTree')
trigchain= ROOT.TChain('tcpTrigNtuples/triggerTree')
if isMC:

    lumichain= ROOT.TChain('lumiSummary/lumiTree')
    genchain = ROOT.TChain('tcpGenNtuples/genTree')

for inputFileName in inputFileList:
    inputFileName=inputFileName.replace("\n","")

    fchain.Add(inputFileName)
    trigchain.Add(inputFileName)
    if isMC:

        lumichain.Add(inputFileName)
        genchain.Add(inputFileName)

fchain.AddFriend(trigchain)
if isMC:

    fchain.AddFriend(lumichain)
    fchain.AddFriend(genchain)
jets = ROOT.JetInfoDS()
muons = ROOT.MuonInfoDS()
electrons = ROOT.ElectronInfoDS()
muCtaus = ROOT.TauInfoDS()
eCtaus = ROOT.TauInfoDS()

if isMC:
    genParticles = ROOT.GenParticleInfoDS()
diTau_Hists={
    "h_ditauID":ROOT.TH1F("h_ditauID", "diTauID", 25,0,1),
    "h_NdiTau":ROOT.TH1F("h_NdiTau", "nDiTaus", 5,0, 5),
    "h_taupt":ROOT.TH1F("h_taupt", "DiTau PT", 25,0,75),
    "h_tauCharge":ROOT.TH1F("h_tauCharge", "DiTau charge", 4,-2,2),

    "h_diTau_b1_PNetID":ROOT.TH1F("h_diTau_b1_PNetID", "DiTauPNetID", 25,0,1),
    "h_diTau_Mvis":ROOT.TH1F("h_diTau_Mvis", "DiTau Mass", 20,0,20),
    "h_diTau_bMass":ROOT.TH1F("h_diTau_bMass", "diTau BMass", 20,0,20),
    "h_diTau_tauDRB":ROOT.TH1F("h_diTau_tauDRB", "di Tau Dr(tau,b)", 20,0,4),
    "h_diTau_MET":ROOT.TH1F("h_diTau_MET", "DiTau MET", 10,0,100),
    "h_diTau_NEles":ROOT.TH1F("h_diTau_NEles", "nEle in DiTau", 5,0,5),
    "h_diTau_NMus":ROOT.TH1F("h_diTau_NMus", "nMu DiTau", 5,0,5)
}
DiTauSelection = ROOT.TH1F("DiTauSelection", "DiTauSelection", 3,0,3)
DiTauSelection.Sumw2()
DiTauSelection.SetCanExtend(ROOT.TH1.kAllAxes)
for key in diTau_Hists.keys():
    diTau_Hists[key].Sumw2()



histos={}
histos["h_nEvents"]=ROOT.TH1F("h_nEvents", "nEvents", 4,0,4)
histos["h_pdgid"]=ROOT.TH1F("h_pdgid", "h_pdgid", 30,0,30)
histos["h_genBsteptoNull"]=ROOT.TH1F("h_genBsteptoNull", "b N steps to Null", 15,0,15)
histos["h_genBmomBeforeNull"]=ROOT.TH1F("h_genBmomBeforeNull", "b last mother", 15,0,15)
histos["h_pdgidbs"]=ROOT.TH1F("h_pdgidbs", "h_pdgidbs", 200,400,600)


histos["h_triggerMu_dBSig"]=ROOT.TH1F("h_triggerMu_dBSig", "Trigger Mu dBSig", 20,0,20)
histos["h_triggerMu_pT"]=ROOT.TH1F("h_triggerMu_pT", "Trigger Mu pT", 25,1,51)
histos["h_Mu_dBSig"]=ROOT.TH1F("h_Mu_dBSig", "Trigger Mu dBSig", 20,0,20)


histos["h_nBs"]=ROOT.TH1F("h_nBs", "number of selected Bjets per event", 4,0,4)
histos["h_nBs_matched"]=ROOT.TH1F("h_nBs_matched", "number of matched Bjets per event", 4,0,4)

histos["h_b_DR_AllMu"]=ROOT.TH1F("h_b_DR_AllMu", "b DR allMu", 20,0,4)
histos["h_nOffline_Trigmu"]=ROOT.TH1F("h_nOffline_Trigmu", "number of Offline trigger muons", 5,0,5)
histos['h_DeepFlav']=ROOT.TH1F("h_DeepFlav", "DeepFlavScores (All Jets) ", 1000,0,1)
histos['h_pNetFull']=ROOT.TH1F("h_pNetFull", "PNetScores (All Jets)", 20,0,1)

histos['h_ditau2017v1_DiTauMatch']=ROOT.TH1F("h_ditau2017v1_DiTauMatch", " DeepDiTau V1 (DiTauMatch)", 50000,0,1)
histos['h_ditau2017MDv1_DiTauMatch']=ROOT.TH1F("h_ditau2017MDv1_DiTauMatch", "DeepDiTau MD V1 (DiTauMatch)", 50000,0,1)
histos['h_ditau2017v2_DiTauMatch']=ROOT.TH1F("h_ditau2017v2_DiTauMatch", "DeepDiTau V2 (DiTauMatch)", 50000,0,1)
histos['h_ditau2017MDv2_DiTauMatch']=ROOT.TH1F("h_ditau2017MDv2_DiTauMatch", "DeepDiTau MDV2 (DiTauMatch)", 50000,0,1)

histos['h_ditau2017v1']=ROOT.TH1F("h_ditau2017v1", " DeepDiTau V1 (All Jets)", 50000,0,1)
histos['h_ditau2017MDv1']=ROOT.TH1F("h_ditau2017MDv1", "DeepDiTau MD V1 (All Jets)", 50000,0,1)
histos['h_ditau2017v2']=ROOT.TH1F("h_ditau2017v2", "DeepDiTau V2 (All Jets)", 50000,0,1)
histos['h_ditau2017MDv2']=ROOT.TH1F("h_ditau2017MDv2", "DeepDiTau MDV2 (All Jets)", 50000,0,1)

histos['h_ditau2017v1_Unmatched']=ROOT.TH1F("h_ditau2017v1_Unmatched", " DeepDiTau V1 (Unmatched)", 50000,0,1)
histos['h_ditau2017MDv1_Unmatched']=ROOT.TH1F("h_ditau2017MDv1_Unmatched", "DeepDiTau MD V1 (Unmatched)", 50000,0,1)
histos['h_ditau2017v2_Unmatched']=ROOT.TH1F("h_ditau2017v2_Unmatched", "DeepDiTau V2 (Unmatched)", 50000,0,1)
histos['h_ditau2017MDv2_Unmatched']=ROOT.TH1F("h_ditau2017MDv2_Unmatched", "DeepDiTau MDV2 (Unmatched)", 50000,0,1)

histos['h_ditau2017v1_MonoTauMatch']=ROOT.TH1F("h_ditau2017v1_MonoTauMatch", " DeepDiTau V1 (MonoTauMatch)", 50000,0,1)
histos['h_ditau2017MDv1_MonoTauMatch']=ROOT.TH1F("h_ditau2017MDv1_MonoTauMatch", "DeepDiTau MD V1 (MonoTauMatch)", 50000,0,1)
histos['h_ditau2017v2_MonoTauMatch']=ROOT.TH1F("h_ditau2017v2_MonoTauMatch", "DeepDiTau V2 (MonoTauMatch)", 50000,0,1)
histos['h_ditau2017MDv2_MonoTauMatch']=ROOT.TH1F("h_ditau2017MDv2_MonoTauMatch", "DeepDiTau MDV2 (MonoTauMatch)", 50000,0,1)

histos['h_pNetvditau2017v1_Full']=ROOT.TH2F("h_pNetvditau2017v1_Full", " PNet Vs ditau2017v1 (All Jets)", 20,0,1,20,0,1)
histos['h_pNetvditau2017MDv1_Full']=ROOT.TH2F("h_pNetvditau2017MDv1_Full", " PNet Vs ditau2017MDv1 (All Jets)", 20,0,1,20,0,1)
histos['h_pNetvditau2017v2_Full']=ROOT.TH2F("h_pNetvditau2017v2_Full", " PNet Vs ditau2017v2 (All Jets)", 20,0,1,20,0,1)
histos['h_pNetvditau2017MDv2_Full']=ROOT.TH2F("h_pNetvditau2017MDv2_Full", " PNet Vs ditau2017MDv2 (All Jets)", 20,0,1,20,0,1)


histos['h_pNetvDeepFlav_Full']=ROOT.TH2F("h_pNetvDeepFlav_Full", " PNet Vs DeepFlav (All Jets)", 20,0,1,20,0,1)
histos['h_pNetvbmass']=ROOT.TH2F("h_pNetvbmass", " PNet Vs bmass", 20,0,1,20,0,20)

histos['h_pNetMerged_pt_WP80']=ROOT.TH1F("h_pNetMerged_pt_WP80", "PnetTPR=80% PT (Merged Bs)", 12,array('f',ptbins))
histos['h_deepFlavmerged_pt_WP80']=ROOT.TH1F("h_deepFlavmerged_pt_WP80", "DeepFlavTPR=80% PT (Merged Bs)", 12,array('f',ptbins))
histos['h_pNetMerged_pt_WP85']=ROOT.TH1F("h_pNetMerged_pt_WP85", "PnetTPR=85% PT (Merged Bs)", 12,array('f',ptbins))
histos['h_deepFlavmerged_pt_WP85']=ROOT.TH1F("h_deepFlavmerged_pt_WP85", "DeepFlavTPR=85% PT (Merged Bs)", 12,array('f',ptbins))
histos['h_pNetMerged_pt_WP90']=ROOT.TH1F("h_pNetMerged_pt_WP90", "PnetTPR=90% PT (Merged Bs)", 12,array('f',ptbins))
histos['h_deepFlavmerged_pt_WP90']=ROOT.TH1F("h_deepFlavmerged_pt_WP90", "DeepFlavTPR=90% PT (Merged Bs)", 12,array('f',ptbins))
histos['h_Merged_pt']=ROOT.TH1F("h_Merged_pt", "PT (Merged Bs)", 12,array('f',ptbins))


histos['h_pNetMerged_10to40']=ROOT.TH1F("h_pNetMerged_10to40", "PNetScores10to40 (Merged Bs)", 50000,0,1)
histos['h_pNetMerged_40to100']=ROOT.TH1F("h_pNetMerged_40to100", "PNetScores (Merged Bs)", 50000,0,1)
histos['h_pNetMerged_100plus']=ROOT.TH1F("h_pNetMerged_100plus", "PNetScores (Merged Bs)", 50000,0,1)
histos['h_DeepFlavMerged_10to40']=ROOT.TH1F("h_DeepFlavMerged_10to40", "DeepFlavScores _10to40(Merged Bs)", 50000,0,1)
histos['h_DeepFlavMerged_40to100']=ROOT.TH1F("h_DeepFlavMerged_40to100", "DeepFlavScores (Merged Bs)", 50000,0,1)
histos['h_DeepFlavMerged_100plus']=ROOT.TH1F("h_DeepFlavMerged_100plus", "DeepFlavScores (Merged Bs)", 50000,0,1)

histos['h_DeepFlav_bb_Merged_10to40']=ROOT.TH1F("h_DeepFlav_bb_Merged_10to40", "DeepFlavScores _10to40(Merged Bs)", 50000,0,1)
histos['h_DeepFlav_bb_Merged_40to100']=ROOT.TH1F("h_DeepFlav_bb_Merged_40to100", "DeepFlavScores (Merged Bs)", 50000,0,1)
histos['h_DeepFlav_bb_Merged_100plus']=ROOT.TH1F("h_DeepFlav_bb_Merged_100plus", "DeepFlavScores (Merged Bs)", 50000,0,1)

histos['h_pNetFake_10to40']=ROOT.TH1F("h_pNetFake_10to40", "PNetScores _10to40(Fake)", 50000,0,1)
histos['h_DeepFlavFake_10to40']=ROOT.TH1F("h_DeepFlavFake_10to40", "DeepFlavScores _10to40(Fake)", 50000,0,1)
histos['h_DeepFlav_bb_Fake_10to40']=ROOT.TH1F("h_DeepFlav_bb_Fake_10to40", "DeepFlavScores _10to40(Fake)", 50000,0,1)
histos['h_pNetFake_40to100']=ROOT.TH1F("h_pNetFake_40to100", "PNetScores _40to100(Fake)", 50000,0,1)
histos['h_DeepFlavFake_40to100']=ROOT.TH1F("h_DeepFlavFake_40to100", "DeepFlavScores _40to100(Fake)", 50000,0,1)
histos['h_DeepFlav_bb_Fake_40to100']=ROOT.TH1F("h_DeepFlav_bb_Fake_40to100", "DeepFlavScores _40to100(Fake)", 50000,0,1)
histos['h_pNetFake_100plus']=ROOT.TH1F("h_pNetFake_100plus", "PNetScores _100plus(Fake)", 50000,0,1)
histos['h_DeepFlavFake_100plus']=ROOT.TH1F("h_DeepFlavFake_100plus", "DeepFlavScores _100plus(Fake)", 50000,0,1)
histos['h_DeepFlav_bb_Fake_100plus']=ROOT.TH1F("h_DeepFlav_bb_Fake_100plus", "DeepFlavScores _100plus(Fake)", 50000,0,1)

histos['h_pNetvDeepFlav_Merged']=ROOT.TH2F("h_pNetvDeepFlav_Merged", " PNet Vs DeepFlav (Merged Bs)", 20,0,1,20,0,1)

for key in histos.keys():
    histos[key].Sumw2()

fchain.SetBranchAddress("StdJets", ROOT.AddressOf(jets))
fchain.SetBranchAddress("TausMCleaned", ROOT.AddressOf(muCtaus))
fchain.SetBranchAddress("TausECleaned", ROOT.AddressOf(eCtaus))
fchain.SetBranchAddress("Muons", ROOT.AddressOf(muons))
fchain.SetBranchAddress("Electrons", ROOT.AddressOf(electrons))

if isMC:
    fchain.SetBranchAddress("GenParticleInfo", ROOT.AddressOf(genParticles))

for iev in range(fchain.GetEntries()): # Be careful!!!                                                                                                   
#for iev in range(10):
    fchain.GetEntry(iev)

    mets = fchain.GetBranch("Mets")
    met_pt = mets.GetLeaf('pt').GetValue()
    met_phi = mets.GetLeaf('phi').GetValue()
    if isMC:
        weight = fchain.GetBranch("lumiInfo")
        genWeight = weight.GetLeaf('weight').GetValue()
        #genWeight = 1 #for counting experiments
        trigLumiWeight=genWeight*33.7e3
        #trigLumiWeight=1
    else:
        genWeight=1
        trigLumiWeight=1

    histos['h_nEvents'].Fill(0.5, 1)
    histos['h_nEvents'].Fill(1.5, genWeight)

    passBPHTrig = bool(fchain.GetLeaf("isBPH").GetValue())
    if not passBPHTrig:continue
    histos['h_nEvents'].Fill(2.5, genWeight)

    if isMC:
        genMuFromTau=[]
        genEFromB=[]
        genEFromTau=[]
        genMuFromB=[]
        gen_taus = []

        gen_bs=[]

        for gen in genParticles:
            histos["h_pdgid"].Fill(abs(gen.pdgid),1)
            histos["h_pdgidbs"].Fill(abs(gen.pdgid),1)

            if abs(gen.pdgid)==13 and gen.isFromB:
                genMuFromB.append(gen)
            elif abs(gen.pdgid)==11 and gen.isFromB:
                genEFromB.append(gen)
            elif abs(gen.pdgid)==11 and gen.isDirectHardProcessTauDecayProductFinalState:
                genEFromTau.append(gen)
            elif abs(gen.pdgid)==13 and gen.isDirectHardProcessTauDecayProductFinalState:
                genMuFromTau.append(gen)
            elif abs(gen.pdgid)==5 and gen.isHardProcess:
                gen_bs+=[gen]
                histos["h_genBsteptoNull"].Fill(gen.stepToNull,genWeight)
                histos["h_genBmomBeforeNull"].Fill(gen.nullMom,genWeight)
            elif (abs(gen.pdgid)==15 and gen.isHardProcess):
                gen_taus+=[gen]
            elif gen.pdgid==-16 and gen.isDirectHardProcessTauDecayProductFinalState:
                gen_tauNuBar=gen
            elif gen.pdgid==16 and gen.isDirectHardProcessTauDecayProductFinalState:
                gen_tauNu=gen
########BPHTrigger Muons Mu Sorting######
        iBPHMuons=[]



        b_locks = []
        b_fakes= []
        unmatched_Bs=[]
        merged_Bs=[]
        muMatched_Jets=[]
        #######GEN Tau Sorting 
        preselected_jets=[]
        matchedDiTaus=[]
        if jets.size()>0:
            for i in range(jets.size()):
                ParticleSelection_HistDict["h_jetSelection"].Fill("N j NTuple",1)
                jet = jets.at(i)
                bidVal= jet.flavorprobb+jet.flavorprobbb+jet.flavorproblepb

                #if jet.pt>10 and jet.pt<432 and jet.genJet==1 and abs(jet.eta)<2.4 and jet.puid>=1 and jet.id >= 1:### I removed the bidBal preslection
                if jet.pt>10 and jet.pt<432  and abs(jet.eta)<2.4 and jet.puid>=1 and jet.id >= 1:### I removed the bidBal preslection
                    preselected_jets+=[jet]
                    ParticleSelection_HistDict["h_jetSelection"].Fill("Kinematics",1)

                    #if jet.pnet_score<BIDCut: continue
                    #if jet.pnet_score>BIDCut: continue
                    #if bidVal<BIDCut: continue
                    j=ROOT.TLorentzVector()
                    j.SetPtEtaPhiM(jet.pt,jet.eta,jet.phi,jet.mass)
                    BdeltaRMin=9999
                    matchedbGen=-1
                    #minDRMuon=.4
                    merged=False
                    histos['h_ditau2017v1'].Fill(jet.ditau2017v1,genWeight)
                    histos['h_ditau2017MDv1'].Fill(jet.ditau2017MDv1,genWeight)
                    histos['h_ditau2017v2'].Fill(jet.ditau2017v2,genWeight)
                    histos['h_ditau2017MDv2'].Fill(jet.ditau2017MDv2,genWeight)

                    histos['h_pNetvditau2017v1_Full'].Fill(jet.pnet_score,jet.ditau2017v1,genWeight)
                    histos['h_pNetvditau2017MDv1_Full'].Fill(jet.pnet_score,jet.ditau2017MDv1,genWeight)
                    histos['h_pNetvditau2017v2_Full'].Fill(jet.pnet_score,jet.ditau2017v2,genWeight)
                    histos['h_pNetvditau2017MDv2_Full'].Fill(jet.pnet_score,jet.ditau2017MDv2,genWeight)
                    unmatched = True
                    if len(gen_taus)>1 and len(genEFromTau)==0 and len(genMuFromTau)==0:
                        t1=ROOT.TLorentzVector()
                        t1.SetPtEtaPhiM(gen_taus[0].pt,gen_taus[0].eta,gen_taus[0].phi,gen_taus[0].mass)
                        t2=ROOT.TLorentzVector()
                        t2.SetPtEtaPhiM(gen_taus[1].pt,gen_taus[1].eta,gen_taus[1].phi,gen_taus[1].mass)
                        nu1=ROOT.TLorentzVector()
                        nu1.SetPtEtaPhiM(gen_tauNuBar.pt,gen_tauNuBar.eta,gen_tauNuBar.phi,gen_tauNuBar.mass)
                        nu2=ROOT.TLorentzVector()
                        nu2.SetPtEtaPhiM(gen_tauNu.pt,gen_tauNu.eta,gen_tauNu.phi,gen_tauNu.mass)
                        ditau=t1+t2-nu1-nu2
                        if ditau.DeltaR(j)<.4:
                            histos['h_ditau2017v1_DiTauMatch'].Fill(jet.ditau2017v1,genWeight)
                            histos['h_ditau2017MDv1_DiTauMatch'].Fill(jet.ditau2017MDv1,genWeight)
                            histos['h_ditau2017v2_DiTauMatch'].Fill(jet.ditau2017v2,genWeight)
                            histos['h_ditau2017MDv2_DiTauMatch'].Fill(jet.ditau2017MDv2,genWeight)
                            matchedDiTaus+=[jet]
                            ParticleSelection_HistDict["h_jetSelection"].Fill("Matched DiTaus",1)

                            unmatched=False
                    elif len(gen_taus)>0 and len(genEFromTau)==1 and len(genMuFromTau)==0:
                        for tau in gen_taus:
                            if tau.pdgid>0 and genEFromTau[0].pdgid<0:
                                t1=ROOT.TLorentzVector()
                                t1.SetPtEtaPhiM(tau.pt,tau.eta,tau.phi,tau.mass)
                                nu=ROOT.TLorentzVector()
                                nu.SetPtEtaPhiM(gen_tauNuBar.pt,gen_tauNuBar.eta,gen_tauNuBar.phi,gen_tauNuBar.mass)
                                gentauhad=t1-nu
                                if gentauhad.DeltaR(j)<.4:
                                    histos['h_ditau2017v1_MonoTauMatch'].Fill(jet.ditau2017v1,genWeight)
                                    histos['h_ditau2017MDv1_MonoTauMatch'].Fill(jet.ditau2017MDv1,genWeight)
                                    histos['h_ditau2017v2_MonoTauMatch'].Fill(jet.ditau2017v2,genWeight)
                                    histos['h_ditau2017MDv2_MonoTauMatch'].Fill(jet.ditau2017MDv2,genWeight)
                            if tau.pdgid<0 and genEFromTau[0].pdgid>0:
                                t1=ROOT.TLorentzVector()
                                t1.SetPtEtaPhiM(tau.pt,tau.eta,tau.phi,tau.mass)
                                nu=ROOT.TLorentzVector()
                                nu.SetPtEtaPhiM(gen_tauNu.pt,gen_tauNu.eta,gen_tauNu.phi,gen_tauNu.mass)
                                gentauhad=t1-nu
                                if gentauhad.DeltaR(j)<.4:
                                    histos['h_ditau2017v1_MonoTauMatch'].Fill(jet.ditau2017v1,genWeight)
                                    histos['h_ditau2017MDv1_MonoTauMatch'].Fill(jet.ditau2017MDv1,genWeight)
                                    histos['h_ditau2017v2_MonoTauMatch'].Fill(jet.ditau2017v2,genWeight)
                                    histos['h_ditau2017MDv2_MonoTauMatch'].Fill(jet.ditau2017MDv2,genWeight)
                                    unmatched=False
                    elif len(gen_taus)>0 and len(genEFromTau)==0 and len(genMuFromTau)==1:
                        for tau in gen_taus:
                            if tau.pdgid>0 and genMuFromTau[0].pdgid<0:
                                t1=ROOT.TLorentzVector()
                                t1.SetPtEtaPhiM(tau.pt,tau.eta,tau.phi,tau.mass)
                                nu=ROOT.TLorentzVector()
                                nu.SetPtEtaPhiM(gen_tauNuBar.pt,gen_tauNuBar.eta,gen_tauNuBar.phi,gen_tauNuBar.mass)
                                gentauhad=t1-nu
                                if gentauhad.DeltaR(j)<.4:
                                    histos['h_ditau2017v1_MonoTauMatch'].Fill(jet.ditau2017v1,genWeight)
                                    histos['h_ditau2017MDv1_MonoTauMatch'].Fill(jet.ditau2017MDv1,genWeight)
                                    histos['h_ditau2017v2_MonoTauMatch'].Fill(jet.ditau2017v2,genWeight)
                                    histos['h_ditau2017MDv2_MonoTauMatch'].Fill(jet.ditau2017MDv2,genWeight)
                            if tau.pdgid<0 and genMuFromTau[0].pdgid>0:
                                t1=ROOT.TLorentzVector()
                                t1.SetPtEtaPhiM(tau.pt,tau.eta,tau.phi,tau.mass)
                                nu=ROOT.TLorentzVector()
                                nu.SetPtEtaPhiM(gen_tauNu.pt,gen_tauNu.eta,gen_tauNu.phi,gen_tauNu.mass)
                                gentauhad=t1-nu
                                if gentauhad.DeltaR(j)<.4:
                                    histos['h_ditau2017v1_MonoTauMatch'].Fill(jet.ditau2017v1,genWeight)
                                    histos['h_ditau2017MDv1_MonoTauMatch'].Fill(jet.ditau2017MDv1,genWeight)
                                    histos['h_ditau2017v2_MonoTauMatch'].Fill(jet.ditau2017v2,genWeight)
                                    histos['h_ditau2017MDv2_MonoTauMatch'].Fill(jet.ditau2017MDv2,genWeight)
                                    unmatched=False
                    if unmatched==True:
                        histos['h_ditau2017v1_Unmatched'].Fill(jet.ditau2017v1,genWeight)
                        histos['h_ditau2017MDv1_Unmatched'].Fill(jet.ditau2017MDv1,genWeight)
                        histos['h_ditau2017v2_Unmatched'].Fill(jet.ditau2017v2,genWeight)
                        histos['h_ditau2017MDv2_Unmatched'].Fill(jet.ditau2017MDv2,genWeight)

                    for igen in range(len(gen_bs)):
                        gb=ROOT.TLorentzVector()
                        gb.SetPtEtaPhiM(gen_bs[igen].pt,gen_bs[igen].eta,gen_bs[igen].phi,gen_bs[igen].mass)
                        if matchedbGen != -1 and gb.DeltaR(j)<.4:
                            merged=True
                            ParticleSelection_HistDict["h_jetSelection"].Fill("Merged b == True",1)

                        if gb.DeltaR(j)<BdeltaRMin:
                            BdeltaRMin=gb.DeltaR(j)
                            if igen not in b_locks and gb.DeltaR(j)<.4:
                                matchedbGen=igen
                                ParticleSelection_HistDict["h_jetSelection"].Fill("matched b == True",1)


                    if matchedbGen != -1 and merged== True:
                        b_locks+=[matchedbGen]
                        merged_Bs+=[jet]
                    else:
                        b_fakes+=[jet]
                    
                    if jet.pnet_score<BIDCut and not reversedBID: 
                        ParticleSelection_HistDict["h_jetSelection"].Fill("BID FAIL ",1)

                        continue
                    if (jet.pnet_score>BIDCut or bidVal<.0495) and reversedBID: 
                        ParticleSelection_HistDict["h_jetSelection"].Fill("Reversed BID FAIL ",1)

                        continue

                    unmatched_Bs+=[jet]
        selected_DiTau=[]
        histos["h_nBs"].Fill(len(unmatched_Bs),1)
        histos["h_nBs_matched"].Fill(len(merged_Bs),1)
        for j in preselected_jets:
            histos["h_DeepFlav"].Fill(j.flavorprobb+j.flavorprobbb+j.flavorproblepb,genWeight)
            histos["h_pNetFull"].Fill(j.pnet_score,genWeight)
            histos['h_pNetvDeepFlav_Full'].Fill(j.pnet_score,j.flavorprobb+j.flavorprobbb+j.flavorproblepb,genWeight)
            histos['h_pNetvbmass'].Fill(j.pnet_score,j.mass,genWeight)
            for b in unmatched_Bs:
                    bt=ROOT.TLorentzVector()
                    bt.SetPtEtaPhiM(b.pt,b.eta,b.phi,b.mass)
                    jt=ROOT.TLorentzVector()
                    jt.SetPtEtaPhiM(j.pt,j.eta,j.phi,j.mass)
                    if jt.DeltaR(bt)>.5:
                        if j.ditau2017v1>.6:
                            selected_DiTau+=[j]

        for jet in merged_Bs:
            histos["h_Merged_pt"].Fill(jet.pt,genWeight)
            if jet.flavorprobbb>.0085:
                histos["h_deepFlavmerged_pt_WP80"].Fill(jet.pt,genWeight)
            if jet.flavorprobbb>.0075:
                histos["h_deepFlavmerged_pt_WP85"].Fill(jet.pt,genWeight)
            if jet.flavorprobbb>.0065:
                histos["h_deepFlavmerged_pt_WP90"].Fill(jet.pt,genWeight)

            if jet.pnet_score>.733:
                histos["h_pNetMerged_pt_WP80"].Fill(jet.pt,genWeight)
            if jet.pnet_score>.605:
                histos["h_pNetMerged_pt_WP85"].Fill(jet.pt,genWeight)
            if jet.pnet_score>.408:
                histos["h_pNetMerged_pt_WP90"].Fill(jet.pt,genWeight)


            if jet.pt<40:
                histos["h_DeepFlav_bb_Merged_10to40"].Fill(jet.flavorprobbb, genWeight)
                histos["h_DeepFlavMerged_10to40"].Fill(jet.flavorprobb+jet.flavorprobbb+jet.flavorproblepb, genWeight)
                histos["h_pNetMerged_10to40"].Fill(jet.pnet_score, genWeight)
            elif jet.pt<100:
                histos["h_DeepFlav_bb_Merged_40to100"].Fill(jet.flavorprobbb, genWeight)
                histos["h_DeepFlavMerged_40to100"].Fill(jet.flavorprobb+jet.flavorprobbb+jet.flavorproblepb, genWeight)
                histos["h_pNetMerged_40to100"].Fill(jet.pnet_score, genWeight)
            else:
                histos["h_DeepFlav_bb_Merged_100plus"].Fill(jet.flavorprobbb, genWeight)
                histos["h_DeepFlavMerged_100plus"].Fill(jet.flavorprobb+jet.flavorprobbb+jet.flavorproblepb, genWeight)
                histos["h_pNetMerged_100plus"].Fill(jet.pnet_score, genWeight)
        for jet in preselected_jets:
            if jet.pt<40:

                histos["h_DeepFlav_bb_Fake_10to40"].Fill(jet.flavorprobbb, genWeight)
                histos["h_DeepFlavFake_10to40"].Fill(jet.flavorprobb+jet.flavorprobbb+jet.flavorproblepb, genWeight)
                histos["h_pNetFake_10to40"].Fill(jet.pnet_score, genWeight)
            elif jet.pt<100:

                histos["h_DeepFlav_bb_Fake_40to100"].Fill(jet.flavorprobbb, genWeight)
                histos["h_DeepFlavFake_40to100"].Fill(jet.flavorprobb+jet.flavorprobbb+jet.flavorproblepb, genWeight)
                histos["h_pNetFake_40to100"].Fill(jet.pnet_score, genWeight)
            else:

                histos["h_DeepFlav_bb_Fake_100plus"].Fill(jet.flavorprobbb, genWeight)
                histos["h_DeepFlavFake_100plus"].Fill(jet.flavorprobb+jet.flavorprobbb+jet.flavorproblepb, genWeight)
                histos["h_pNetFake_100plus"].Fill(jet.pnet_score, genWeight)
        s_muons, bTriggerMus, doubleTrigger_Mus, isoTrigger_Mus, offlineBTrigMus = MuonSelection(muons,ParticleSelection_HistDict['h_muon_selection'],unmatched_Bs,genWeight)

    else:
        unmatched_Bs=[]
        preselected_jets=[]
        if jets.size()>0:
            for i in range(jets.size()):
                ParticleSelection_HistDict["h_jetSelection"].Fill("Input Jets",1)
                jet = jets.at(i)
                bidVal= jet.flavorprobb+jet.flavorprobbb+jet.flavorproblepb

                if jet.pt>10 and jet.pt<432:
                    ParticleSelection_HistDict["h_jetSelection"].Fill("10GeV<pT<432GeV",1)
                    if abs(jet.eta)<2.4:
                        ParticleSelection_HistDict["h_jetSelection"].Fill("|eta|<2.4",1)
                        if jet.puid>=1: 
                            ParticleSelection_HistDict["h_jetSelection"].Fill("LoosePUID",1)
                            if jet.id >= 1:
                                preselected_jets+=[jet]
                                ParticleSelection_HistDict["h_jetSelection"].Fill("Loose ID",1)
                                #if jet.pnet_score<BIDCut: continue
                                #if bidVal>BIDCut: continue                    
                                if jet.pnet_score<BIDCut and not reversedBID: 
                                    ParticleSelection_HistDict["h_jetSelection"].Fill("BID FAIL ",1)

                                    continue
                                if (jet.pnet_score>BIDCut or bidVal<.0495) and reversedBID: 
                                    ParticleSelection_HistDict["h_jetSelection"].Fill("Reversed BID FAIL ",1)

                                    continue
                                unmatched_Bs+=[jet]
        s_muons, bTriggerMus, doubleTrigger_Mus, isoTrigger_Mus, offlineBTrigMus = MuonSelection(muons,ParticleSelection_HistDict['h_muon_selection'],unmatched_Bs,genWeight)

 
    s_muons.sort(key=lambda x: x.pt, reverse=True)
    bTriggerMus.sort(key=lambda x: x.pt, reverse=True)
    doubleTrigger_Mus.sort(key=lambda x: x.pt, reverse=True)
    isoTrigger_Mus.sort(key=lambda x: x.pt, reverse=True)
    offlineBTrigMus.sort(key=lambda x: x.pt, reverse=True)
    histos["h_nOffline_Trigmu"].Fill(len(offlineBTrigMus),genWeight)
    s_electrons = ElectronSelection(ParticleSelection_HistDict["h_std_electron_selection"] ,electrons,genWeight)
    s_electrons.sort(key=lambda x: x.pt, reverse=True)
    s_muCtaus = MuCleanedTauHad_Selection(ParticleSelection_HistDict['h_muCtau_selection'],muCtaus,s_electrons,s_muons,unmatched_Bs, genWeight)
    s_eCtaus = EleCleanedTauHad_Selection(ParticleSelection_HistDict['h_eCtau_selection'],eCtaus,s_electrons,s_muons,unmatched_Bs,genWeight)
    
    for mu in bTriggerMus:
        histos["h_triggerMu_pT"].Fill(mu.pt,genWeight)
        if mu.edB!=0:
            histos["h_triggerMu_dBSig"].Fill(mu.dB/mu.edB,genWeight)   

    #for mu in s_muons:
    #    histos["h_Mu_pT"].Fill(mu.pt,genWeight)
    #    if mu.edB!=0:
    #        histos["h_Mu_dBSig"].Fill(mu.dB/mu.edB,genWeight)   

    s_muCtaus.sort(key=lambda x: x.pt, reverse=True)
    s_eCtaus.sort(key=lambda x: x.pt, reverse=True)
    unmatched_Bs.sort(key=lambda x: x.pt, reverse=True)
    unmatched_Bs.sort(key=lambda x: x.pt, reverse=True)
    if isMC:
        merged_Bs.sort(key=lambda x: x.pt, reverse=True)
        selected_DiTau.sort(key=lambda x: x.pt,reverse=True)
        DiTauPlotting(DiTauSelection,selected_DiTau,unmatched_Bs,diTau_Hists,trigLumiWeight,met_pt, offlineBTrigMus, s_electrons,s_muons)

        #for b in merged_Bs:
        #    histos["h_DeepFlavMerged"].Fill(b.flavorprobb+b.flavorprobbb+b.flavorproblepb,genWeight)
        #    histos["h_pNetMerged"].Fill(b.pnet_score,genWeight)
        #    histos['h_pNetvDeepFlav_Merged'].Fill(b.pnet_score,b.flavorprobb+b.flavorprobbb+b.flavorproblepb,genWeight)
    #unmatched_Bs.sort(key=lambda x: x.flavorprobb+x.flavorprobbb+x.flavorproblepb, reverse=True)
    #merged_Bs.sort(key=lambda x: x.flavorprobb+x.flavorprobbb+x.flavorproblepb, reverse=True)
    Asymmetric_Channels=[['tauE_tauMu',s_electrons,s_muons,False],['tauHad_tauE',s_eCtaus,s_electrons,True],["tauHad_tauMu",s_muCtaus,s_muons,True]]
    for channel in Asymmetric_Channels:
        Asymmetric_Lepton_Plotting(EventSelection_HistDict["h_"+channel[0]+"_isBPH_EventSelection"],channel[1],channel[2],unmatched_Bs,Channel_HistDict,trigLumiWeight,channel[0],met_pt,offlineBTrigMus,isMC)
for key in histos.keys():
    histos[key].Write()
for key in ParticleSelection_HistDict.keys():
    ParticleSelection_HistDict[key].Write()
for key in EventSelection_HistDict.keys():
    EventSelection_HistDict[key].Write()
for key in Channel_HistDict.keys():
    Channel_HistDict[key].Write()
for key in diTau_Hists.keys():
    diTau_Hists[key].Write()
DiTauSelection.Write()
out.Close()
