from treeplot.Tree import Tree
import plotly.graph_objects as go
import plotly.io as pio

import math

class TreePlot():

    def __init__(self, struct, node_rad=0.35, orientation='h', top_down=True):

        self.tree = Tree(struct)
        self.node_size = node_rad
        self.orient = orientation

        self.fig = go.Figure()

        self.edges = list()
        for nid, node in self.tree.nid2node.items():
            self.edges.append((nid, node.pid))

        self.set_depths_of_nodes()

        if top_down:
            self.set_ys_topdown()
        else:
            self.set_ys_bottomup()

        self.pos = dict()
        if orientation == 'h':
            for nid, node in self.tree.nid2node.items():
                self.pos[nid] = (self.tree.nid2depth[nid], node.y)
        else:
            for nid, node in self.tree.nid2node.items():
                self.pos[nid] = (node.y, -self.tree.nid2depth[nid])



    def set_ys_bottomup(self):
        for leaf in self.tree.leaves:
            leaf.set_y(float(self.tree.leaf2ord[leaf.id] * self.node_size * 3))
        for node in self.tree.postorder_traversal():
            parent = node.parent
            y = 0
            for child in parent.children:
                y += child.y
            y /= len(parent.children)
            parent.set_y(float(y))


    def get_space_for_child(self, child):
        to_visit = [child]
        res = 0
        while len(to_visit) > 0:
            curr_node = to_visit.pop()
            if curr_node.is_leaf():
                res += 1
            for child in curr_node.children:
                to_visit.append(child)
        return res
    

    def set_ys_topdown(self):
        for node in self.tree.bfs_traversal():
            if node == self.tree.root:
                node.set_y(float(0))
            D = 0
            for child in node.children:
                d = self.get_space_for_child(child)
                if d >= D:
                    D = d

            D = D 
            N = len(node.children)

            prev = node.y - ((D * (N-1)) / 2)
            for child in node.children_ordered:
                child.set_y(prev)
                prev += D

            """if N % 2 == 0:
                i = 1
                for child in node.children_ordered:
                    if i % 2 == 0:
                        child.set_y(node.y - ((D * (i//2))/2))
                    else:
                        child.set_y(node.y + ((D * (i//2 + 1))/2))
                    i += 1
        
            else:
                i = 0
                for child in node.children_ordered:
                    if i == 0:
                        child.set_y(node.y)
                    elif i%2 == 0:
                        child.set_y(node.y + (D * (i//2)))
                    else:
                        child.set_y(node.y - (D * (i//2 + 1)))
                    i += 1"""


    
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
        
        #TODO: implement arrows option for tree plot
        
        self.fig.add_trace(go.Scatter())

        for node in self.tree.nid2node.values():
            self.fig.add_shape(type='circle', xref='x', yref='y', x0=self.pos[node.id][0]-self.node_size, y0=self.pos[node.id][1]-self.node_size,
                               x1=self.pos[node.id][0]+self.node_size, y1=self.pos[node.id][1]+self.node_size, fillcolor=color)
            if labels:
                self.fig.add_annotation(dict(text=str(node.id), x=self.pos[node.id][0], y=self.pos[node.id][1], xref='x', yref='y',
                                        font=dict(color='#FFFFFF', size=12), showarrow=False))
            if node.is_root():
                continue
            
            theta = 0
            x_off, y_off = 0, 0
            if self.orient == 'h':
                theta = math.atan(abs((self.pos[node.id][1]-self.pos[node.pid][1]) / (self.pos[node.id][0]-self.pos[node.pid][0])))
                x_off = -self.node_size*math.cos(theta)
                y_off = -self.node_size*math.sin(theta) if self.pos[node.pid][1]<self.pos[node.id][1] else self.node_size*math.sin(theta)
            else:
                theta = math.atan(abs((self.pos[node.id][0]-self.pos[node.pid][0]) / (self.pos[node.id][1]-self.pos[node.pid][1])))
                x_off = -self.node_size*math.sin(theta) if self.pos[node.pid][0]<self.pos[node.id][0] else self.node_size*math.sin(theta)
                y_off = self.node_size*math.cos(theta)
            
            self.fig.add_annotation(dict(
                x=self.pos[node.id][0]+x_off, y=self.pos[node.id][1]+y_off,
                ax=self.pos[node.pid][0]-x_off, ay=self.pos[node.pid][1]-y_off,
                xref="x", yref="y", text="", axref="x", ayref="y",
                arrowhead=4 if arrows else None, arrowwidth=3, arrowcolor='black', arrowsize=1, arrowside='end'))
     

        self.fig.update_layout(title=title, xaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=False), 
                                yaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=False))
        
        fig_width = abs(min([self.pos[node.id][0] for node in self.tree.nid2node.values()]) - max([self.pos[node.id][0] for node in self.tree.nid2node.values()]))
        fig_height = abs(min([self.pos[node.id][1] for node in self.tree.nid2node.values()]) - max([self.pos[node.id][1] for node in self.tree.nid2node.values()]))
        
        self.fig.update_layout(width=fig_width*100, height=fig_height*100, autosize=True, plot_bgcolor="white")
        
        if show:
            self.fig.show()


    def save_fig(self, outpath):
        pio.write_image(self.fig, outpath)
