from cf_node import *

class LeafNode(CFNode):
    def __init__(self, cf, parent, clusters):
        super().__init__(cf, parent)
        self.node_type = CFType.LEAF_NODE
        self.clusters = clusters

    def append_leaf_node (self, cf):
        self.cf += cf
        self.clusters.append(cf)

    def merge_leaf_node (self, node):
        self.cf += node.cf
        for cluster in node.clusters:
            self.clusters.append(cluster)
    
    def get_farthest_clusters (self):
        TODO