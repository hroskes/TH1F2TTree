No promises, but this worked for my case.
It's for converting an EDAnalyzer that makes a bunch of histograms into one that makes a tree.

python TH1F2TTree.py /.../CMSSW_.../src/.../.../plugins/myEDanalyzer.cc

Output is in /.../CMSSW_.../src/.../.../plugins/myEDanalyzer_tree.cc
(Or provide an output file as a second command line argument)
