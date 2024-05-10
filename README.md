# TreePlot

Package for plotting ladderized tree structures 

Installation:

```
cd TreePlot
pip install . --user
```

Basic Tutorial:

Input: parent vector tree structure representation in the form of a dict, with key=child_label and value=parent_label

Node labels can be integers or strings

```
parent_vector = {1: 0, 2: 4, 3: 2, 4: 1, 5: 3, 6: 7, 7: 8, 8: 5, 9: 6, 10: 1, 11: 1, 12: 11, 13: 10, 14: 9, 15: 10, 16: 9, 17: 9, 18: 12, 19: 13} 

tree = TreePlot(struct=parent_vector)

tree.plot()

tree.save_fig('path/to/output/file.pdf')

```
![image](https://github.com/verammaz/TreePlot/assets/110197814/771834a4-cfb6-4f33-963f-454a8faf7c5f)


Optional Parameters:

TreePlot init
- `orientation` (`str`, default is `h`): orientation of tree plot, horizontal (`h`) or vertical (`v`).
- `node_size` (`float`, default is `0.35`): specify radius of the circle for tree nodes.
- `top_down` (`bool`, default is `True`): specify whether node spacing is computed in parent-->child or child-->parent direction.

plot() method
- `title` (`str`, default is `None`): specify tree plot title.
- `color` (`str`, default is blue `#6495ED`): specify tree node color using hexcode or rgb format.
- `labels` (`bool`, default it `True`): indicate whether to display labels on tree nodes.
- `show` (`bool`, default is `True`): indicate whether to immediately export tree plot to HTML file and load it in browser.

