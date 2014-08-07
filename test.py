import ROOT
import rootpy
import root_numpy

#import client as apy
import agilepy as apy

net = apy.NeuralNetwork()
net.load('test.yaml')
T = apy.root.tree_reader('/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140727_DL/merge.root')
T.get_tree('evaluate')
T.get_array(branches = net.branches)
X = T.to_array()
#print X
predictions = net.predict(X)
print predictions
