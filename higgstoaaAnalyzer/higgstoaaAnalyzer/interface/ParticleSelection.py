import ROOT,sys,os
import numpy as np
ROOT.gInterpreter.Declare('#include "../interface/JetInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/MuonInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/ElectronInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/TauInfoDS.h"')

def bJetSelection(jets, selection_hist,genWeight):
    bjets=[]
    if jets.size()>0:
        for i in range(jets.size()):
            jet = jets.at(i)
            if jet.pt>10 and abs(jet.eta)<2.5:
                selection_hist.Fill("pt>10, |eta|<2.5",genWeight)
                if jet.id >= 1:
                    selection_hist.Fill("Loose Jet ID",genWeight)
                    if (jet.flavorprobb+jet.flavorprobbb+jet.flavorproblepb) > 0.7476:
                        selection_hist.Fill("total Deep Flavor >.7476",genWeight)
                        bjets+=[jet]
    return bjets
def MuonSelection(muons,bjets,selection_hist,genWeight):
    selected_Mus=[]
    btrigger_Mus=[]
    isoTrigger_Mus=[]
    doubleTrigger_Mus=[]
    if muons.size()>0:
        for i in range(muons.size()):
            muon = muons.at(i)
            selection_hist.Fill("Total Muons",genWeight)
            if muon.isBPHMuon:
                btrigger_Mus+=[muon]
            if muon.isMuIsoTrigMuon:
                isoTrigger_Mus+=[muon]
            if muon.isDoubleMu:
                doubleTrigger_Mus+=[muon]
            if muon.pt>3 and abs(muon.eta)<2.4:
                selection_hist.Fill("pt>3, |eta|<2.4",genWeight)

                if muon.id >= 1:
                    selection_hist.Fill("Loose ID",genWeight)
                    selected_mus+=[muon]
                    isFromB=False
                    if (bjets.size()>0):
                        mu = ROOT.TLorentzVector()
                        b=ROOT.TLorentzVector()
                        mu.SetPtEtaPhiM(muon.pt, muon.eta, muon.phi, muon.mass)
                        b.SetPtEtaPhiM(bjets[0].pt, bjets[0].eta, bjets[0].phi, bjets[0].mass)
                        dr = b.DeltaR(mu)
                        if (dr<.4):
                            isFromB=True
                    if  not isFromB:
                        selection_hist.Fill("DR(Mu,b)>.4",genWeight)
                        if muon.isMuIsoTrigMuon:
                            selection_hist.Fill("Single Mu Firing*",genWeight)
                        if muon.isDoubleMu:
                            selection_hist.Fill("Double Mu Firing*",genWeight)
                        if muon.isBPHMuon:
                            selection_hist.Fill("BPH MuFiring*",genWeight)
                        selected_Mus+=[muon]

    return selected_mus,btriggerMus,doubleTrigger_Mus, isoTrigger_Mus

def MuCleanedTauHad_Selection(selection_hist,muCtaus,selected_electrons,selected_mus,selected_bs,genWeight):
    if muCtaus.size()>0:
        for i in range(muCtaus.size()):
            tau=muCtaus.at(i)
            selection_hist.Fill("Total Taus",genWeight)
            if (tau.pt>10 and abs(tau.eta)<2.4):
                selection_hist.Fill("Pt>10, eta<2.4",genWeight)
                if (tau.mvaid>=3):
                    selection_hist.Fill("Loose MVA ID",genWeight)
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
                    for electron in selected_electrons:
                        ele = ROOT.TLorentzVector()
                        ele.SetPtEtaPhiM(electron.pt, electron.eta, electron.phi, electron.mass)
                        edr = t.DeltaR(ele)

                        if(edr<.1):
                            isLepFake=True
                    for muon in selected_mus:
                        mu = ROOT.TLorentzVector()
                        mu.SetPtEtaPhiM(muon.pt, muon.eta, muon.phi, muon.mass)
                        mudr = t.DeltaR(mu)
                        if(mudr<.1):
                            isLepFake=True
                    if JetSeperation:
                        selection_hist.Fill("DR(tau,All Bjets)>.5",genWeight)
                        if not isLepFake:
                            selection_hist.Fill("DR(tau,Lep)>.1",genWeight)
                            selected_muclean_taus+=[tau]
            return selected_muclean_taus
def EleCleanedTauHad_Selection(selection_hist,eCtaus,selected_electrons,selected_mus,selected_bs,genWeight):
    if eCtaus.size()>0:
        for i in range(eCtaus.size()):
            tau=eCtaus.at(i)
            selection_hist.Fill("Total Taus",genWeight)
            if (tau.pt>10 and abs(tau.eta)<2.4):
                selection_hist.Fill("Pt>10, eta<2.4",genWeight)
                if (tau.mvaid>=3):
                    selection_hist.Fill("Loose MVA ID",genWeight)
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
                        if(edr<.1):
                            isLepFake=True
                    for muon in selected_mus:
                        mu = ROOT.TLorentzVector()
                        mu.SetPtEtaPhiM(muon.pt, muon.eta, muon.phi, muon.mass)
                        edr = t.DeltaR(mu)
                        if(dr<.1):
                            eisLepFake=True
                    if JetSeperation:
                        selection_hist.Fill("DR(tau,Bjets)>.5",genWeight)
                        if not isLepFake:
                            selection_hist.Fill("DR(tau,Lep)>.1",genWeight)
                            selected_eclean_taus+=[tau]
        return selected_eclean_taus
def ElectronSelection(selection_hist,electrons):
    if electrons.size()>0:
        for i in range(electrons.size()):
            electron = electrons.at(i)
            selection_hist.Fill("Total Electrons",genWeight)
            if electron.pt>7 and abs(electron.eta)<2.4:
                selection_hist.Fill("pt>7, eta<2.4",genWeight)
                if electron.id >= 1 :
                    selection_hist.Fill("LooseID",genWeight)
                    selected_electrons+=[electron]
    return selected_electrons