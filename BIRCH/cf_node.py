from math import sqrt
import numpy as np
from copy import copy

# Various Types of A CF Node
class CFType:
    UNDEFINED = 0
    LEAF_NODE = 1
    NON_LEAF_NODE = 2

# Returns the Linear Sum of Data Points
def linear_sum (dp):
    # dp --> List of the data points
    ls = []
    for i in range(len(dp[0])):
        sum = 0
        for j in range(len(dp)):
            sum += dp[j][i]
        ls.append(sum)
    return ls

# Returns the Square Sum of Data Points
def square_sum (dp):
    # dp --> List of the data points
    ss = 0
    for i in range(len(dp)):
        for j in range(len(dp[0])):
            ss += dp[i][j]**2
    return ss

# Returns Manhattan Distance between two CFs
def manhattan_distance (cf1, cf2):
    dis=0
    for i in range(len(cf1)):
        dis += abs(cf1[i]-cf2[i])
    return dis

# Cluster Feature
class CF:
    def __init__(self, N, LS, SS):
        self.N = N
        self.LS = LS
        self.SS = SS

        self.centroid = None
        self.radius = None
        self.diameter = None

    def __add__(self, new_cf):
        return CF(self.N+new_cf.N, self.LS+new_cf.LS, self.SS+new_cf.SS)

    def get_centroid (self):
        if (self.centroid != None):
            return self.centroid
        self.centroid = []
        for i in range(len(self.LS)):
            self.centroid.append (self.LS[i]/self.N)
        return self.centroid

    def get_radius (self):
        if (self.radius != None):
            return self.radius
        centroid = self.get_centroid()
        self.radius = sqrt((self.N*np.dot(centroid,centroid) + self.SS - 2*np.dot(centroid,self.LS))/self.N)
        return self.radius

    def get_diameter (self):
        if (self.diameter != None):
            return self.diameter
        self.diameter = sqrt((2*self.N*self.SS - 2*np.dot(self.LS,self.LS))/(self.N*(self.N-1)))
        return self.diameter

    def get_distance(self, cf):
        return manhattan_distance (self.centroid, cf.centroid)

# CF Node
class CFNode:
    def __init__(self, cf, parent):
        self.cf = copy(cf)
        self.parent = parent
        self.type_node = CFType.UNDEFINED

    def get_distance (self, cf_node):
        return self.cf.get_distance (cf_node.cf)

# dp = [[1,2,3],[5,6,7],[3,0,1]]
# cf = CF (3, linear_sum(dp), square_sum(dp))
# c = CFNode (cf, None)