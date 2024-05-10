from treeplot.TreePlot import TreePlot
from treeplot.Tree import Tree

import numpy as np

p1 = {1:0, 2:1, 3:1, 4:1, 5:4, 6:4}

data = np.load('/Users/veramazeeva/MtSinai/Data_met_fs_corrected/PairtreeOutputs/pairtree/PAM42/PAM42_results.npz')
parent_vec = data['struct'][0]

p2 = dict()
for i in range(len(parent_vec)):
    p2[i+1] = parent_vec[i]


#tree = Tree(parents=p1)

#for node in tree.nid2node.values():
    #print(node.children_ordered)


treeplot = TreePlot(p2, orientation='h', top_down=False)
print(treeplot.pos)
treeplot.plot(show=True, arrows=True)
treeplot.save_fig('test_tree.png')


