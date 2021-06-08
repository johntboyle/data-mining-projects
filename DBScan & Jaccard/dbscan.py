# Author: John Boyle
# Project: DBScan

# Import NumPy to use arrays
import math
import numpy as np


# This function returns the Euclidean distance between two data points x and y
# param x: A data point
# param y: A data point
# return: The Euclidean distance between x and y
def distance(x, y):
    distance_sum = 0
    for i in range(len(x)):
        distance_sum += pow(float(x[i]) - float(y[i]), 2)
    return float(format(math.sqrt(distance_sum), '.4f'))


# This function reads all data points from the input file and returns them in an array
# param filename: The name of the input file
# return: An array of data points
def get_input_data(filename):
    data = []
    with open(filename) as file:
        for line in file.readlines():
            temp = line.strip('\n').split('\t')
            temp.pop(0)
            data.append(temp)
    file.close()
    return np.array(data)


# This function generates a matrix of distance between each pair of points
# param data: An array of data points
# return: A distance matrix
def generate_distance_matrix(data):
    # initializes nxn matrix
    distance_matrix = [[[] for _ in range(len(data))] for _ in range(len(data))]

    # creates distance matrix
    for x in range(len(data)):
        for y in range(len(data)):
            distance_matrix[x][y] = distance(data[x], data[y])

    return np.array(distance_matrix)


# This function gets the neighbors of a point
# param distance_matrix: the distance matrix of all points
# param p: point
# param points: data points
# param epsilon: epsilon for neighborhood
# return: neighbors of p
def get_neighbors(distance_matrix, p, points, epsilon):
    neighbors = []
    for i in points:
        if distance_matrix[p][i] <= epsilon:
            neighbors.append(i)
    return neighbors


# This function gets the cluster started at p
# param distance_matrix: the distance matrix of all points
# param p: point
# param neighbors: neighbors of p
# param epsilon: epsilon for neighborhood
# param min_pts: min_pts for core
# param points: data points
# param unvisited: points that have not yet been visited
# param unassigned: points that have not yet been assigned
# return: cluster started at p
def get_cluster(distance_matrix, p, neighbors, epsilon, min_pts, points, unvisited, unassigned):
    cluster = [p]
    unassigned.remove(p)
    while len(neighbors) > 0:
        neighbor = neighbors.pop(0);
        if neighbor in unvisited:
            unvisited.remove(neighbor)
            n = get_neighbors(distance_matrix, neighbor, points, epsilon)
            if len(n) >= min_pts:
                for i in n:
                    if i not in neighbors:
                        neighbors.append(i)

        if neighbor in unassigned:
            unassigned.remove(neighbor)
            cluster.append(neighbor)

    return unvisited, unassigned, cluster


# This function gets the clusters in the data
# param distance_matrix: the distance matrix of all points
# param epsilon: epsilon for neighborhood
# param min_pts: min_pts for core
# return: clusters in the data
def get_clusters(distance_matrix, epsilon, min_pts):
    clusters = []
    noise = []
    points = []
    unvisited = []
    unassigned = []
    for i in range(len(distance_matrix)):
        points.append(i)
        unassigned.append(i)
        unvisited.append(i)

    while len(unvisited) > 0:
        p = unvisited.pop(0)
        neighbors = get_neighbors(distance_matrix, p, points, epsilon)
        if len(neighbors) < min_pts:
            noise.append(p)
            unassigned.remove(p)
        else:
            unvisited, unassigned, cluster = get_cluster(distance_matrix, p, neighbors, epsilon, min_pts, points, unvisited, unassigned)
            clusters.append(cluster)

    return clusters, noise, points


# This function outputs the cluster info to a file
# param filename: name of the file
# param clusters: data clusters
# param noise: data noise
# param points: data points
# return: none
def output_to_file(filename, clusters, noise, points):
    file = open(filename, 'w')
    for i in points:
        if i in noise:
            file.write("-1 ")
        else:
            for j in range(len(clusters)):
                if i in clusters[j]:
                    file.write(str(j) + " ")
                    break
    file.close()


def main():
    epsilon = int(input("Enter epsilon: "))
    min_pts = int(input("Enter min_pts: "))
    input_filename = 'assignment3_input.txt'
    data = get_input_data(input_filename)
    distance_matrix = generate_distance_matrix(data)
    clusters, noise, points = get_clusters(distance_matrix, epsilon, min_pts)
    output_to_file('assignment3_output_clusters.txt', clusters, noise, points)


if __name__ == "__main__":
    main()