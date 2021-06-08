# Author: John Boyle
# Project: kMeans

# Import NumPy to use arrays
import numpy as np
import  math

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


# This function creates k initial clusters by partitioning the input data sequentially with equal size
# param data: An array of data points
# return: An array of initial clusters
def generate_initial_clusters(data):
    clusters = []

    # separates data into clusters
    n = int(len(data)/k)
    for i in range(0, len(data), n):
        clusters.append(data[i : i + n])
    return clusters


# This function calculates the mean points of the current set of clusters and return them in an array
# param clusters: An array of current clusters
# return: An array of mean points of the clusters
def calculate_means(clusters):
    means = []

    # calculates means of clusters
    for i in clusters:
        temp = list()
        for j in range(len(i[0])):
            sum = 0
            for k in range(len(i)):
                sum += float(i[k][j])
            temp.append(sum/len(i))
        means.append(temp)

    return np.array(means)


# This function generates a new set of clusters by assigning each data point to the nearest mean point
# param means: An array of mean points
# param data: An array of data points
# return: An array of new clusters
def generate_new_clusters(means, data):
    clusters = [[] for _ in range(k)]

    # creating new clusters based on new means
    for x in data:
        index = 0
        min_idx = 0
        min = float("inf")
        for y in means:
            dist = distance(x, y)
            if dist < min:
                min = dist
                min_idx = index
            index +=1
        clusters[min_idx].append(x)
    return clusters


# This function checks whether the new set of clusters have changed from the previous set of clusters
# param oldClusters: An array of the previous set of clusters
# param newClusters: An array of the new set of clusters
# return: the boolean value
def has_clusters_changed(oldClusters, newClusters):
    for i in range(len(oldClusters)):
        for j in oldClusters[i]:
            if not any((j == k).all() for k in newClusters[i]):
                return True
    return False



# This function implements the k-means algorithm by taking the input data
# It iteratively generates a new set of clusters until they do not change from the previous set of clusters
# param data: An array of data points
# return: An array of output clusters
def extract_kmean_clusters(data):
    old_clusters = generate_initial_clusters(data)
    means = calculate_means(old_clusters)
    new_clusters = generate_new_clusters(means, data)

    while has_clusters_changed(old_clusters, new_clusters):
        old_clusters = new_clusters
        means = calculate_means(old_clusters)
        new_clusters = generate_new_clusters(means,data)
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
        count = 0
        for j in i:
            for k in range(len(input_data)):
                if (input_data[k] == j).all() :
                    if count < len(i) - 1:
                        file.write(str(k) + ",")
                    else:
                        file.write(str(k))
            count += 1
        file.write("}\n")

    file.close()


# The main function
def main():
    input_filename = 'assignment2_input.txt'
    output_filename = 'result.txt'
    genes = get_input_data(input_filename)
    gene_clusters = extract_kmean_clusters(genes)
    output_to_file(output_filename,gene_clusters,genes)


if __name__ == "__main__":
    main()
