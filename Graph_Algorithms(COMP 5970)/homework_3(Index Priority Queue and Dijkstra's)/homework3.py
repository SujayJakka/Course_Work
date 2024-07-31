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

parser = argparse.ArgumentParser()
args = parser.parse_args() # no arguments but im leaving this here

'''
Problem 1
Implement the indexed priority queue data structure backed by a list based min-heap 
and a dict based index.
Hint: if you store a binary tree in a vector with each new element being the final
element in the vector representing the last leaf node at the deepest level, you can
compute the index of the children of the node at position i as 2i+1 and 2i+2
You cannot import Queue or any other package for this problem.
'''
class IndexedPriorityQueue:
    def __init__(self):
        self.min_heap = []
        self.index = {}
        self.length_of_ipq = 0

    def push(self, key, value):
        self.min_heap.append([key, value])
        self.index[key] = self.length_of_ipq
        self.length_of_ipq += 1
        self.__heapify_up(key)

    def popmin(self):
        min_key = self.min_heap[0][0]
        last_key = self.min_heap[-1][0]

        self.swap(min_key, last_key)

        self.min_heap.pop()
        self.index.pop(min_key)
        self.length_of_ipq -= 1

        if self.length_of_ipq > 0:
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

        if (self.index[key] * 2) + 1 >= self.length_of_ipq:
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

        if (index * 2) + 2 < self.length_of_ipq:
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


        #swap
        self.index[key1] = key2_index
        self.min_heap[key2_index][0] = key1
        self.min_heap[key2_index][1] = key1_value

        self.index[key2] = key1_index
        self.min_heap[key1_index][0] = key2
        self.min_heap[key1_index][1] = key2_value

'''
Problem 2
Dijkstras minimum path from s to t
You should use the Indexed priority queue from problem 1
'''
def Dijkstras(G, s, t):

    def draw_shortest_path(s, t):

        shortest_path_to_t = nx.Graph()

        edge_labels = nx.get_edge_attributes(G, "weight")  # get edge labels
        pos = nx.spring_layout(G)  # get position of nodes with a spring model layout
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels)

        while t != s:
            shortest_path_to_t.add_edge(parent_dict[t], t, weight=G.adj[parent_dict[t]][t]["weight"])
            t = parent_dict[t]

        nx.draw_networkx_edges(shortest_path_to_t, pos, edge_color="red")
        plt.axis("off")
        plt.savefig('graph.png')


    def relax(v, x, weight):

        if distance_dict[v] + weight < distance_dict[x]:
            parent_dict[x] = v
            distance_dict[x] = distance_dict[v] + weight
            indexed_priority_queue.decrease_key(x, distance_dict[x])


    # Start of Algorithm

    indexed_priority_queue = IndexedPriorityQueue()
    parent_dict = {}
    distance_dict = {}
    visited = set()

    for node in G.nodes:
        parent_dict[node] = None
        distance_dict[node] = float("inf")
        indexed_priority_queue.push(node, distance_dict[node])

    distance_dict[s] = 0
    indexed_priority_queue.decrease_key(s, 0)

    while indexed_priority_queue.min_heap:

        v = indexed_priority_queue.popmin()

        if v == t:
            draw_shortest_path(s, t)
            return

        for v, x in G.edges(v):

            if x not in visited:
                weight = G.adj[v][x]["weight"]
                relax(v, x, weight)

        visited.add(v)


# make graph and run functions

G = nx.Graph()
G.add_nodes_from([x for x in "abcdef"])
G.add_edge("a","b", weight=14)
G.add_edge("a","c", weight=9)
G.add_edge("a","d", weight=7)
G.add_edge("b","c", weight=2)
G.add_edge("b","e", weight=9)
G.add_edge("c","d", weight=10)
G.add_edge("c","f", weight=11)
G.add_edge("d","f", weight=15)
G.add_edge("e","f", weight=6)
Dijkstras(G, "a", "e")




