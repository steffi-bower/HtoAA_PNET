#ifndef __TCPAnalysis_JetInfoDS_H__
#define __TCPAnalysis_JetInfoDS_H__

#include <vector>

struct JetInfo {
  float pt, eta, phi, mass;
  float ptuncor; 
  float deepcsv; 
  float csvprobb;
  float csvprobbb; 
  float flavorproblepb;
  float flavorprobb;
  float flavorprobbb;
  float pnet_score;
  int genJet;
  float ditau2017v1;
  float ditau2017MDv1;
  float ditau2017v2;
  float ditau2017MDv2;
  int id; //jetID 1, jetID + lept-veto 2
  int puid; // fail 0, loose 1, medium 2, tight 3

  bool operator<(const JetInfo& j) const { return pt < j.pt; }
  
};

typedef class std::vector<JetInfo> JetInfoDS;

#endif
