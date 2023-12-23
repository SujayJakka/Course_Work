'''
COMP 5970/6970 Graph Algorithms Homework 4 coding section
requires networkx, argparse
requires python 3.6+ (can get with anaconda or elsewhere, note standard python with mac is python 2)
pip install networkx
pip install argparse
'''

import argparse
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import numpy as np
from plotnine import *
import pandas as pd
from networkx.algorithms import bipartite
import random
from collections import deque

parser = argparse.ArgumentParser()
args = parser.parse_args() # no arguments but im leaving this here

'''
Problem 1
Implement maximum cardinality matching given a bipartite graph.
Feel free to use either Hopcraft-Karp or Edmonds-Karp
The nodes will have an attribute "bipartite" with values 0 or 1 
Output a picture of the graph with edges in the matching in a different color
Use the bipartite_layout to draw it.
'''
def maximum_matching(G):

    M = set()
    unmatched_nodes = set()

    for node in G.nodes:
        unmatched_nodes.add(node)

    def alternating_level_graph_function():

        visited = set()
        queue = deque()
        in_queue = set()

        alternating_level_graph = nx.Graph()

        for node in unmatched_nodes:
            if G.nodes[node]["bipartite"] == 0:
                visited.add(node)
                queue.append(node)
                in_queue.add(node)
                alternating_level_graph.add_node(node)

        unmatched_node_found = False
        need_unmatched_edges = True

        while len(queue) != 0:

            for i in range(len(queue)):

                u = queue.popleft()
                in_queue.remove(u)

                for u, v in G.edges(u):

                    if (u, v) not in M and (v, u) not in M and need_unmatched_edges:

                        if v not in visited or v in in_queue:

                            if v in unmatched_nodes:
                                unmatched_node_found = True

                            if v not in in_queue:
                                queue.append(v)
                                in_queue.add(v)
                                visited.add(v)
                                alternating_level_graph.add_node(v)

                            alternating_level_graph.add_edge(u, v)

                    elif ((u, v) in M or (v, u) in M) and need_unmatched_edges == False:

                        if v not in visited or v in in_queue:

                            if v not in in_queue:
                                queue.append(v)
                                in_queue.add(v)
                                visited.add(v)
                                alternating_level_graph.add_node(v)

                            alternating_level_graph.add_edge(u, v)

            if unmatched_node_found:
                break

            if need_unmatched_edges == True:
                need_unmatched_edges = False
            else:
                need_unmatched_edges = True

        leaf_nodes = []

        for node in queue:
            leaf_nodes.append(node)

        return leaf_nodes, alternating_level_graph

    def augmenting_path(leaf_nodes, alternating_level_graph):
        visited = set()
        edges = []

        def DFS(u, need_unmatched_edges):
            visited.add(u)
            for u, v in alternating_level_graph.edges(u):
                if v not in visited:
                    if ((u, v) not in M and (v, u) not in M) and (need_unmatched_edges == True):
                        edges.append((u, v))
                        if G.nodes[v]["bipartite"] == 0 and v in unmatched_nodes:
                            visited.add(v)
                            break
                        DFS(v, False)
                        break

                    elif ((u, v) in M or (v, u) in M) and (need_unmatched_edges == False):
                        edges.append((u, v))
                        DFS(v, True)
                        break

        for u in leaf_nodes:
            if u not in visited:
                DFS(u, True)

        return edges


    while True:
        leaf_nodes, alternating_level_graph = alternating_level_graph_function()
        P = augmenting_path(leaf_nodes, alternating_level_graph)

        for u, v in P:

            if (u, v) not in M and (v, u) not in M:
                M.add((u, v))

                if u in unmatched_nodes:
                    unmatched_nodes.remove(u)

                if v in unmatched_nodes:
                    unmatched_nodes.remove(v)

            else:
                if (u, v) in M:
                    M.remove((u, v))
                else:
                    M.remove((v, u))

                unmatched_nodes.add(u)
                unmatched_nodes.add(v)

        if len(P) == 0:
            break


    matching_graph = nx.Graph()
    nodes_partition_1 = set()

    for node in G.nodes:
        matching_graph.add_node(node)
        if G.nodes[node]["bipartite"] == 0:
            nodes_partition_1.add(node)

    for u, v in M:
        matching_graph.add_edge(u, v)


    pos = nx.bipartite_layout(G, nodes_partition_1)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(matching_graph, pos, edge_color="red")

    plt.axis("off")
    plt.savefig('graph.png')

    print("Edges in Matching")
    print(M)

'''
Problems 2 and 3
Implement Karger's min-cut algorithm
Note: the input is a multi-graph
On each input graph, run 200 iterations of Kargers, report the minimum cut size, and plot a distribution of cut sizes across iterations
I suggest using plotnine for this, a python implementation of ggplot 
'''
def Kargers(G):

    min_cut = float("infinity")
    cut_array = []
    nodes_component_1 = None
    nodes_component_2 = None

    for i in range(200):

        new_nodes = -1
        G_prime = G.copy()
        node_dict = {}
        edges = []

        for node in G_prime.nodes:
            node_dict[node] = [node]

        for edge in G_prime.edges:
            edges.append(edge)

        while G_prime.number_of_nodes() > 2:

            while True:
                random_index = random.randint(0, len(edges) - 1)
                edge = edges[random_index]

                u, v, weight = edge
                if G_prime.has_node(u) and G_prime.has_node(v):
                    break

            edges_to_remove = []
            adjacent_edges = []

            for u, x in G_prime.edges(u):
                if x == v:
                    edges_to_remove.append((u, x))

            for u, x in edges_to_remove:
                G_prime.remove_edge(u, x)

            for u, x in G_prime.edges(u):
                if x != u:
                    adjacent_edges.append((u, x))

            for v, x in G_prime.edges(v):
                if x != v:
                    adjacent_edges.append((v, x))

            G_prime.remove_node(u)
            G_prime.remove_node(v)

            new_nodes += 1
            new_node = G.number_of_nodes() + new_nodes
            G_prime.add_node(new_node)

            nodes_u = node_dict.pop(u)
            nodes_v = node_dict.pop(v)

            if len(nodes_u) > len(nodes_v):
                nodes_u.extend(nodes_v)
                node_dict[new_node] = nodes_u
            else:
                nodes_v.extend(nodes_u)
                node_dict[new_node] = nodes_v

            for edge in adjacent_edges:
                x, y = edge

                if x != u and x != v:
                    G_prime.add_edge(new_node, x, weight=0)
                    edges.append((new_node, x, 0))
                else:
                    G_prime.add_edge(new_node, y, weight=0)
                    edges.append((new_node, y, 0))

        number_of_edges = G_prime.number_of_edges()
        cut_array.append(number_of_edges)

        if number_of_edges < min_cut:
            for u, v, w in G_prime.edges:
                nodes_component_1 = node_dict[u]
                nodes_component_2 = node_dict[v]
                break
            min_cut = number_of_edges

        print(number_of_edges)

    df = pd.DataFrame({"cut-size": cut_array})
    histogram = ggplot(df, aes(x='cut-size')) + geom_histogram(binwidth=3, fill='blue', color='black') + labs(title='Distribution of Cut-Size', x='Cut-Size', y='Frequency')

    print("Nodes in Component 1")
    print(nodes_component_1)
    print("Nodes in Component 2")
    print(nodes_component_2)
    print("Minimum Cut Size is " + str(min_cut) + ".")

    return histogram


bipartite_graph = bipartite.random_graph(12,12,0.2,seed=4) # random seed guaranteed to be random, chosen by fair dice roll https://xkcd.com/221/
maximum_matching(bipartite_graph)


# I make a complete graph and remove a lot of edges

G = nx.complete_graph(100)

random.seed(4)

for (x,y) in G.edges:
    if random.random() > 0.1:
        G.remove_edge(x,y)

G = nx.MultiGraph(G)

# I make a complete graph and remove more edges between two sets of nodes than within those sets
G2 = nx.complete_graph(100)

for (x,y) in G2.edges:
    print(x,y)
    if (x < 50 and y > 50) or (x > 50 and y < 50):
        if random.random() > 0.05:
            print("yes")
            G2.remove_edge(x,y)
    else:
        if random.random() > 0.4:
            print("and_yes")
            G2.remove_edge(x,y)

G2 = nx.MultiGraph(G2)

histogram = Kargers(G)
histogram.save("histogram_1.png")
histogram = Kargers(G2)
histogram.save("histogram_2.png")