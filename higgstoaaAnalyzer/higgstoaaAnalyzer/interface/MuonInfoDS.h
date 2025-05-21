#ifndef __TCPAnalysis_MuonInfoDS_H__
#define __TCPAnalysis_MuonInfoDS_H__

#include <vector>

struct MuonInfo {
  float pt, eta, phi, mass, charge;
  int id; // 1 loose, 2 medium, 3 tight
  float iso; 
  float dxy, dz;
  bool isBPHMuon;
  bool isMuIsoTrigMuon;
  bool isDoubleMu;
  float dB;
  float edB;


  bool operator<(const MuonInfo& m) const { return pt < m.pt; }
  
};

typedef class std::vector<MuonInfo> MuonInfoDS;

#endif
