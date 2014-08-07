#!/bin/usr/python

import sys
import os

from types import *

import random
from random import randint

import pandas as pd
import numpy as np
import ROOT


def main():

    Lumi = 20.3

    file_dir = '/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_intput/20140727_DL/'
    out_dir = '/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140727_DL/'    

    sig_train_validate = ['T700_L1', 'T650_L1', 'T750_L1', 'T800_L1', 'T650_L50', 'T700_L50', 'T750_L50', 'T800_L50']
    sig_evaluate = ['T700_L1']
    bkg_train_validate_evaluate = ['Tt']

    xsec = {}
    xsec['T650_L1'] = 0.0139566
    xsec['T650_L50'] = 0.0139566
    xsec['T700_L1'] = 0.0081141 
    xsec['T700_L50'] = 0.0081141
    xsec['T750_L1'] = 0.00480639
    xsec['T750_L50'] = 0.00480639
    xsec['T800_L1'] = 0.00289588
    xsec['T800_L50'] = 0.00289588
    xsec['Tt'] = 253.00 * 0.543
 
    # define branches
    sig = np.zeros(1, dtype=int)
    evt_weight = np.zeros(1, dtype=float)
    met = np.zeros(1, dtype=float)
    mt = np.zeros(1, dtype=float)
    ht = np.zeros(1, dtype=float)
    htratio = np.zeros(1, dtype=float)
    metsig = np.zeros(1, dtype=float)
    htsig = np.zeros(1, dtype=float)
    amt2 = np.zeros(1, dtype=float)
    mt2tau = np.zeros(1, dtype=float)
    topness = np.zeros(1, dtype=float)
    jet1_pt = np.zeros(1, dtype=float)
    jet2_pt = np.zeros(1, dtype=float)
    jet3_pt = np.zeros(1, dtype=float)
    jet4_pt = np.zeros(1, dtype=float)
    jet1met_dphi = np.zeros(1, dtype=float)
    jet2met_dphi = np.zeros(1, dtype=float)
    jet3met_dphi = np.zeros(1, dtype=float)
    jet4met_dphi = np.zeros(1, dtype=float)
    lepb_mindr = np.zeros(1, dtype=float)
    lepfj1_dr = np.zeros(1, dtype=float)
    cutbtag70 = np.zeros(1, dtype=int)
    tauveto = np.zeros(1, dtype=int)
    fj1_pt = np.zeros(1, dtype=float)
    fj1_m = np.zeros(1, dtype=float)
    fj2met_dphi = np.zeros(1, dtype=float)

    lepmv1b_dr = np.zeros(1, dtype=float)
    tnboost_jets = np.zeros(1, dtype=int)
    tnboost_btag = np.zeros(1, dtype=int)
    tnboost_jmet = np.zeros(1, dtype=int)
    tnboost_met = np.zeros(1, dtype=int)
    tnboost_mt = np.zeros(1, dtype=int)
    tnboost_amt2 = np.zeros(1, dtype=int)
    tnboost_topness = np.zeros(1, dtype=int)
    tnboost_htsig = np.zeros(1, dtype=int)
    tnboost_fj2met = np.zeros(1, dtype=int)
    tnboost_tauveto = np.zeros(1, dtype=int)
    tnboost_toptag = np.zeros(1, dtype=int)
    tnboost_lepb = np.zeros(1, dtype=int)
    tnboost = np.zeros(1, dtype=int)

   
    # signal
    f = ROOT.TFile(out_dir+'signal.root', "recreate")
    tree_sig = {}
    tree_sig['train'] = ROOT.TTree("train", "tree title")
    tree_sig['validate'] = ROOT.TTree("validate", "tree title")
    tree_sig['evaluate'] = ROOT.TTree("evaluate", "tree title")

    for k, t in tree_sig.items():

        t.Branch('Signal',  sig, 'Signal/I')
        t.Branch("EventWeight", evt_weight, 'EventWeight/D');
        t.Branch('MET',  met, 'MET/D')
        t.Branch('mTW', mt, 'mTW/D');
        t.Branch('HT', ht ,'HT/D');
        t.Branch('HTratio', htratio,'HTratio/D');
        t.Branch('METsig', metsig,'METsig/D');
        t.Branch('HTmissSig', htsig,'HTmissSig/D');
        t.Branch('aMT2', amt2,'aMT2/D');
        t.Branch('MT2tau', mt2tau,'MT2tau/D');
        t.Branch('Topness', topness,'Topness/D');
        t.Branch('Jet1_Pt', jet1_pt,'Jet1_Pt/D');
        t.Branch('Jet2_Pt', jet2_pt,'Jet2_Pt/D');
        t.Branch('Jet3_Pt', jet3_pt,'Jet3_Pt/D');
        t.Branch('Jet4_Pt', jet4_pt,'Jet4_Pt/D');
        t.Branch('Jet1_dPhiMET', jet1met_dphi,'Jet1_dPhiMET/D');
        t.Branch('Jet2_dPhiMET', jet2met_dphi,'Jet2_dPhiMET/D');
        t.Branch('Jet3_dPhiMET', jet3met_dphi,'Jet3_dPhiMET/D');
        t.Branch('Jet4_dPhiMET', jet4met_dphi,'Jet4_dPhiMET/D');
        t.Branch('Lepton_BTag70Jet_mindR', lepb_mindr,'Lepton_BTag70Jet_mindR/D');
        t.Branch('Lepton_TrimmedJet1_dR', lepfj1_dr,'Lepton_TrimmedJet1_dR/D');
        t.Branch('cutBTag70', cutbtag70,'cutBTag70/I');
        t.Branch('Tauveto', tauveto, 'Tauveto/I');
        t.Branch('TrimmedJet1_Pt', fj1_pt,'TrimmedJet1_Pt/D');
        t.Branch('TrimmedJet1_4VM', fj1_m,'TrimmedJet1_4VM/D');
        t.Branch('TrimmedJet2_dPhiMET', fj2met_dphi,'TrimmedJet2_dPhiMET/D');

        t.Branch('Lepton_BMV1Jet_dR', lepmv1b_dr,'Lepton_BMV1Jet_dR/D');
        t.Branch('tNboost_jets', tnboost_jets,'tNboost_jets/I');
        t.Branch('tNboost_btag', tnboost_btag,'tNboost_btag/I');
        t.Branch('tNboost_jmet', tnboost_jmet,'tNboost_jmet/I');
        t.Branch('tNboost_met', tnboost_met,'tNboost_met/I');
        t.Branch('tNboost_mt', tnboost_mt,'tNboost_mt/I');
        t.Branch('tNboost_amt2', tnboost_amt2,'tNboost_amt2/I');
        t.Branch('tNboost_topness', tnboost_topness,'tNboost_topness/I');
        t.Branch('tNboost_htsig', tnboost_htsig,'tNboost_htsig/I');
        t.Branch('tNboost_fj2met', tnboost_fj2met,'tNboost_fj2met/I');
        t.Branch('tNboost_tauveto', tnboost_tauveto,'tNboost_tauveto/I');
        t.Branch('tNboost_toptag', tnboost_toptag,'tNboost_toptag/I');
        t.Branch('tNboost_lepb', tnboost_lepb,'tNboost_lepb/I');
        t.Branch('tNboost', tnboost,'tNboost/I');


    for i in sig_train_validate:
        f_train = ROOT.TFile(file_dir+i+'.root', "read")
        t_train = f_train.Get('minuit') 
        
        hbook = f_train.Get("hbook")
        print hbook.GetBinContent(2)
        sf = Lumi/(float(xsec[i]) * float(hbook.GetBinContent(2)) )   # remove the dependence of xsection

        for e in t_train:
            sig[0] = 1
            evt_weight[0] = e.EventWeight * sf
            met[0] = e.MET
            mt[0] = e.mTW
            ht[0] = e.HT
            htratio[0] = e.HTratio
            metsig[0] = e.METsig
            htsig[0] = e.HTmissSig
            amt2[0] = e.aMT2
            mt2tau[0] = e.MT2tau
            topness[0] = e.Topness
            jet1_pt[0] = e.Jet1_Pt
            jet2_pt[0] = e.Jet2_Pt
            jet3_pt[0] = e.Jet3_Pt
            jet4_pt[0] = e.Jet4_Pt
            jet1met_dphi[0] = e.Jet1_dPhiMET
            jet2met_dphi[0] = e.Jet2_dPhiMET
            jet3met_dphi[0] = e.Jet3_dPhiMET
            jet4met_dphi[0] = e.Jet4_dPhiMET
            lepb_mindr[0] = e.Lepton_BTag70Jet_mindR
            lepfj1_dr[0] = e.Lepton_TrimmedJet1_dR
            cutbtag70[0] = e.cutBTag70
            tauveto[0] = e.Tauveto
            fj1_pt[0] = e.TrimmedJet1_Pt
            fj1_m[0] = e.TrimmedJet1_4VM
            fj2met_dphi[0] = e.TrimmedJet2_dPhiMET

            lepmv1b_dr[0] = e.Lepton_BMV1Jet_dR
            tnboost_jets[0] = e.tNboost_jets
            tnboost_btag[0] = e.tNboost_btag
            tnboost_jmet[0] = e.tNboost_jmet
            tnboost_met[0] = e.tNboost_met
            tnboost_mt[0] = e.tNboost_mt
            tnboost_amt2[0] = e.tNboost_amt2
            tnboost_topness[0] = e.tNboost_topness
            tnboost_htsig[0] = e.tNboost_htsig
            tnboost_fj2met[0] = e.tNboost_fj2met
            tnboost_tauveto[0] = e.tNboost_tauveto
            tnboost_toptag[0] = e.tNboost_toptag
            tnboost_lepb[0] = e.tNboost_lepb
            tnboost[0] = e.tNboost


            r = randint(1,11)
            if r==1:
                tree_sig['validate'].Fill()
            else:
                tree_sig['train'].Fill()

        f_train.Close()

    for i in sig_evaluate:
        f_evaluate = ROOT.TFile(file_dir+i+'.root', "read")
        t_evaluate = f_evaluate.Get('minuit')

        hbook = f_evaluate.Get("hbook")
        print hbook.GetBinContent(2)
        sf = Lumi/(float(xsec[i]) * float(hbook.GetBinContent(2)))

        for e in t_evaluate:
            sig[0] = 1
            evt_weight[0] = e.EventWeight * sf
            met[0] = e.MET
            mt[0] = e.mTW
            ht[0] = e.HT
            htratio[0] = e.HTratio
            metsig[0] = e.METsig
            htsig[0] = e.HTmissSig
            amt2[0] = e.aMT2
            mt2tau[0] = e.MT2tau
            topness[0] = e.Topness
            jet1_pt[0] = e.Jet1_Pt
            jet2_pt[0] = e.Jet2_Pt
            jet3_pt[0] = e.Jet3_Pt
            jet4_pt[0] = e.Jet4_Pt
            jet1met_dphi[0] = e.Jet1_dPhiMET
            jet2met_dphi[0] = e.Jet2_dPhiMET
            jet3met_dphi[0] = e.Jet3_dPhiMET
            jet4met_dphi[0] = e.Jet4_dPhiMET
            lepb_mindr[0] = e.Lepton_BTag70Jet_mindR
            lepfj1_dr[0] = e.Lepton_TrimmedJet1_dR
            cutbtag70[0] = e.cutBTag70
            tauveto[0] = e.Tauveto
            fj1_pt[0] = e.TrimmedJet1_Pt
            fj1_m[0] = e.TrimmedJet1_4VM
            fj2met_dphi[0] = e.TrimmedJet2_dPhiMET

            lepmv1b_dr[0] = e.Lepton_BMV1Jet_dR
            tnboost_jets[0] = e.tNboost_jets
            tnboost_btag[0] = e.tNboost_btag
            tnboost_jmet[0] = e.tNboost_jmet
            tnboost_met[0] = e.tNboost_met
            tnboost_mt[0] = e.tNboost_mt
            tnboost_amt2[0] = e.tNboost_amt2
            tnboost_topness[0] = e.tNboost_topness
            tnboost_htsig[0] = e.tNboost_htsig
            tnboost_fj2met[0] = e.tNboost_fj2met
            tnboost_tauveto[0] = e.tNboost_tauveto
            tnboost_toptag[0] = e.tNboost_toptag
            tnboost_lepb[0] = e.tNboost_lepb
            tnboost[0] = e.tNboost


            # use T700_L1 to evaluate performance
            tree_sig['evaluate'].Fill()
        f_evaluate.Close()

    f.Write()
    f.Close()


    # background
    f = ROOT.TFile(out_dir+'background.root', "recreate")
    tree_bkg = {}
    tree_bkg['train'] = ROOT.TTree("train", "tree title")
    tree_bkg['validate'] = ROOT.TTree("validate", "tree title")
    tree_bkg['evaluate'] = ROOT.TTree("evaluate", "tree title")
 

    for k, t in tree_bkg.items():

        t.Branch('Signal',  sig, 'Signal/I')
        t.Branch("EventWeight", evt_weight, 'EventWeight/D');
        t.Branch('MET',  met, 'MET/D')
        t.Branch('mTW', mt, 'mTW/D');
        t.Branch('HT', ht ,'HT/D');
        t.Branch('HTratio', htratio,'HTratio/D');
        t.Branch('METsig', metsig,'METsig/D');
        t.Branch('HTmissSig', htsig,'HTmissSig/D');
        t.Branch('aMT2', amt2,'aMT2/D');
        t.Branch('MT2tau', mt2tau,'MT2tau/D');
        t.Branch('Topness', topness,'Topness/D');
        t.Branch('Jet1_Pt', jet1_pt,'Jet1_Pt/D');
        t.Branch('Jet2_Pt', jet2_pt,'Jet2_Pt/D');
        t.Branch('Jet3_Pt', jet3_pt,'Jet3_Pt/D');
        t.Branch('Jet4_Pt', jet4_pt,'Jet4_Pt/D');
        t.Branch('Jet1_dPhiMET', jet1met_dphi,'Jet1_dPhiMET/D');
        t.Branch('Jet2_dPhiMET', jet2met_dphi,'Jet2_dPhiMET/D');
        t.Branch('Jet3_dPhiMET', jet3met_dphi,'Jet3_dPhiMET/D');
        t.Branch('Jet4_dPhiMET', jet4met_dphi,'Jet4_dPhiMET/D');
        t.Branch('Lepton_BTag70Jet_mindR', lepb_mindr,'Lepton_BTag70Jet_mindR/D');
        t.Branch('Lepton_TrimmedJet1_dR', lepfj1_dr,'Lepton_TrimmedJet1_dR/D');
        t.Branch('cutBTag70', cutbtag70,'cutBTag70/I');
        t.Branch('Tauveto', tauveto, 'Tauveto/I');
        t.Branch('TrimmedJet1_Pt', fj1_pt,'TrimmedJet1_Pt/D');
        t.Branch('TrimmedJet1_4VM', fj1_m,'TrimmedJet1_4VM/D');
        t.Branch('TrimmedJet2_dPhiMET', fj2met_dphi,'TrimmedJet2_dPhiMET/D');

        t.Branch('Lepton_BMV1Jet_dR', lepmv1b_dr,'Lepton_BMV1Jet_dR/D');
        t.Branch('tNboost_jets', tnboost_jets,'tNboost_jets/I');
        t.Branch('tNboost_btag', tnboost_btag,'tNboost_btag/I');
        t.Branch('tNboost_jmet', tnboost_jmet,'tNboost_jmet/I');
        t.Branch('tNboost_met', tnboost_met,'tNboost_met/I');
        t.Branch('tNboost_mt', tnboost_mt,'tNboost_mt/I');
        t.Branch('tNboost_amt2', tnboost_amt2,'tNboost_amt2/I');
        t.Branch('tNboost_topness', tnboost_topness,'tNboost_topness/I');
        t.Branch('tNboost_htsig', tnboost_htsig,'tNboost_htsig/I');
        t.Branch('tNboost_fj2met', tnboost_fj2met,'tNboost_fj2met/I');
        t.Branch('tNboost_tauveto', tnboost_tauveto,'tNboost_tauveto/I');
        t.Branch('tNboost_toptag', tnboost_toptag,'tNboost_toptag/I');
        t.Branch('tNboost_lepb', tnboost_lepb,'tNboost_lepb/I');
        t.Branch('tNboost', tnboost,'tNboost/I');


    for i in bkg_train_validate_evaluate:
        f_train_evaluate = ROOT.TFile(file_dir+i+'.root', "read")
        t_train_evaluate = f_train_evaluate.Get('minuit')

        hbook = f_train_evaluate.Get("hbook")
        print hbook.GetBinContent(2)
        sf = Lumi/(float(xsec[i]) * float(hbook.GetBinContent(2)))

        for e in t_train_evaluate:
            sig[0] = 0
            evt_weight[0] = e.EventWeight * sf
            met[0] = e.MET
            mt[0] = e.mTW
            ht[0] = e.HT
            htratio[0] = e.HTratio
            metsig[0] = e.METsig
            htsig[0] = e.HTmissSig
            amt2[0] = e.aMT2
            mt2tau[0] = e.MT2tau
            topness[0] = e.Topness
            jet1_pt[0] = e.Jet1_Pt
            jet2_pt[0] = e.Jet2_Pt
            jet3_pt[0] = e.Jet3_Pt
            jet4_pt[0] = e.Jet4_Pt
            jet1met_dphi[0] = e.Jet1_dPhiMET
            jet2met_dphi[0] = e.Jet2_dPhiMET
            jet3met_dphi[0] = e.Jet3_dPhiMET
            jet4met_dphi[0] = e.Jet4_dPhiMET
            lepb_mindr[0] = e.Lepton_BTag70Jet_mindR
            lepfj1_dr[0] = e.Lepton_TrimmedJet1_dR
            cutbtag70[0] = e.cutBTag70
            tauveto[0] = e.Tauveto
            fj1_pt[0] = e.TrimmedJet1_Pt
            fj1_m[0] = e.TrimmedJet1_4VM
            fj2met_dphi[0] = e.TrimmedJet2_dPhiMET

            lepmv1b_dr[0] = e.Lepton_BMV1Jet_dR
            tnboost_jets[0] = e.tNboost_jets
            tnboost_btag[0] = e.tNboost_btag
            tnboost_jmet[0] = e.tNboost_jmet
            tnboost_met[0] = e.tNboost_met
            tnboost_mt[0] = e.tNboost_mt
            tnboost_amt2[0] = e.tNboost_amt2
            tnboost_topness[0] = e.tNboost_topness
            tnboost_htsig[0] = e.tNboost_htsig
            tnboost_fj2met[0] = e.tNboost_fj2met
            tnboost_tauveto[0] = e.tNboost_tauveto
            tnboost_toptag[0] = e.tNboost_toptag
            tnboost_lepb[0] = e.tNboost_lepb
            tnboost[0] = e.tNboost


            r = randint(1,10)
            if r==1:
                tree_bkg['train'].Fill()
            else:
                tree_bkg['validate'].Fill()

            # use all events to evaluate performace
            tree_bkg['evaluate'].Fill()

        f_train_evaluate.Close()

    f.Write()
    f.Close()



if __name__ == '__main__':
    main()
