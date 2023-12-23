'''
COMP 5970/6970 Graph Algorithms Homework 2 coding section
requires networkx, argparse
requires python 3.6+ (can get with anaconda or elsewhere, note standard python with mac is python 2)
pip install networkx
pip install argparse
'''

import argparse
import networkx as nx
import pickle
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--graph", help="file containing graph in pickle format for problem 1")
args = parser.parse_args()

'''
Problem 1
Implement the disjoint-set / union-find data structure with path compression
'''
class DisjointSet:
    # data structure to back the disjoint set here (you can use an array, a dict, or you could use a graph)

    def __init__(self):
        self.parent_dict = {}

    def makeset(self, x):
        self.parent_dict[x] = x

    def find(self, x):
        if self.parent_dict[x] != x:
            self.parent_dict[x] = self.find(self.parent_dict[x])
            return self.parent_dict[x]
        else:
            return self.parent_dict[x]

    def union(self, x, y):
        if x != y:
            self.parent_dict[y] = x

'''
Problem 2
find the minimum spanning tree of G using your disjoint set data structure above
then draw the graph with the edges in the MST twice as thick as the other edges and save that to mst.png

some code I used to draw the graph
edge_labels = nx.get_edge_attributes(G, "weight") # get edge labels
pos = nx.spring_layout(G) # get position of nodes with a spring model layout
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels)

plt.axis("off")
plt.savefig('graph.png')
'''
def kruskal(G):
    # Elements are tuples in the form (u, v, w) where u and v are nodes of the edge and w is the weight of the edge
    minimum_spanning_tree = nx.Graph()
    graph_edges = []
    disjoint_set = DisjointSet()

    edge_labels = nx.get_edge_attributes(G, "weight")  # get edge labels
    pos = nx.spring_layout(G)  # get position of nodes with a spring model layout
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    for node in G.nodes:
        disjoint_set.makeset(node)

    for u, v in G.edges:
        weight = G.adj[u][v]["weight"]
        graph_edges.append((u, v, weight))

    graph_edges.sort(key=lambda x:x[2])

    for u, v, w in graph_edges:

        parent_u = disjoint_set.find(u)
        parent_v = disjoint_set.find(v)

        if parent_u != parent_v:
            disjoint_set.union(parent_u, parent_v)
            minimum_spanning_tree.add_edge(u, v, weight = w)

    nx.draw_networkx_edges(minimum_spanning_tree, pos, edge_color="red")
    plt.axis("off")
    plt.savefig('mst.png')


# load graphs and run functions

graph = pickle.load(open(args.graph,'rb'))
kruskal(graph)


