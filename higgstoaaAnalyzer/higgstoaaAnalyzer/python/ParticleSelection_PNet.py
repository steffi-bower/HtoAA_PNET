import ROOT,sys,os
import numpy as np
import MyArgs
MyArgs.init()
ROOT.gInterpreter.Declare('#include "../interface/JetInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/MuonInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/ElectronInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/TauInfoDS.h"')

def MuonSelection(muons,selection_hist,bjets,genWeight):
    selected_Mus=[]
    btrigger_Mus=[]
    isoTrigger_Mus=[]
    doubleTrigger_Mus=[]
    offlineBTriggerSelection=[]
    if len(muons)>0:
        for i in range(len(muons)):
            muon = muons[i]
            selection_hist.Fill("Total Muons",genWeight)

            if 60>muon.pt>4 and abs(muon.eta)<2.4:
                selection_hist.Fill("60>pt>4, |eta|<2.4",genWeight)

                if muon.id >= 1:
                    selection_hist.Fill("Loose ID ",genWeight)

                    if len(bjets)>0:
                        b=ROOT.TLorentzVector()
                        b.SetPtEtaPhiM(bjets[0].pt,bjets[0].eta,bjets[0].phi,bjets[0].mass)
                        m=ROOT.TLorentzVector()
                        m.SetPtEtaPhiM(muon.pt,muon.eta,muon.phi,muon.mass)
                        bdr=b.DeltaR(m)
                        if bdr>.4: 
                            selected_Mus+=[muon]
                            selection_hist.Fill("dr(b)>.4",genWeight)
                    if muon.isBPHMuon:
                        btrigger_Mus+=[muon]
                        if muon.pt>9:
                            selection_hist.Fill("pt>9",genWeight)
                            if muon.edB!=0:
                                if muon.dB/muon.edB>6:
                                    selection_hist.Fill("dbSig>6",genWeight)
                                    offlineBTriggerSelection+=[muon]
    return selected_Mus,btrigger_Mus,doubleTrigger_Mus, isoTrigger_Mus, offlineBTriggerSelection

def MuCleanedTauHad_Selection(selection_hist,muCtaus,selected_electrons,selected_mus,selected_bs,genWeight):
    selected_muclean_taus= []
    if len(muCtaus)>0:
        for i in range(len(muCtaus)):
            tau=muCtaus.at(i)
            selection_hist.Fill("Total Taus",genWeight)
            if (tau.pt>10 and abs(tau.eta)<2.4):
                selection_hist.Fill("Pt>10, |eta|<2.4",genWeight)
                if not (tau.mvaid>=4) and not reversedTauID:
                    continue
                else:
                    selection_hist.Fill("Medium ID",genWeight)

                if not (tau.mvaid<4 and tau.mvaid>0) and reversedTauID:
                    continue
                else:
                    selection_hist.Fill("Reversed Medium ID",genWeight)
                JetSeperation=False
                isLepFake=False
                t=ROOT.TLorentzVector()
                t.SetPtEtaPhiM(tau.pt, tau.eta, tau.phi, tau.mass)
                if len(selected_bs)>0:
                    b=ROOT.TLorentzVector()
                    b.SetPtEtaPhiM(selected_bs[0].pt,selected_bs[0].eta,selected_bs[0].phi,selected_bs[0].mass)

                    bdr=b.DeltaR(t)
                    if bdr>.5: 
                        JetSeperation=True
                for muon in selected_mus:
                    mu = ROOT.TLorentzVector()
                    mu.SetPtEtaPhiM(muon.pt, muon.eta, muon.phi, muon.mass)
                    mudr = t.DeltaR(mu)
                    if(mudr<.05):
                        isLepFake=True
                
                if JetSeperation:
                    
                    selection_hist.Fill("DR(tau,All Bjets)>.5",genWeight)
                    if not isLepFake:
                        selection_hist.Fill("DR(tau,Mu)>.05",genWeight)
                        selected_muclean_taus+=[tau]
    return selected_muclean_taus
def EleCleanedTauHad_Selection(selection_hist,eCtaus,selected_electrons,selected_mus,selected_bs,genWeight):
    selected_eclean_taus=[]
    if len(eCtaus)>0:
        for i in range(len(eCtaus)):
            tau=eCtaus.at(i)
            selection_hist.Fill("Total Taus",genWeight)
            if (tau.pt>10 and abs(tau.eta)<2.4):
                selection_hist.Fill("Pt>10, |eta|<2.4",genWeight)
                if not (tau.mvaid>=4) and not reversedTauID:
                    continue
                else:
                    selection_hist.Fill("Medium ID",genWeight)

                if not (tau.mvaid<4 and tau.mvaid>0) and reversedTauID:
                    continue
                else:
                    selection_hist.Fill("Reversed Medium ID",genWeight)
                JetSeperation=False
                isLepFake=False

                t=ROOT.TLorentzVector()
                t.SetPtEtaPhiM(tau.pt, tau.eta, tau.phi, tau.mass)
                if len(selected_bs)>0:
                    b=ROOT.TLorentzVector()
                    b.SetPtEtaPhiM(selected_bs[0].pt,selected_bs[0].eta,selected_bs[0].phi,selected_bs[0].mass)
                    bdr=b.DeltaR(t)
                    if bdr>.5: JetSeperation=True
                for electron in selected_electrons:
                    ele = ROOT.TLorentzVector()
                    ele.SetPtEtaPhiM(electron.pt, electron.eta, electron.phi, electron.mass)
                    edr = t.DeltaR(ele)
                    if(edr<.05):
                        isLepFake=True

                if JetSeperation:
                    selection_hist.Fill("DR(tau,Bjets)>.5",genWeight)
                    if not isLepFake:
                        selection_hist.Fill("DR(tau,e)>.05",genWeight)
                        selected_eclean_taus+=[tau]
    return selected_eclean_taus
def ElectronSelection(selection_hist,electrons, genWeight):
    selected_electrons=[]
    if len(electrons)>0:
        for i in range(len(electrons)):
            electron = electrons.at(i)
            selection_hist.Fill("Total Electrons",genWeight)
            if 60>electron.pt>7 and abs(electron.eta)<2.4:
                selection_hist.Fill("60>pt>7, |eta|<2.4",genWeight)
                if electron.id >= 1 :
                    
                    selection_hist.Fill("LooseID",genWeight)
                    if electron.iso>1 and reversedEIso==False:
                        selection_hist.Fill("Medium Iso",genWeight)
                    elif electron.iso<=1 and reversedEIso:
                        selection_hist.Fill("Medium Iso REVERSED",genWeight)
                        selected_electrons+=[electron]
    return selected_electrons