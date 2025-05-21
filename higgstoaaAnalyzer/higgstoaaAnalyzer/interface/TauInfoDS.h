#ifndef __TCPAnalysis_TauInfoDS_H__
#define __TCPAnalysis_TauInfoDS_H__

#include <vector>

struct TauInfo {
  float pt, eta, phi, mass, charge;
  int decaymode;
  float mvaidraw;
  int mvaid; // VVLoose 1, VLoose 2, Loose 3, Medium 4, Tight 5, VTight 6, VVTight 7
  float deepidraw;
  int deepid; // VVVLoose 0, VVLoose 1, VLoose 2, Loose 3, Medium 4, Tight 5, VTight 6, VVTight 7
  //float dxy, dz;

  bool operator<(const TauInfo& t) const { return pt < t.pt; }
  
};

typedef class std::vector<TauInfo> TauInfoDS;

#endif
