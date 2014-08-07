import ROOT
from ROOT import *


f = TFile("/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140727_DL/merge.root", "read")

new_f = TFile("/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140727_DL/mergeDL.root", "recreate")

t1 = f.Get("train")
new_t1 = t1.CopyTree("tNboost_tauveto < 0.5 && cutBTag70 > 0.5 && tNboost_fj2met > 0.5")
new_t1.Write("trainDL")

t2 = f.Get("validate")
new_t2 = t2.CopyTree("tNboost_tauveto < 0.5 && cutBTag70 > 0.5 && tNboost_fj2met > 0.5")
new_t2.Write("validateDL")

t3 = f.Get("evaluate")
new_t3 = t3.CopyTree("tNboost_tauveto < 0.5 && cutBTag70 > 0.5 && tNboost_fj2met > 0.5")
new_t3.Write("evaluateDL")

new_f.Close()

f.Close()
