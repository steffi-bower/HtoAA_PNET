#ifndef __TCPAnalysis_GenParticleInfoDS_H__
#define __TCPAnalysis_GenParticleInfoDS_H__

#include <vector>

struct GenParticleInfo {
  float pt, eta, phi, mass;
  int pdgid, stepToNull, nmothers;
  bool isHardProcess;
  bool isDirectHardProcessTauDecayProductFinalState;
  bool isFromB;
  bool nullMom;

  bool operator<(const GenParticleInfo& p) const { return pt < p.pt; }
  
};

typedef class std::vector<GenParticleInfo> GenParticleInfoDS;

#endif
