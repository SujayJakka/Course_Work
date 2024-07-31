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
args = parser.parse_args() # no arguments but im leaving this here

'''
Problem 1
Implement topological sort on the nodes of the graph G
'''
def topological_sort(G):
    visited = set()
    topological_order_stack = []

    def dfs(u):

        for u, v in G.edges(u):
            if v not in visited:
                dfs(v)

        visited.add(u)
        topological_order_stack.append(u)


    for u in G.nodes:
        if u not in visited:
            dfs(u)

    return topological_order_stack


'''
Problem 2
Find the longest path in the directed acyclic graph
output the labels of the traversed edges and the alignment they imply
(edges are labeled with tuples, build up 2 strings from these and output on separate lines)
(example if i had path with edge labels (-,G),(A,A) then I want the following output
-A
GA
'''
def longest_path(G):

    topological_order_stack = topological_sort(G)
    distance_dict = {}
    parent_dict = {}

    distance_dict[topological_order_stack[-1]] = 0
    parent_dict[topological_order_stack[-1]] = None

    for i in range(len(topological_order_stack) - 2, -1, -1):

        v = topological_order_stack[i]

        distance_dict[v] = float("-inf")
        parent_dict[v] = None

        for u, v in G.in_edges(v):

            if distance_dict[u] + G[u][v]["weight"] > distance_dict[v]:
                distance_dict[v] = distance_dict[u] + G[u][v]["weight"]
                parent_dict[v] = u

    v = topological_order_stack[0]

    sequence_1 = ""
    sequence_2 = ""

    while parent_dict[v] is not None:
        parent_of_v = parent_dict[v]
        edge_label = G[parent_of_v][v]["label"]

        sequence_1 = edge_label[0] + sequence_1
        sequence_2 = edge_label[1] + sequence_2

        v = parent_of_v

    print(sequence_1)
    print(sequence_2)


# make graph and run functions

s1 = "GTCGTAGAATA"
s2 = "GTAGTAGATA"
G = nx.DiGraph()
for i in range(len(s1)+1):
    for j in range(len(s2)+1):
        G.add_node((i,j))
print(G.nodes)
print(len(G.nodes))

for i in range(1,len(s1)+1):
    G.add_edge((i-1,0),(i,0), weight=-1, label=(s1[i-1],"-"))
for j in range(1,len(s2)+1):
    G.add_edge((0,j-1),(0,j), weight=-1, label=("-",s2[j-1]))

for i in range(1,len(s1)+1):
    for j in range(1,len(s2)+1):
        # add 3 edges, one from left, one from up, and one from diagonal up left
        G.add_edge((i-1,j),(i,j),weight=-1,label=(s1[i-1],"-"))
        G.add_edge((i,j-1),(i,j),weight=-1,label=("-",s2[j-1]))
        score = -1
        if s1[i-1] == s2[j-1]:
            score = 1
        G.add_edge((i-1,j-1),(i,j),weight=score, label=(s1[i-1],s2[j-1]))


print(len(G.edges))
longest_path(G)
