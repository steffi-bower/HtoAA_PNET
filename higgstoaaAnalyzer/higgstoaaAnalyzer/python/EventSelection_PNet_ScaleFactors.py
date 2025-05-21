import ROOT,sys,os
import numpy as np
import correctionlib
import MyArgs
MyArgs.init()

ROOT.gInterpreter.Declare('#include "../interface/JetInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/MuonInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/ElectronInfoDS.h"')
ROOT.gInterpreter.Declare('#include "../interface/TauInfoDS.h"')

ESFFile = ROOT.TFile.Open("../../2018_ElectronLoose.root")
EleSFHist = ESFFile.Get("EGamma_SF2D")

ceval = correctionlib.CorrectionSet.from_file("muon_JPsi.json")
list(ceval.keys())

print("Inputs")
print(ceval["NUM_LooseID_DEN_TrackerMuons"].evaluate(1.7,16.8,"nominal"))
def Asymmetric_Lepton_Plotting(selection_hist,lepton1s,lepton2s,bjets,variable_hists,weight,channel,MET, TriggerMuons,isMC):
    selection_hist.Fill("NEvents",weight)
    Lep1Name = channel.split("_")[0]
    Lep2Name = channel.split("_")[1]
    if (len(lepton1s)>0):
        selection_hist.Fill(Lep1Name+">0",weight)
        if len(lepton2s)>0:
            selection_hist.Fill(Lep2Name+">0",weight)
            if len(bjets)>.9:
                selection_hist.Fill("nBjets>.9",weight)
                if len(bjets)<1.1:
                    selection_hist.Fill("nBjets<1.1",weight)
                
                    if len(TriggerMuons)>0:
                        b=ROOT.TLorentzVector()

                        mu=ROOT.TLorentzVector()
                        b.SetPtEtaPhiM(bjets[0].pt,bjets[0].eta,bjets[0].phi,bjets[0].mass)
                        #minmudr=999
                        #for mu in TriggerMuons:
                        #   m.SetPtEtaPhiM(mu.pt,mu.eta,mu.phi,mu.mass)
                        #    if b.DeltaR(m)<minmudr:
                        #        minmudr=b.DeltaR(m)
                        mu.SetPtEtaPhiM(TriggerMuons[0].pt,TriggerMuons[0].eta,TriggerMuons[0].phi,TriggerMuons[0].mass)
                        if (b.DeltaR(mu)<.5):
                            selection_hist.Fill("bJet Trigger Mu Match",weight)

                            l1=ROOT.TLorentzVector()
                            l1.SetPtEtaPhiM(lepton1s[0].pt,lepton1s[0].eta,lepton1s[0].phi,lepton1s[0].mass)
                            l2=ROOT.TLorentzVector()
                            l2.SetPtEtaPhiM(lepton2s[0].pt,lepton2s[0].eta,lepton2s[0].phi,lepton2s[0].mass)
                            mvis = (l1+l2).M()
                            bMass=b.M()
                            lepDR=l1.DeltaR(l2) 
                            leadBFlav=bjets[0].flavorprobb+bjets[0].flavorprobbb+bjets[0].flavorproblepb


                            if (isMC):
                                if "tauE" in Lep1Name:
                                    weight = weight*getEleSF(lepton1s[0].pt,lepton1s[0].eta)
                                if "tauE" in Lep2Name:
                                    weight = weight*getEleSF(lepton2s[0].pt,lepton2s[0].eta)
                                if "Mu" in Lep1Name:
                                    weight = weight*ceval["NUM_LooseID_DEN_TrackerMuons"].evaluate(lepton1s[0].eta,lepton1s[0].pt,muUncertainty)
                                if "Mu" in Lep2Name:
                                    weight = weight*ceval["NUM_LooseID_DEN_TrackerMuons"].evaluate(lepton2s[0].eta,lepton2s[0].pt,muUncertainty)
                                if "Tau" in channel:
                                    weight=weight*1.02
                            if l1.DeltaR(b)>.4 and l2.DeltaR(b)>.4:
                                selection_hist.Fill("lep[1,2], b dr >.4",weight)
                                if 6<bMass and bMass<16:
                                    selection_hist.Fill("2<bMass<20",weight)
                                    if mvis>4 and mvis<15:
                                        selection_hist.Fill("4<mVis<15",weight)
                                    #if mvis<3:
                                        #selection_hist.Fill("3>mvis",weight)
                                        if (lepDR<.7):#changed from 1.5 for simple testing Will likely change to .8
                                            selection_hist.Fill("lepDR<.7",weight)
                                            if MET<80:
                                                selection_hist.Fill("MET<80",weight)
                                                if np.sign(lepton1s[0].charge) != np.sign(lepton2s[0].charge) and SameSign==False:
                                                    selection_hist.Fill("Opposite Lepton Charge",weight)

                                                    variable_hists["h_"+channel+"_b1_ID_Total_isBPH"].Fill(leadBFlav,weight)
                                                    variable_hists["h_"+channel+"_b1_PNetID_isBPH"].Fill(bjets[0].pnet_score,weight)
                                                    variable_hists["h_"+channel+"_Mvis_isBPH"].Fill(mvis,weight)
                                                    variable_hists["h_"+channel+"_bMass_isBPH"].Fill(bMass,weight)
                                                    variable_hists["h_"+channel+"_lepDr_isBPH"].Fill(lepDR,weight)
                                                    variable_hists["h_"+channel+"_lep1DRB_isBPH"].Fill(l1.DeltaR(b),weight)
                                                    variable_hists["h_"+channel+"_lep2DRB_isBPH"].Fill(l2.DeltaR(b),weight)
                                                    variable_hists["h_"+channel+"_MET_isBPH"].Fill(MET,weight)
                                                    variable_hists["h_"+channel+"_NLep1s_isBPH"].Fill(len(lepton1s),weight)
                                                    variable_hists["h_"+channel+"_NLep2s_isBPH"].Fill(len(lepton2s),weight)
                                                    variable_hists["h_"+channel+"_mergedBPt_isBPH"].Fill(bjets[0].pt,weight)
                                                    variable_hists["h_"+channel+"_mergedLepPt_isBPH"].Fill((l1+l2).Pt(),weight)
                                                    variable_hists["h_"+channel+"_lep1Pt_isBPH"].Fill(lepton1s[0].pt,weight)
                                                    variable_hists["h_"+channel+"_lep2Pt_isBPH"].Fill(lepton2s[0].pt,weight)
                                                    if "tauE" in Lep1Name:

                                                        variable_hists["h_"+channel+"_eleIso_isBPH"].Fill(lepton1s[0].iso,weight)
                                                    if "tauE" in Lep2Name:

                                                        variable_hists["h_"+channel+"_eleIso_isBPH"].Fill(lepton2s[0].iso,weight)

                                                    if "Mu" in Lep1Name:

                                                        variable_hists["h_"+channel+"_muIso_isBPH"].Fill(lepton1s[0].iso,weight)
                                                    if "Mu" in Lep2Name:

                                                        variable_hists["h_"+channel+"_muIso_isBPH"].Fill(lepton2s[0].iso,weight)



                                                elif np.sign(lepton1s[0].charge) == np.sign(lepton2s[0].charge) and SameSign==True:
                                                    selection_hist.Fill("Same Lepton Charge",weight)

                                                    variable_hists["h_"+channel+"_b1_ID_Total_isBPH"].Fill(leadBFlav,weight)
                                                    variable_hists["h_"+channel+"_b1_PNetID_isBPH"].Fill(bjets[0].pnet_score,weight)
                                                    variable_hists["h_"+channel+"_Mvis_isBPH"].Fill(mvis,weight)
                                                    variable_hists["h_"+channel+"_bMass_isBPH"].Fill(bMass,weight)
                                                    variable_hists["h_"+channel+"_lepDr_isBPH"].Fill(lepDR,weight)
                                                    variable_hists["h_"+channel+"_lep1DRB_isBPH"].Fill(l1.DeltaR(b),weight)
                                                    variable_hists["h_"+channel+"_lep2DRB_isBPH"].Fill(l2.DeltaR(b),weight)
                                                    variable_hists["h_"+channel+"_MET_isBPH"].Fill(MET,weight)
                                                    variable_hists["h_"+channel+"_NLep1s_isBPH"].Fill(len(lepton1s),weight)
                                                    variable_hists["h_"+channel+"_NLep2s_isBPH"].Fill(len(lepton2s),weight)
                                                    variable_hists["h_"+channel+"_mergedBPt_isBPH"].Fill(bjets[0].pt,weight)
                                                    variable_hists["h_"+channel+"_mergedLepPt_isBPH"].Fill((l1+l2).Pt(),weight)
                                                    variable_hists["h_"+channel+"_lep1Pt_isBPH"].Fill(lepton1s[0].pt,weight)
                                                    variable_hists["h_"+channel+"_lep2Pt_isBPH"].Fill(lepton2s[0].pt,weight)
                                                    if "tauE" in Lep1Name:

                                                        variable_hists["h_"+channel+"_eleIso_isBPH"].Fill(lepton1s[0].iso,weight)
                                                    if "tauE" in Lep2Name:

                                                        variable_hists["h_"+channel+"_eleIso_isBPH"].Fill(lepton2s[0].iso,weight)

                                                    if "Mu" in Lep1Name:

                                                        variable_hists["h_"+channel+"_muIso_isBPH"].Fill(lepton1s[0].iso,weight)
                                                    if "Mu" in Lep2Name:

                                                        variable_hists["h_"+channel+"_muIso_isBPH"].Fill(lepton2s[0].iso,weight)

def DiTauPlotting(selection_hist,taus,bjets,variable_hists,weight,MET, TriggerMuons, eles,mus):
    selection_hist.Fill("NEvents",weight)


    if (len(taus)==1):
        selection_hist.Fill("taus==1",weight)
        if (len(mus)==0):
            selection_hist.Fill("nMuons==0",weight)

            if (len(eles)==0):
                selection_hist.Fill("neles==0",weight)

                if len(bjets)>.9:
                    selection_hist.Fill("nBjets>.9",weight)
                    if len(bjets)<1.1:
                        selection_hist.Fill("nBjets<1.1",weight)
                    
                        if len(TriggerMuons)>0:
                            b=ROOT.TLorentzVector()

                            mu=ROOT.TLorentzVector()
                            b.SetPtEtaPhiM(bjets[0].pt,bjets[0].eta,bjets[0].phi,bjets[0].mass)
                            mu.SetPtEtaPhiM(TriggerMuons[0].pt,TriggerMuons[0].eta,TriggerMuons[0].phi,TriggerMuons[0].mass)
                            if (b.DeltaR(mu)<.5):
                                selection_hist.Fill("bJet Trigger Mu Match",weight)

                                l1=ROOT.TLorentzVector()
                                l1.SetPtEtaPhiM(taus[0].pt,taus[0].eta,taus[0].phi,taus[0].mass)

                                mvis = (l1).M()
                                bMass=b.M()
                                leadBFlav=bjets[0].flavorprobb+bjets[0].flavorprobbb+bjets[0].flavorproblepb



                                if l1.DeltaR(b)>.6:
                                    selection_hist.Fill("tau, b dr >.4",weight)
                                    if 6<bMass and bMass<16:
                                        selection_hist.Fill("2<bMass<20",weight)
                                        if mvis>2 and mvis<20:
                                            selection_hist.Fill("2<mVis<20",weight)
                                            if MET<100:
                                                selection_hist.Fill("MET<100",weight)
                                                #if np.sign(taus[0].charge) == 0 :
                                                if True:
                                                    selection_hist.Fill("neutralTaus",weight)
                                                    variable_hists["h_taupt"].Fill(taus[0].pt,weight)
                                                    #variable_hists["h_tauCharge"].Fill(taus[0].charge,weight)

                                                    variable_hists["h_ditauID"].Fill(taus[0].ditau2017v1,weight)
                                                    variable_hists["h_NdiTau"].Fill(len(taus),weight)
                                                    variable_hists["h_diTau_b1_PNetID"].Fill(bjets[0].pnet_score,weight)
                                                    variable_hists["h_diTau_Mvis"].Fill(mvis,weight)
                                                    variable_hists["h_diTau_bMass"].Fill(bMass,weight)
                                                    variable_hists["h_diTau_tauDRB"].Fill(l1.DeltaR(b),weight)
                                                    variable_hists["h_diTau_MET"].Fill(MET,weight)
                                                    variable_hists["h_diTau_NEles"].Fill(len(eles),weight)
                                                    variable_hists["h_diTau_NMus"].Fill(len(mus),weight)



def GetElePtBinnumber(pt):
    if pt<20 and pt>10:
        return 1
    elif pt<35 and pt>20:
        return 2
    elif pt<50 and pt>35:
        return 3
    elif pt<100 and pt>50:
        return 4
    elif pt<35 and pt>100:
        return 5
    elif pt<200 and pt>100:
        return 6
    else: return 7
def GetEleEtaBinNumber(eta):
    if eta<-2:
        return 1
    elif (eta)<-1.566:
        return 2
    elif (eta)<-1.44:
        return 3
    elif (eta)<-.8:
        return 4
    elif (eta)<0:
        return 5 
    elif (eta)<.8:
        return 6
    elif (eta)<1.444:
        return 7
    elif (eta)<1.566:
        return 8
    elif (eta)<2:
        return 9
    else: return 10
def getEleSF(pt,eta):
    etabin = GetEleEtaBinNumber(eta)
    ptbin=GetElePtBinnumber(pt)
    scalefactor = EleSFHist.GetBinContent(etabin,ptbin)+EleSFHist.GetBinError(etabin,ptbin) * EleUncertainty
    return scalefactor

