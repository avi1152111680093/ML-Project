from BIRCH.cf_node import CFNode
from cf_node import *

class NonLeafNode(CFNode):
    def __init__(self, cf, parent):
        super().__init__(cf, parent)
        