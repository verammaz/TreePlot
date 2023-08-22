from TreePlot import TreePlot

p1 = {1:0, 2:1, 3:1, 4:1, 5:4, 6:4}

tree = Tree(parents=p1)
print(tree.nid2node)

treeplot = TreePlot(p1, orientation='v')
treeplot.plot(title='Hello World')
treeplot.save_fig('test_tree.pdf')
