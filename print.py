import ROOT
from ROOT import *


f = TFile("/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140711_DL/merge.root", "read")

t = f.Get("evaluate")

for e in t:
    print e.MET
