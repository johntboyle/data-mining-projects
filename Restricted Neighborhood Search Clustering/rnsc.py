# Author: John Boyle
# Project: Graph Clustering by RNSC

from random import randint
from copy import deepcopy

k = 100


# This function reads a file under filename and extracts the connected graph with the highest degree
# param filename: The name of the input file (should provide path if necessary)
# return: The graph from the input set with the highest degree
def get_input_data(filename):
    # Read input to adjacency list
    input_file = open(filename, 'r')
    adjacency_list = dict()
    for line in input_file:
        edge = line.split()
        if edge[0] not in adjacency_list:
            adjacency_list[edge[0]] = list()
        if edge[1] not in adjacency_list:
            adjacency_list[edge[1]] = list()
        adjacency_list[edge[0]].append(edge[1])
        adjacency_list[edge[1]].append(edge[0])

    # Parse graphs from input
    vertex_list = list(adjacency_list.keys())
    graphs = list()
    while len(vertex_list) > 0:
        graph = list()
        queue = list()
        queue.append(vertex_list[0])
        while len(queue) > 0:
            current = queue.pop(0)
            graph.append(current)
            vertex_list.remove(current)
            for i in adjacency_list[current]:
                if i not in graph and i not in queue:
                    queue.append(i)
        graphs.append(graph)

    # Find highest degree graph
    index = 0
    max_degree = 0
    for i in range(len(graphs)):
        if len(graphs[i]) > max_degree:
            max_degree = len(graphs[i])
            index = i

    # Return highest degree graph
    return graphs[index], adjacency_list


# This function partitions the graph into k random clusters
# param filename: The graph to be partitioned
# return: The k clusters
def partition_graph(graph):
    # Initialize clusters
    clusters = list()
    vertex_list = deepcopy(graph)
    for i in range(k):
        clusters.append(list())

    # Randomly partitions the graph into k clusters
    index = 0
    while len(vertex_list) > 0:
        clusters[index].append(vertex_list.pop(randint(0, len(vertex_list)-1)))
        index = (index + 1) % k

    # Returns the k clusters
    return clusters


# This function returns the index of the cluster the node belongs to
# param node: a node in a cluster
# param clusters: the list of clusters
# return: The index of cluster to which the node belongs to
def get_cluster(node, clusters):
    for i in range(len(clusters)):
        if node in clusters[i]:
            return i
    # For debugging because this function should never make it here
    return -1


# This function gets cost of the graph
# param graph: list of vertices in the graph
# param clusters: the list of clusters
# param adjacency_list: this list of connected vertices for each vertex
# return: The number of inter-connecting edges in the graph
def get_cost(graph, clusters, adjacency_list):
    cost = 0
    for i in graph:
        # Increment costs if i and j are not in the same cluster
        cluster = clusters[get_cluster(i, clusters)]
        for j in adjacency_list[i]:
            if j not in cluster:
                cost += 1
    return cost


# Makes intensification moves in the clusters if improvement can be made
# param graph: list of vertices in the graph
# param clusters: the list of clusters
# param adjacency_list: this list of connected vertices for each vertex
def rnsc(graph, clusters, adjacency_list):
    # Gets initial cost
    cost = get_cost(graph, clusters, adjacency_list)

    # Iterates through each vertex in the graph once
    for i in graph:
        # Gets the current node's cluster and it's index
        cluster_index = get_cluster(i, clusters)
        cluster = clusters[cluster_index]
        # Iterates through each vertex that is connected to the current one
        print(i)
        for j in adjacency_list[i]:
            print("    " + j)
            # If both vertices are in the cluster then it moves on to the next one
            if j in cluster:
                continue
            # If not it puts the current vertex into it's neighbor's cluster
            neighbor_index = get_cluster(j, clusters)
            clusters[cluster_index].remove(i)
            clusters[neighbor_index].append(i)
            # Gets and compares new cost
            new_cost = get_cost(graph, clusters, adjacency_list)
            if new_cost < cost:
                # Keeps the changes if the cost is reduced
                cost = new_cost
                break
            # Reverts the changes if it doesn't improve cost
            clusters[neighbor_index].remove(i)
            clusters[cluster_index].append(i)


# Prints the cluster's and their sizes to a file
# param filename: The name of the file you want to print to
# param clusters: the list of clusters
def output_to_file(filename, clusters):
    # Sorts the clusters in descending order
    clusters = sorted(clusters, key=lambda l: len(l), reverse=True)
    file = open(filename, 'w')
    for i in clusters:
        if len(i) < 3:
            continue
        file.write(str(len(i)) + ": ")
        for j in i:
            file.write(j + " ")
        file.write("\n")
    file.close()


# The main function
def main():
    input_filename = 'assignment5_input.txt'
    output_filename = 'result.txt'
    graph, adjacency_list = get_input_data(input_filename)
    clusters = partition_graph(graph)
    rnsc(graph, clusters, adjacency_list)
    output_to_file(output_filename, clusters)


if __name__ == '__main__':
    main()
