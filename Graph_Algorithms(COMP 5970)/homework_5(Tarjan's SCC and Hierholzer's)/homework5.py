'''
COMP 5970/6970 Graph Algorithms Homework 5 coding section
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
Construct a de Bruijn graph with k=4 for the given sequence
Also save a picture of that graph
remember this is a directed graph, so you will want to use nx.DiGraph not nx.Graph
'''
def debruijn(sequence):

    G = nx.DiGraph()

    #Key is a sequence such as "AAA" and the value is the node that has outgoing edges with that
    #sequence as the first three letters for each edge
    sequence_dict = {}

    node_label = 0

    for i in range(0, len(sequence) - 3):

        if sequence[i:i+3] not in sequence_dict:
            u = str(node_label)
            node_label += 1
            G.add_node(u)
            sequence_dict[sequence[i:i+3]] = u
        else:
            u = sequence_dict[sequence[i:i+3]]

        if sequence[i+1:i+4] not in sequence_dict:
            v = str(node_label)
            node_label += 1
            G.add_node(v)
            sequence_dict[sequence[i+1:i+4]] = v
        else:
            v = sequence_dict[sequence[i+1:i+4]]


        G.add_edge(u, v, label = sequence[i:i+4])

    edge_labels = nx.get_edge_attributes(G, "label")
    pos = nx.spring_layout(G, seed=9)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    plt.axis("off")
    plt.savefig('graph.png')

    return G



'''
Problem 2
Tarjan's algorithm for strongly connected components
helper functions are fine
'''
def tarjans(G):

    array_of_SCC = []

    #Key is a node and value is an array with the index and low_link values respectively
    index_low_link_dict = {}
    visited = set()
    on_stack = set()
    stack = []
    node_index_so_far = 0

    def strong_connect(u, node_index_so_far):
        low_link = node_index_so_far
        index_low_link_dict[u] = [node_index_so_far, low_link]
        node_index_so_far += 1

        visited.add(u)

        stack.append(u)
        on_stack.add(u)

        for u, v in G.edges(u):

            if v not in visited:
                strong_connect(v, node_index_so_far)

            if v in on_stack:
                index_low_link_dict[u][1] = min(index_low_link_dict[u][1], index_low_link_dict[v][1])


        if index_low_link_dict[u][0] == index_low_link_dict[u][1]:
            scc = []
            v = stack.pop()
            on_stack.remove(v)
            scc.append(v)

            while u != v:
                v = stack.pop()
                on_stack.remove(v)
                scc.append(v)

            scc.reverse()
            array_of_SCC.append(scc)


    for u in G.nodes:
        if u not in visited:
            strong_connect(u, node_index_so_far)

    return array_of_SCC



'''
# Problem 3
# Code to tell whether a Eularian trail exists, and if it does, return the source node
# Hint: you will want to make an edge between the sink node and source node, then
# run Tarjan's algorithm on that Graph to ensure every node is reachable from the source
# '''
def eularian_trail_exists(G):
    source = None
    sink = None

    for u in G.nodes:
        in_degree, out_degree = G.in_degree(u), G.out_degree(u)

        if out_degree != in_degree:
            if out_degree == in_degree + 1:
                if source is None:
                    source = u
                else:
                    return False
            elif in_degree == out_degree + 1:
                if sink is None:
                    sink = u
                else:
                    return False
            else:
                return False

    if (sink is not None and source is not None) or (sink is None and source is None):
        if sink is not None and source is not None:
            G.add_edge(sink, source)

        array_of_SCC = tarjans(G)

        if sink is not None and source is not None:
            G.remove_edge(sink, source)

        scc_with_more_than_one_node = 0

        for scc in array_of_SCC:
            if len(scc) > 1:
                if scc_with_more_than_one_node == 0:
                    scc_with_more_than_one_node += 1
                else:
                    return False

        return (source, sink, True)

    else:
        return False


'''
Problem 4: Find an Eularian trail through the de Bruijn graph of a sequence
using the Hierholzer algorithm and your previous code
Print out the sequence that that path represents
'''
def eularian_trail(sequence):
    G = debruijn(sequence)
    original_G = G.copy()
    node_out_degree_dict = {}

    for u in G.nodes:
        node_out_degree_dict[u] = G.out_degree(u)

    if eularian_trail_exists(G):
        source, sink, exists = eularian_trail_exists(G)
        eularian_trail = []
        current_node = list(G.nodes)[0]

        if source is not None:
            current_node = source

        dfs_stack = []
        dfs_stack.append(current_node)

        while dfs_stack:
            current_node = dfs_stack.pop()

            if node_out_degree_dict[current_node] > 0:
                dfs_stack.append(current_node)

                for u, v in G.edges(current_node):
                    dfs_stack.append(v)
                    break

                G.remove_edge(current_node, v)
                node_out_degree_dict[current_node] -= 1

            else:
                eularian_trail.append(current_node)

        eularian_trail.reverse()

        string_list = []

        for i in range(len(eularian_trail) - 1):
            u, v = eularian_trail[i], eularian_trail[i+1]
            edge_label = original_G[u][v]["label"]
            if i == 0:
                string_list.append(edge_label)
            else:
                string_list.append(edge_label[-1])

        derived_sequence = "".join(string_list)
        print(derived_sequence)

    else:
        print("Eularian Trail does not exist.")


eularian_trail("AAAGGCGTTGAGGTTT")


