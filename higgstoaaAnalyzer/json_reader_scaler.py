import json

f = open("NUM_TrackerMuons_DEN_genTracks_Z_abseta_pt.json")
MuonSF_Dict = json.load(f)
def getMuSF():
    for etaBin in MuonSF_Dict.keys():
        print(etaBin)

getMuSF