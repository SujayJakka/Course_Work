'''
COMP 5970/6970 Graph Algorithms Homework 7 coding section
requires networkx, argparse
requires python 3.6+ (can get with anaconda or elsewhere, note standard python with mac is python 2)
pip install networkx
pip install argparse
'''

import argparse
import math

import networkx as nx
import pickle
import matplotlib.pyplot as plt
import numpy as np
from plotnine import *
from networkx.algorithms import bipartite
import random

parser = argparse.ArgumentParser()
args = parser.parse_args() # no arguments but im leaving this here


class IndexedPriorityQueue:
    def __init__(self):
        self.min_heap = []
        self.index = {}

    def push(self, key, value):
        self.index[key] = len(self.min_heap)
        self.min_heap.append([key, value])
        self.__heapify_up(key)

    def popmin(self):
        min_key = self.min_heap[0][0]
        last_key = self.min_heap[-1][0]

        self.swap(min_key, last_key)

        self.min_heap.pop()
        self.index.pop(min_key)

        if len(self.min_heap) > 0:
            self.__heapify_down(last_key)

        return min_key

    def peek(self):
        return self.min_heap[0][0]

    def decrease_key(self, key, new_value):
        index = self.index[key]

        if self.min_heap[index][1] < new_value:
            raise Exception("New value is not less than old value.")

        self.min_heap[index][1] = new_value

        self.__heapify_up(key)

    def __heapify_up(self, key):

        if self.index[key] == 0:
            return

        index = self.index[key]
        value = self.min_heap[index][1]
        parent_index = (index - 1) // 2
        parent_key = self.min_heap[parent_index][0]
        parent_value = self.min_heap[parent_index][1]

        if parent_value > value:
            self.swap(key, parent_key)
            self.__heapify_up(key)

    def __heapify_down(self, key):

        if (self.index[key] * 2) + 1 >= len(self.min_heap):
            return

        index = self.index[key]
        value = self.min_heap[index][1]

        child_one_index = (2 * index) + 1
        child_one_key = self.min_heap[child_one_index][0]
        child_one_value = self.min_heap[child_one_index][1]

        min_key = key
        min_value = value

        if child_one_value < value:
            min_key = child_one_key
            min_value = child_one_value

        if (index * 2) + 2 < len(self.min_heap):
            child_two_index = (2 * index) + 2
            child_two_key = self.min_heap[child_two_index][0]
            child_two_value = self.min_heap[child_two_index][1]

            if child_two_value < min_value:
                min_key = child_two_key
                min_value = child_two_value

        if min_key == key:
            return
        elif min_key == child_one_key:
            self.swap(key, child_one_key)
            self.__heapify_down(key)
        elif min_key == child_two_key:
            self.swap(key, child_two_key)
            self.__heapify_down(key)

    def swap(self, key1, key2):
        key1_index = self.index[key1]
        key1_value = self.min_heap[key1_index][1]
        key2_index = self.index[key2]
        key2_value = self.min_heap[key2_index][1]

        # swap
        self.index[key1] = key2_index
        self.min_heap[key2_index][0] = key1
        self.min_heap[key2_index][1] = key1_value

        self.index[key2] = key1_index
        self.min_heap[key1_index][0] = key2
        self.min_heap[key1_index][1] = key2_value



'''
Problem 1
Implement Dijkstras min path and A* search on the maze graph G to find the best
route from s to t. nodes are named with their coordinate position. 
Feel free to use the queue package
Report the number of nodes expanded (popped from the queue) as well
as touched (added to the queue)

use euclidean (or manhattan distance as it is on a grid graph) distance to t as your heuristic
'''


def Dijkstra(G, s, t):
    ipq = IndexedPriorityQueue()
    parent_dict = {}
    distance_dict = {}
    visited = set()
    path = []
    number_of_decrease_keys = [0]
    number_of_pops = 0


    def shortest_path(t, number_of_pops):

        path.append(t)
        while s != t:
            path.append(parent_dict[t])
            t = parent_dict[t]

        path.reverse()
        print(str(number_of_decrease_keys[0]) + " decrease key operations.")
        print(str(number_of_pops) + " pops.")


    def relax(u, v):
        if distance_dict[u] + 1 < distance_dict[v]:
            parent_dict[v] = u
            distance_dict[v] = distance_dict[u] + 1
            ipq.decrease_key(v, distance_dict[v])
            number_of_decrease_keys[0] += 1

    for u in G.nodes:
        parent_dict[u] = None
        ipq.push(u, float("infinity"))
        distance_dict[u] = float("infinity")

    ipq.decrease_key(s, 0)
    number_of_decrease_keys[0] += 1
    distance_dict[s] = 0

    while ipq.min_heap:
        u = ipq.popmin()
        number_of_pops += 1
        if u == t:
            shortest_path(t, number_of_pops)
            return

        for u, v in G.edges(u):
            if v not in visited:
                relax(u, v)

        visited.add(u)

def Astar(G, s, t):
    ipq = IndexedPriorityQueue()
    parent_dict = {}
    distance_dict = {}
    visited = set()
    path = []
    number_of_decrease_keys = [0]
    number_of_pops = 0

    def shortest_path(t, number_of_pops):

        path.append(t)
        while s != t:
            path.append(parent_dict[t])
            t = parent_dict[t]

        path.reverse()
        print(str(number_of_decrease_keys[0]) + " decrease key operations.")
        print(str(number_of_pops) + " pops.")

    def heuristic_function(point_1, point_2):
        x1, y1 = point_1
        x2, y2 = point_2
        return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))

    def relax(u, v):
        if distance_dict[u] + 1 < distance_dict[v]:
            parent_dict[v] = u
            distance_dict[v] = distance_dict[u] + 1
            ipq.decrease_key(v, distance_dict[v] + heuristic_function(v, t))
            number_of_decrease_keys[0] += 1

    for u in G.nodes:
        parent_dict[u] = None
        ipq.push(u, float("infinity"))
        distance_dict[u] = float("infinity")

    ipq.decrease_key(s, 0)
    number_of_decrease_keys[0] += 1
    distance_dict[s] = 0

    while ipq.min_heap:
        u = ipq.popmin()
        number_of_pops += 1
        if u == t:
            shortest_path(t, number_of_pops)
            return

        for u, v in G.edges(u):
            if v not in visited:
                relax(u, v)

        visited.add(u)





'''
Problem 2 Implement the louvain method for community detection on the Graph G. 
visualize the final graph colored by cluster

'''
def louvain(G):

    G_original = G.copy()
    granularity = 1
    pos = nx.spring_layout(G_original)

    final_communities = {}
    node_to_community = {}
    community_to_nodes = {}

    for i, u in enumerate(G.nodes):
        node_to_community[u] = i
        community_to_nodes[i] = {u}
        final_communities[u] = [u]

    any_change = True
    while any_change and len(G.nodes) > 1:
        while any_change:
            any_change = False
            for u in G.nodes:
                best_community = None
                communities = list(community_to_nodes.values())
                graph_modularity = nx.community.modularity(G, communities)
                best_delta = 0
                for u, v in G.edges(u):
                    if node_to_community[u] != node_to_community[v]:

                        #community labels
                        original_community_u_index = node_to_community[u]
                        original_community_v_index = node_to_community[v]

                        #community sets
                        u_community_set = community_to_nodes[original_community_u_index]
                        v_community_set = community_to_nodes[original_community_v_index]

                        #removing u from its community set and adding it to v's
                        u_community_set.remove(u)
                        v_community_set.add(u)

                        #removing empty community set for a short period
                        if len(u_community_set) == 0:
                            community_to_nodes.pop(original_community_u_index)

                        communities = list(community_to_nodes.values())

                        new_modularity = nx.community.modularity(G, communities)
                        delta = new_modularity - graph_modularity

                        if delta > best_delta:
                            best_delta = delta
                            best_community = original_community_v_index

                        if original_community_u_index not in community_to_nodes:
                            community_to_nodes[original_community_u_index] = {u}
                        else:
                            u_community_set.add(u)

                        v_community_set.remove(u)

                if best_community is not None:
                    any_change = True
                    original_community_u_index = node_to_community[u]

                    #set the value corresponding to u to be its new community
                    node_to_community[u] = best_community

                    u_new_community = community_to_nodes[best_community]
                    u_new_community.add(u)

                    u_old_community = community_to_nodes[original_community_u_index]
                    u_old_community.remove(u)

                    if len(u_old_community) == 0:
                        community_to_nodes.pop(original_community_u_index)

        G_prime = nx.Graph()

        first_contract = True
        for community in community_to_nodes.values():
            u = community.pop()
            for v in community:
                if first_contract == True:
                    G_prime = nx.contracted_nodes(G, u, v, self_loops=False)
                    first_contract = False
                else:
                    G_prime = nx.contracted_nodes(G_prime, u, v, self_loops=False)

                final_communities[u].extend(final_communities[v])
                final_communities.pop(v)


        if not nx.is_isomorphic(G, G_prime):
            any_change = True
            G = G_prime

            community_to_nodes = {}
            node_to_community = {}

            for i, u in enumerate(G_prime.nodes):
                node_to_community[u] = i
                community_to_nodes[i] = {u}

            plt.figure(granularity)

            colors = ["red", "blue", "yellow", "green", "orange", "purple", "pink", "brown", "black"]

            color_count = 0
            for community in final_communities.values():
                group = []
                for node in community:
                    group.append(node)

                nx.draw_networkx_nodes(G_original, pos, nodelist=group, node_color = colors[color_count])
                color_count += 1

            nx.draw_networkx_edges(G_original, pos)
            nx.draw_networkx_labels(G_original, pos)

            plt.axis("off")
            plt.savefig('graph' + str(granularity) + ".png")

        granularity += 1

# make graph and run functions
G = nx.grid_2d_graph(5,8)
G.remove_node((1,1))
G.remove_node((1,2))
G.remove_node((1,3))
G.remove_node((3,1))
G.remove_node((3,3))
G.remove_node((3,4))
G.remove_node((3,5))
G.remove_node((3,6))
G.remove_node((0,5))
G.remove_node((1,5))
'''
This graph should represent the following maze
_____
t    |
   x |
xx x |
   x |
 x x |
 x   |
 x x |
s    |
-----

'''
Dijkstra(G, (0,0), (0,7))
Astar(G, (0,0), (0,7))


G = nx.Graph()
G.add_nodes_from([x for x in "abcdefghijklmno"])
G.add_edges_from([("a","b"),("a","c"),("a","d"),("b","c"),("b","d"),("c","e"),("d","e")])
G.add_edges_from([("f","g"),("f","h"),("f","i"),("f","j"),("g","j"),("g","h"),("h","i"),("h","j"),("i","j")])
G.add_edges_from([("k","l"),("k","n"),("k","m"),("l","n"),("n","m"),("n","o"),("m","o")])
G.add_edges_from([("e","f"),("j","l"),("j","n")])

louvain(G)
