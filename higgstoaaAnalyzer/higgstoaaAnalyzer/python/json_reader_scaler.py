import correctionlib

ceval = correctionlib.CorrectionSet.from_file("Efficiencies_muon_generalTracks_Z_Run2018_UL_ID.json")
list(ceval.keys())

print("Inputs")
for corr in ceval.values():
    print(f"Correction {corr.name} has {len(corr.inputs)} inputs")
    for ix in corr.inputs:
        print(f"   Input {ix.name} ({ix.type}): {ix.description}")
