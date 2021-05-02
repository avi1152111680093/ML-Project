import time
import pandas as pd
from math import pi
from math import sin
from math import cos
from random import randint
import matplotlib.pyplot as plt

class HierarchicalClustering:
    def __init__(self, k):
        self.k = k
        self.colors = []
        self.clusterDataX = []
        self.clusterDataY = []
        self.distanceMatrix = []

    @staticmethod
    def compute_distance(p1x, p1y, p2x, p2y):
        return (p1x - p2x) ** 2 + (p1y - p2y) ** 2

    def computeDistanceMatrix(self, X, Y):
        for _ in range(len(X)):
            self.distanceMatrix.append([])
        for i in range(len(X)):
            for j in range(len(Y)):
                self.distanceMatrix[i].append(self.compute_distance(X[i], Y[i], X[j], Y[j]))

    def recomputeDistanceMatrix(self, minInx):
        i = minInx[0]
        j = minInx[1]
        for k in range(len(self.distanceMatrix)):
            self.distanceMatrix[k][i] = min(self.distanceMatrix[k][i], self.distanceMatrix[k][j])
            self.distanceMatrix[i][k] = min(self.distanceMatrix[i][k], self.distanceMatrix[j][k])

        self.distanceMatrix.pop(j)
        for k in range(len(self.distanceMatrix)):
            self.distanceMatrix[k].pop(j)

    def findMin(self, mat):
        mini = [float("infinity"), 0, 0]                    # min, r, c
        for r in range(1, len(mat)):
            for c in range(0, r):
                dist = self.distanceMatrix[r][c]
                if dist < mini[0]:
                    mini[0] = dist
                    if r < c:
                        mini[1], mini[2] = r, c
                    else:
                        mini[1], mini[2] = c, r
        return mini

    def fit(self, X, Y, visualize=False):
        self.computeDistanceMatrix(X, Y)
        for i in range(len(X)):
            color = "#" + str(hex(randint(1048576, 16777215))[2:])
            self.colors.append(color)

            self.clusterDataX.append([X[i]])
            self.clusterDataY.append([Y[i]])

        while len(self.clusterDataX) > self.k:
            minimum = self.findMin(self.distanceMatrix)

            if len(self.clusterDataX[minimum[1]]) < len(self.clusterDataX[minimum[2]]):
                self.colors[minimum[1]] = self.colors[minimum[2]]

            self.colors.pop(minimum[2])
            self.clusterDataX[minimum[1]] += self.clusterDataX.pop(minimum[2])
            self.clusterDataY[minimum[1]] += self.clusterDataY.pop(minimum[2])

            if visualize:
                plt.clf()
                for i in range(len(self.clusterDataX)):
                    plt.scatter(self.clusterDataX[i], self.clusterDataY[i], c=self.colors[i])
                plt.pause(0.00001)

            self.recomputeDistanceMatrix(minimum[1:])

    def plot(self):
        print("Number of cluster =", self.k)
        for i in range(len(self.clusterDataX)):
            plt.scatter(self.clusterDataX[i], self.clusterDataY[i], c=self.colors[i])
        plt.show()

# region Data
dummyData = True
if dummyData:
    r1 = 50
    n1 = 20
    x1 = [r1*cos(i * 2 * pi / n1) for i in range(n1)]
    y1 = [r1*sin(i * 2 * pi / n1) for i in range(n1)]

    r2 = 100
    n2 = 20
    x2 = [r2*cos(i * 2 * pi / n2) for i in range(n2)]
    y2 = [r2*sin(i * 2 * pi / n2) for i in range(n2)]

    a3 = 1
    n3 = 20
    offX3 = -500
    offY3 = -200
    x3 = [a3*i**2+offX3 for i in range(-n3, n3)]
    y3 = [2*a3*i+offY3 for i in range(-n3, n3)]

    a4 = 1
    n4 = 20
    offX4 = -150
    offY4 = -100
    x4 = [-a4*i**2+offX4 for i in range(-n4, n4)]
    y4 = [2*a4*i+offY4 for i in range(-n4, n4)]

    x = x1 + x2 + x3 + x4
    y = y1 + y2 + y3 + y4
else:
    Data = pd.read_csv('./faithful.csv')
    x = list(Data["eruptions"])
    y = list(Data["waiting"])
    x = [18*i for i in x]
# endregion

# region Application
plt.scatter(x, y, s=30, c="white", edgecolors="black")
plt.pause(0.001)

visualise = True
t1 = time.time()
C = HierarchicalClustering(k=4)
C.fit(x, y, visualise)
print("Time required =", time.time() - t1, "sec")

C.plot()
# endregion