import ROOT
import sys
import math

QCD_XSections={
    '15to30':1.246e+09,
    '30to50':1.068e+08,
    '50to80':1.575e+07, 
    '80to120':2.340e+06, 
    '120to170':4.082e+05,
    '170to300':1.036e+05,
    '300to470':6.825e+03,
    '470to600':5.523e+02,
    '600to800':1.564e+02,
    '800to1000':2.620e+01,
    '1000to1400':7.486e+00,
    '1400to1800': 6.499e-01,
    '1800to2400':8.734e-02 ,
    '2400to3200':5.252e-03 ,
    '3200toInf':1.352e-04
}
pi = math.pi

c_t = 1
m_t = 1.77686#Tau Mass
fa = 1000#dimensional param

m_a = [10,20,30,40,50,60,70,80,90,100]#pseudoScalar Mass
xsec_gt = [1.0256092e-07, 1.930e-07 , 5.021e-07]

#Br = [0, 6.8 , 9.7 , 5.7 , 6.2 , 3.0 , 3.0 , 9.7 , 0.88 , 1.9 , 1.8 , 2.1 , 2.9] #so Model 1 is M[_][1]
Br=[6.7,3.4,2.5,1.9,1.5,1.2,.95,.79,.66,.57]#Branching ration of TCP to tau tau from theory paper model 1
xsec_M = []

for i in range (9):
    Gamma_tt = ((c_t**2*m_a[i]/(8*pi))*m_t**2*math.sqrt(1-4*m_t**2/m_a[i]**2))/fa**2
    xsec_g_TCP = 1/ Gamma_tt#cross section of gg fusion to tcp
    xsec_M_list = xsec_g_TCP * Br[i]#Cross Section of gg fusion to TCP to tau Tau
    xsec_M.append(xsec_M_list)
    #print xsec_M[j][i]
###Rescale each
xsec_TCP10 = xsec_M[0]*41.53e3
xsec_TCP30 = xsec_M[2]*41.53e3
xsec_TCP50 = xsec_M[4]*41.53e3
TCP_M30_XSections={
    '400toInf':xsec_M[2]*1.930e-07,
    '100to400':xsec_M[2]*8.395e-06,
    '0to100':xsec_M[2]*8.887e-05 
}
DY_xsecs={"FULL_HT":5.357e+03}
WZ_xsecs={"FULL_HT":2.749e+01}
WJetstoLL_xsecs={"FULL_HT":5.375e+04}
TTBar_xsecs={"FULL_HT":7.502e+02}
SUSY_xsecs={"FULL_HT":2.749e+01}
DY_LowMass_xsecs={"FULL_HT":1.589e+04}
QCD_2017_xsecs={
    '50to100':1.868e+08,
    '100to200':2.344e+07,
    '200to300':1.555e+06, 
    '300to500':3.250e+05, 
    #'500to700':3.056e+04,
    '700to1000':6.444e+03 ,
    '1000to1500':1.114e+03,
    '1500to2000':1.072e+02,
    '2000toInf':2.198e+01 ,
}
WZTo3LNu_2018_xsecs={"FULL_HT":5.340e+00}
WJetsToLNu_2018_xsecs={"FULL_HT":5.513e+04}
WW_2018_xsecs={"FULL_HT":7.462e+01}
WZ_2018_xsecs={"FULL_HT":2.739e+01}
ZZ_2018_xsecs={"FULL_HT":1.221e+01}
ZZTo4L_2018_xsecs={"FULL_HT":1.325e+00}
DYJetsToLL_2018_xsecs={
    #"10to50": 1.574e+04,
    #'50':5.695e+03,
    'FULL_HT':5.695e+03
}
TTJets_2018_xsecs={"FULL_HT":6.637e+02}
#SUSY_2018_xsecs={"FULL_HT":2.263e+02}
SUSY_2018_xsecs={"FULL_HT":2.263}
QCD_Flat_2018_xsecs={"FULL_HT": 1.363e+09}
QCD_BFilter_2018_xsecs={
    "100to200" : 1.420e+06,
    '200to300' : 1.125e+05,
    '300to500' : 2.895e+04,
    '500to700' : 3.226e+03,
    '700to1000' : 6.355e+02,
    '1000to1500' : 1.427e+02,
    '1500to2000' : 1.848e+01,
    '2000toInf' : 3.474e+00 
}
QCD_PtBin_2018_xsecs={
    '15to30' : 1.246e+09,
    '30to50' : 1.068e+08,
    '50to80' : 1.569e+07,
    '80to120' : 2.343e+06,
    '120to170' : 4.062e+05,
    '170to300' : 1.032e+05,
    '300to470' : 6.831e+03,
    '470to600' :  5.515e+02,
    '600to800' : 1.567e+02,
    '800to1000' : 2.622e+01,
    '1000to1400' : 7.455e+00,
    '1400to1800' : 6.477e-01
}