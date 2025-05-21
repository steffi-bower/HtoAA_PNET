import ROOT
import sys
import subprocess
import string,math,os
import glob
import numpy as np
import mplhep as hep
import matplotlib.colors as mcolors

import matplotlib.pylab as plt
import sklearn.metrics as metrics
label = "Oct_24Training"
ROOT.gROOT.SetBatch(True)

hep.style.use(hep.style.ROOT)
hep.cms.label('', data=False, year=2018)
inFileLoss = "Loss.csv"
inFileAcc = "Accuracy.csv"
Loss_Data=[]
Acc_Data=[]
epoch_Data = []
first_line=True
Loss=open(inFileLoss, "r")
outDir = "higgstoaaAnalyzer/graphs/"+label+"/"
def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)   
checkAndMakeDir(outDir)
for l in Loss:
    if not first_line:

        values = l.split(',')
        epoch_Data.append(float(values[1]))
        Loss_Data.append(float(values[2]))
    first_line=False

Loss.close()


first_line=True
Acc=open(inFileAcc, "r")
for l in Acc:
    if not first_line:
        values = l.split(',')
        Acc_Data.append(float(values[2]))
    first_line=False

Acc.close()

plt.plot(epoch_Data, Loss_Data, 'tab:cyan' )

plt.grid(axis='x', color='0.95')

plt.grid(axis='y', color='0.95')

plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.savefig(outDir+"Loss.png")
plt.close()

hep.style.use(hep.style.ROOT)
hep.cms.label('', data=False, year=2018)
plt.plot(epoch_Data, Acc_Data, 'tab:cyan' )

plt.grid(axis='x', color='0.95')

plt.grid(axis='y', color='0.95')

plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.savefig(outDir+"Acc.png")
plt.close()