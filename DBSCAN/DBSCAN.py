import time
import pandas as pd
from math import pi
from math import sin
from math import cos
from random import randint
import matplotlib.pyplot as plt

class DBSCAN:
    def __init__(self, epsilon, minPts):
        self.epsilon = epsilon
        self.minPts = minPts
        self.clusters_x = []
        self.clusters_y = []
        self.colors = []

    def fit(self, X, Y, visualize=False):
        while len(X) > 0:
            temp_cluster_x = [X.pop(0)]
            temp_cluster_y = [Y.pop(0)]
            color = "#" + str(hex(randint(1048576, 16777215))[2:])
            k = 0

            if visualize:
                plt.cla()
                plt.scatter(bx, by, s=30, c="white", edgecolors="black")
                plt.scatter(temp_cluster_x, temp_cluster_y, c=color)
                for i in range(len(self.clusters_x)):
                    plt.scatter(self.clusters_x[i], self.clusters_y[i], c=self.colors[i])

            while k < len(temp_cluster_x):
                tx, ty = temp_cluster_x[k], temp_cluster_y[k]
                j = 0

                if visualize:
                    draw_circle = plt.Circle((tx, ty), self.epsilon, facecolor="None", edgecolor="red")
                    axes.add_artist(draw_circle)
                    plt.pause(0.0001)

                while j < len(X):
                    dist = (tx-X[j])**2 + (ty-Y[j])**2
                    if dist <= self.epsilon**2:
                        if visualize:
                            plt.scatter(X[j], Y[j], c=color)
                        temp_cluster_x.append(X[j])
                        temp_cluster_y.append(Y[j])
                        X.pop(j)
                        Y.pop(j)
                        j -= 1
                    j += 1
                k += 1

            if len(temp_cluster_x) >= self.minPts:
                self.clusters_x.append(temp_cluster_x)
                self.clusters_y.append(temp_cluster_y)
                self.colors.append(color)

    def plot(self):
        plt.clf()
        plt.scatter(bx, by, s=30, c="white", edgecolors="black")

        if len(self.clusters_x) == 0:
            print("No cluster formed!")
            plt.show()
            return

        print("Number of cluster formed =", len(self.clusters_x))
        for i in range(len(self.clusters_x)):
            Xs = [c for c in self.clusters_x[i]]
            Ys = [c for c in self.clusters_y[i]]
            plt.scatter(Xs, Ys, c=self.colors[i])
        plt.show()

# region Data
dummyData = True
if dummyData:
    r1 = 50
    n1 = 50
    x1 = [r1*cos(i * 2 * pi / n1) for i in range(n1)]
    y1 = [r1*sin(i * 2 * pi / n1) for i in range(n1)]

    r2 = 100
    n2 = 50
    x2 = [r2*cos(i * 2 * pi / n2) for i in range(n2)]
    y2 = [r2*sin(i * 2 * pi / n2) for i in range(n2)]

    a3 = 1
    n3 = 50
    offX3 = -500
    offY3 = -200
    x3 = [a3*i**2/10+offX3 for i in range(-n3, n3)]
    y3 = [2*a3*i+offY3 for i in range(-n3, n3)]

    a4 = 1
    n4 = 50
    offX4 = -150
    offY4 = -100
    x4 = [-a4*i**2/10+offX4 for i in range(-n4, n4)]
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
bx = [b for b in x]
by = [b for b in y]

figure, axes = plt.subplots()

visualise = True
t1 = time.time()
D = DBSCAN(13, 5)
D.fit(x, y, visualise)
print("Time required =", time.time() - t1, "sec")

D.plot()
# endregion

