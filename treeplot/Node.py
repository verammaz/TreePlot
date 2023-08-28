class Node():
    """
        Node object stores item and references to its children. 
        Parent not may have any number of children, but each child has only one parent."
    """

    def __init__(self, id=None, pid=None):
        """
        Params
        ---------
        id : int or str
            clone id to be displayed on node
        depth : int
            distance from root, used as x-coord when plotting node within tree graph
        """

        self.id = id
        self.parent = None
        self.pid = pid
        self.children = list()
        self.children_ordered = list() 
        self.children_ordered1 = list() #used for tree ladderization
        self.depth = 0 
        self.y = 0 # to be computed later
        self.subtree_h = 0
    

    def __repr__(self):
        return "<Node id={0}, pid={1}>".format(self.id, self.pid)
    
    def __eq__(self, other):
        return (self.id == other.id)
    
    def __lt__(self, other):
        return (self.depth < other.depth)
    
    def __hash__(self):
        return hash(str(self.id))
    

    def set_depth(self, d):
        self.depth = d

    def set_subtree_height(self):
        if self.is_leaf():
            self.subtree_h = 0
        else:
            max_depth = -1
            to_visit = [self]
            while to_visit:
                curr_node = to_visit.pop()
                if curr_node.depth > max_depth:
                    max_depth = curr_node.depth
                for child in curr_node.children:
                    to_visit.append(child)
            self.subtree_h = (max_depth - self.depth)
    
    def add_child(self, node):
        self.children.append(node)
    
    def add_children(self, children=[]):
        for child in children:
            self.add_child(child)
    
    def set_parent(self, parent):
        self.parent = parent

    def set_pid(self, pid):
        self.pid = pid
          
    def set_y(self, y):
        self.y = y

    def is_leaf(self):
        return len(self.children) == 0
    
    def is_root(self):
        return self.id == self.parent.id
