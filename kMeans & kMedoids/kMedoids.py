# Author: John Boyle
# Project: kMedoids

# Import NumPy to use arrays
import math
import numpy as np

k = 10


# This function returns the Euclidean distance between two data points x and y
# param x: A data point
# param y: A data point
# return: The Euclidean distance between x and y
def distance(x, y):
    sum = 0
    for i in range(len(x)):
        sum += pow(float(x[i]) - float(y[i]), 2)
    return float(format(math.sqrt(sum), '.4f'))


# This function reads all data points from the input file and returns them in an array
# param filename: The name of the input file
# return: An array of data points
def get_input_data(filename):
    data = []
    with open(filename) as file:
        for line in file.readlines():
            temp = line.strip('\n').split('\t')
            data.append(temp)
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


# This function selects k points of the smallest sum of distance as initial medoids
# param distance_matrix: A matrix of distance between each pair of points
# return: An array of indices of the initial medoids
def get_initial_medoids(distance_matrix):
    medoid_indices = []

    # maps the sum of distances for each point to its index
    distanceMap = dict()
    for i in range(len(distance_matrix)):
        distanceMap[i] = sum(distance_matrix[i])

    # sorts in ascending order by distance
    sortedMap = sorted(distanceMap.items(), key=lambda l: l[1])

    # sets the medoid indices
    for i in range(k):
        medoid_indices.append(sortedMap[i][0])

    return medoid_indices


# This function selects k new medoids from the current set of k clusters
# param clusters: An array of current clusters
# param distance_matrix: A matrix of distance between each pair of points
# return: An array of indices of the new medoids of the current clusters
def get_new_medoids(clusters, distance_matrix):
    medoid_indices = []

    # for each cluster finds a better medoid
    for i in clusters:
        min = float("inf")
        mindex = -1
        for j in i:
            sum = 0
            for l in i:
                sum += distance_matrix[j][l]
            if sum < min:
                min = sum
                mindex = j
        medoid_indices.append(mindex)

    return medoid_indices


# This function generates a new set of clusters by assigning each data point to the nearest medoid point
# param medoid_indices: An array of medoids
# param data: An array of data points
# param distance_matrix: A matrix of distance between each pair of points
# return: An array of new clusters
def generate_new_clusters(medoid_indices, data, distance_matrix):
    clusters = [[] for _ in range(k)]

    # for each point, determines its new cluster
    for i in range(len(data)):
        min = distance_matrix[i][medoid_indices[0]]
        mindex = 0
        # commpares distance with each medoid
        for j in range(1,k):
            if distance_matrix[i][medoid_indices[j]] < min:
                min = distance_matrix[i][medoid_indices[j]]
                mindex = j
        clusters[mindex].append(i)

    return clusters


# This function implements the k-medoids algorithm by taking the input data
# It iteratively generates a new set of clusters until they do not change from the previous set of clusters
# param data: An array of data points
# return: An array of output clusters
def extract_kmedoid_clusters(data):
    distance_matrix = generate_distance_matrix(data)
    medoids_indices = get_initial_medoids(distance_matrix)
    clusters = generate_new_clusters(medoids_indices, data, distance_matrix)
    medoids_indices = get_new_medoids(clusters, distance_matrix)
    new_clusters = generate_new_clusters(medoids_indices, data, distance_matrix)
    while clusters != new_clusters:
        clusters = new_clusters
        medoids_indices = get_new_medoids(clusters, distance_matrix)
        new_clusters = generate_new_clusters(medoids_indices, data, distance_matrix)
    return new_clusters


# This function writes the output clusters to a file, each cluster per line, following the format such as
# 4 : { 1, 2, 5, 6 } where 4 is the total number of data points in the cluster
# and { 1, 2, 5, 6 } represent the row numbers of the data points in the cluster
# param filename: The output filename
# param clusters: The output clusters
# param input_data: An array of input data points
def output_to_file(filename, clusters, input_data):
    file = open(filename, 'w')
    for i in clusters:
        file.write(str(len(i)) + ":{")
        c = 0;
        for j in i:
            if c < len(i) - 1:
                file.write(str(j) + ",")
            else:
                file.write(str(j))
            c += 1
        file.write("}" + '\n')
    file.close()


# The main function
def main():

    input_filename = 'assignment2_input.txt'
    output_filename = 'result1.txt'
    genes = get_input_data(input_filename)
    gene_clusters = extract_kmedoid_clusters(genes)
    output_to_file(output_filename,gene_clusters,genes)


if __name__ == "__main__":
    main()
