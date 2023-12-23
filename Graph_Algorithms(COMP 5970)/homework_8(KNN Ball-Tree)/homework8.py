'''
COMP 5970/6970 Graph Algorithms Homework 8 coding section
requires networkx, argparse
requires python 3.6+ (can get with anaconda or elsewhere, note standard python with mac is python 2)
pip install networkx
pip install argparse
'''

import argparse
import heapq
import math

import networkx as nx
import pickle
import matplotlib.pyplot as plt
import numpy as np
from plotnine import *
from networkx.algorithms import bipartite
import random
import queue
import statistics
import pydot


parser = argparse.ArgumentParser()
args = parser.parse_args() # no arguments but im leaving this here

'''
Problem 1
Implement a ball-tree datastructure for fast knn_search
The data has just 2 dimensions, each row is a datapoint
'''


def euclidean_distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))


class BallTree:
    def __init__(self, data):
        self.center = []
        self.radius = 0
        self.data = data
        self.left = None
        self.right = None

        self.create_ball_tree()

    def create_ball_tree(self):

        if len(self.data) == 1:
            self.center = self.data[0]
            self.radius = 0

        else:
            x_coordinates = [x for x, y in self.data]
            y_coordinates = [y for x, y in self.data]

            range_x = max(x_coordinates) - min(x_coordinates)
            range_y = max(y_coordinates) - min(y_coordinates)

            median = 0
            large_dimension = 0

            if range_x > range_y:
                median = statistics.median(x_coordinates)
            else:
                median = statistics.median(y_coordinates)
                large_dimension = 1

            L, R = [], []

            for x, y in self.data:
                if large_dimension == 0:
                    if x <= median:
                        L.append((x, y))
                    else:
                        R.append((x, y))
                else:
                    if y <= median:
                        L.append((x, y))
                    else:
                        R.append((x, y))

            average_x = sum(x_coordinates) / len(x_coordinates)
            average_y = sum(y_coordinates) / len(y_coordinates)

            self.center = ((average_x, average_y))

            for point in self.data:

                distance = euclidean_distance(point, self.center)

                if distance > self.radius:
                    self.radius = distance

            self.left = BallTree(L)
            self.right = BallTree(R)




'''
Problem 2 
implement knn_search on a balltree for a target point t and returning the k closest points
'''
def knn_search(B, d, k):
    max_heap = []
    heapq.heapify(max_heap)
    heapq.heappush(max_heap, (float("-inf"), (float("inf"), float("inf"))))

    def knn_helper(current_B, k):
        if len(max_heap) == k and euclidean_distance(d, current_B.center) - current_B.radius > (-1 * max_heap[0][0]):
            return

        elif len(current_B.data) == 1:
            distance = euclidean_distance(d, current_B.center)

            if distance < (-1 * max_heap[0][0]):
                heapq.heappush(max_heap, ((-1 * distance), current_B.data[0]))
                if len(max_heap) > k:
                    heapq.heappop(max_heap)

        else:
            left_child_distance = euclidean_distance(d, current_B.left.center) - current_B.left.radius
            right_child_distance = euclidean_distance(d, current_B.right.center) - current_B.right.radius

            if left_child_distance < right_child_distance:
                knn_helper(current_B.left, k)
                knn_helper(current_B.right, k)
            else:
                knn_helper(current_B.right, k)
                knn_helper(current_B.left, k)

    knn_helper(B, k)

    return [y for x, y in max_heap]

'''
Problem 3
create a knn graph and output to a dot file
and visualize this in Gephi with force-atlas-2 or some other layout if you prefer
if you use the queue.PriorityQueue, you will want a class to store the priority and the data point
this will look like 
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
'''
def create_knn_graph(B, data, k):
    # for each data point, find its k nearest neighbors and make edges in a graph to them
    # you will use your knn_search function to do this
    # you will need a max heap and can either use your code from a previous
    # homework or the queue.PriorityQueue (but this is min-heap so make sure to 
    # use the negative of the distance to make it a max heap)

    G = nx.Graph()

    for point in data:

        point = tuple(point)
        nearest_neighbors = knn_search(B, point, k)

        for neighbor in nearest_neighbors:
            if neighbor == point:
                continue

            G.add_edge(point, neighbor)

    nx.drawing.nx_pydot.write_dot(G, "KNN_Graph.dot")
    nx.write_gexf(G, "KNN_Graph.gexf")

data = np.loadtxt("data.csv",delimiter=",")
tree = BallTree(data)

create_knn_graph(tree, data, 10)
