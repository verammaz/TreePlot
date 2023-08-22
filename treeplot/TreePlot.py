from treeplot.Tree import Tree
import plotly.graph_objects as go
import plotly.io as pio

class TreePlot():

    def __init__(self, struct, node_size=60, orientation='h'):

        self.tree = Tree(struct)
        self.node_size = node_size
        self.orient = orientation

        self.fig = go.Figure()

        self.edges = list()
        for nid, node in self.tree.nid2node.items():
            self.edges.append((nid, node.pid))

        self.set_depths_of_nodes()
        self.set_ys_of_nodes()

        self.pos = dict()
        if orientation == 'h':
            for nid, node in self.tree.nid2node.items():
                self.pos[nid] = (self.tree.nid2depth[nid], node.y)
        else:
            for nid, node in self.tree.nid2node.items():
                self.pos[nid] = (node.y, -self.tree.nid2depth[nid])



    def set_ys_of_nodes(self):
        for leaf in self.tree.leaves:
            leaf.set_y(float(self.tree.leaf2ord[leaf.id] * self.node_size))
        for node in self.tree.postorder_traversal():
            parent = node.parent
            y = 0
            for child in parent.children:
                y += child.y
            y /= len(parent.children)
            parent.set_y(float(y))

    
    def set_depths_of_nodes(self):
        for nid, node in self.tree.nid2node.items():
            if nid == self.tree.root.id:
                self.tree.nid2depth[nid] = 0
                continue
            d = 1
            pid = node.pid
            while pid != self.tree.root.id:
                d += 1
                pid = self.tree.parents[pid]
            self.tree.nid2depth[nid] = d
        
    
    def plot(self, color='#6495ED', labels=True, title=None, show=True, arrows=False):

        Xe, Ye = [], []

        for edge in self.edges:
            Xe += [self.pos[edge[0]][0], self.pos[edge[1]][0], None]
            Ye += [self.pos[edge[0]][1], self.pos[edge[1]][1], None]
        
        self.fig.add_trace(go.Scatter(x=Xe, y=Ye, mode="lines+markers",
        marker=dict(
            symbol="arrow",
            size=15,
            angleref="previous",
        ),line=dict(color='#1D2339', width=3), 
                                 hoverinfo='none', showlegend=False))
            
        self.fig.add_trace(go.Scatter(x=[self.pos[nid][0] for nid, node in self.tree.nid2node.items()], 
                                 y=[self.pos[nid][1] for nid, node in self.tree.nid2node.items()], 
                                 mode='markers', 
                                 marker=dict(symbol='circle', size=self.node_size, color=color,
                                 line=dict(color='#1D2339', width=1)), 
                                 hoverinfo='none', showlegend=False))

        self.fig.update_layout(title=title, xaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=False), 
                                yaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=False))
        
        if labels:
            self.add_labels()

        if show:
            self.fig.show()


    def add_labels(self):
        annotations = list()
        for nid in self.tree.nid2node.keys():
            annotations.append(
                dict(text=str(nid), x=self.pos[nid][0], y=self.pos[nid][1], xref='x', yref='y',
                font=dict(color='#FFFFFF', size=12), showarrow=False))
        self.fig.update_layout(annotations=annotations)
    

    def save_fig(self, outpath):
        pio.write_image(self.fig, outpath)
