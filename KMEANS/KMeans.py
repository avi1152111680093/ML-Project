import time
import pandas as pd
from math import pi
from random import randint
from matplotlib import pyplot as plt

class KMeans:
    def __init__(self, max_iter=50, k=2):
        self.k = k
        self.colors = []
        self.centroids = []
        self.cluster_data_x = []
        self.cluster_data_y = []
        self.max_iter = max_iter
        for _ in range(k):
            self.cluster_data_x.append([])
            self.cluster_data_y.append([])
            self.colors.append("#" + str(hex(randint(1048576, 16777215))[2:]))

    def init_centroids(self, X, Y):
        for _ in range(self.k):
            i = randint(0, len(X)-1)
            self.centroids.append([X[i], Y[i]])

    @staticmethod
    def compute_distance(p1x, p1y, p2):
        return (p1x - p2[0]) ** 2 + (p1y - p2[1]) ** 2

    def recompute_centroids(self):
        i = 0
        while i < self.k:
            if len(self.cluster_data_x[i]) == 0:
                self.k -= 1
                self.centroids.pop(i)
                self.cluster_data_x.pop(i)
                self.cluster_data_y.pop(i)
                continue
            self.centroids[i][0] = sum([pt for pt in self.cluster_data_x[i]]) / len(self.cluster_data_x[i])
            self.centroids[i][1] = sum([pt for pt in self.cluster_data_y[i]]) / len(self.cluster_data_y[i])
            i += 1

    def fit(self, X, Y, visualize=False):
        self.init_centroids(X, Y)
        for _ in range(self.max_iter):
            if visualize:
                for i in range(self.k):
                    plt.scatter(self.centroids[i][0], self.centroids[i][1], s=75, c="r", edgecolors="black")
                    plt.scatter(self.cluster_data_x[i], self.cluster_data_y[i], c=self.colors[i])
                    plt.draw()
                plt.pause(0.0001)
                plt.clf()

            for i in range(self.k):
                self.cluster_data_x[i].clear()
                self.cluster_data_y[i].clear()

            for r in range(len(X)):
                min_dist = float("infinity")
                min_index = 0
                for j in range(self.k):
                    distance = self.compute_distance(X[r], Y[r], self.centroids[j])
                    if distance <= min_dist:
                        min_dist = distance
                        min_index = j
                self.cluster_data_x[min_index].append(X[r])
                self.cluster_data_y[min_index].append(Y[r])
            self.recompute_centroids()

    def plot(self):
        plt.clf()
        xAxis, yAxis = [], []
        print("Num of clusters = ", self.k)
        for c in range(self.k):
            xAxis.append([i for i in self.cluster_data_x[c]])
            yAxis.append([i for i in self.cluster_data_y[c]])

        for i in range(self.k):
            plt.scatter(xAxis[i], yAxis[i], c=self.colors[i])
            plt.scatter(self.centroids[i][0], self.centroids[i][1], s=75, c="red", edgecolors="black")
        plt.show()

# region Data
Data = pd.read_csv('./faithful.csv')
x = list(Data["eruptions"])
y = list(Data["waiting"])
x = [18*i for i in x]
# endregion

# region Application
plt.scatter(x, y, s=30, c="white", edgecolors="black")
visualise = True
t1 = time.time()
K = KMeans(max_iter=3, k=2)
K.fit(x, y, visualise)

print("Time required =", time.time() - t1, "sec")

K.plot()
# endregion