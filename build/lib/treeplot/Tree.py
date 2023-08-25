from treeplot.Node import Node

class Tree():

    def __init__(self, parents):

        """
        Params 
        ---------
        
        parents : dict
            specifies tree structure by identifying parent of each node in tree
            dict should have key = node id, value = node parent id
        
        format : str
            specifies type of node ids
        
        """
        

        self.parents = parents
        self.n = len(parents) + 1

        self.root = None
        self.nid2node = dict()
        self.nid2depth = dict()
        self.leaves = list()
        self.leaf2ord = dict() # applicable only if want to ladderize tree 

        self.__init_nodes()
        
        self.__init_node_infos()
        
        self.ladderize()


    def __init_nodes(self):

        rid = self.get_root_id()
        self.root = Node(id=rid, pid=rid)
        self.nid2node = {nid: Node(id=nid, pid=self.parents[nid]) for nid in self.parents.keys()}
        self.nid2node[rid] = self.root
    

    def get_root_id(self):
        rid = None
        for nid, pid in self.parents.items():
            if pid not in self.parents.keys():
                rid = pid
                break
        return rid

    def __init_node_infos(self):

        for nid in self.nid2node.keys():
            d = 0
            if nid == self.root.id:
                self.nid2depth[nid] = 0
                continue
            parent = self.parents[nid]
            while parent != self.root.id:
                d += 1
                parent = self.parents[parent]
            self.nid2depth[nid] = d

        for nid in self.nid2node.keys():
            if nid == self.root.id:
                self.nid2node[nid].set_pid(nid)
                self.nid2node[nid].set_parent(self.root)
                self.nid2node[nid].set_depth(0)
            else:
                self.nid2node[nid].set_pid(self.parents[nid])
                self.nid2node[nid].set_depth(self.nid2depth[nid])
        
        for node in self.nid2node.values():
            node.set_parent(self.nid2node[node.pid])
            parent = self.nid2node[node.pid]
            if parent != node:
                parent.add_child(node)
        
        for node in self.nid2node.values():
            node.set_subtree_height()
    

    def ladderize(self):
        for node in self.nid2node.values():
            node.children_ordered1 = sorted(node.children, key=lambda x: x.subtree_h, reverse=True)
            node.children_ordered = sorted(node.children, key=lambda x: x.subtree_h, reverse=True)
            #node.children.sort(key=lambda x: x.subtree_h, reverse=True)
            if len(node.children) == 0:
                self.leaves.append(node)
        self.order_leaves()

    
    def order_leaves(self):
        done = False
        d = -1
        curr_node = self.root
        while not done:
            d += 1
            while not curr_node in self.leaves and curr_node.children_ordered1:
                curr_node = curr_node.children_ordered1.pop(0)
            if curr_node in self.leaves:
                self.leaf2ord[curr_node.id] = d
            else:
                d -= 1
            if curr_node.is_root():
                done = True
            else:
                curr_node = curr_node.parent


    def postorder_traversal(self):
        result = []
        to_visit = [self.root]
        while len(to_visit) > 0:
            curr_node = to_visit.pop()
            result.append(curr_node)
            for child in curr_node.children:
                to_visit.append(child)
        return result[::-1]


    def bfs_traversal(self):
        result = []
        to_visit = [self.root]
        while len(to_visit) > 0:
            curr_node = to_visit.pop(0)
            result.append(curr_node)
            for child in curr_node.children:
                to_visit.append(child)
        return result