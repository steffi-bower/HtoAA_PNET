#ifndef __TCPAnalysis_ElectronInfoDS_H__
#define __TCPAnalysis_ElectronInfoDS_H__

#include <vector>

struct ElectronInfo {
  float pt, eta, phi, mass, charge;
  int id; // cut base ID without rel iso: 1 loose, 2 medium, 3 tight
  int iso; // reliso: 0 non iso, 1 loose, 2 medium, 3 tight
  float dxy, dz;
  float dB;
  float edB;
  float lowptid;   // MVA score for low pt electrons
  
  bool operator<(const ElectronInfo& e) const { return pt < e.pt; }
  
};

typedef class std::vector<ElectronInfo> ElectronInfoDS;

#endif
