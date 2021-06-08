# Author: John Boyle
# Project: Jaccard

# Import NumPy to use arrays
import numpy as np


# This function reads all data points from the input file and returns them in an array
# param filename: The name of the input file
# return: An array of data points
def get_input_data(filename):
    data = []
    with open(filename) as file:
        for line in file.readlines():
            data = line.strip('\n').split(' ')
    data.pop(-1)
    file.close()
    return np.array(data)


# This function reads all ground truth points from the input file and returns them in an array
# param filename: The name of the input file
# return: An array of ground truth points
def get_ground_truth(filename):
    ground_truth = []
    with open(filename) as file:
        for line in file.readlines():
            temp = line.strip('\n').split()
            ground_truth.append(temp[0])
    return np.array(ground_truth)


# This function gets the incident matrix of the data points
# param data: data points
# return: The incident matrix of the data
def get_incident_matrix(data):
    # initializes nxn matrix
    incident_matrix = [[[] for _ in range(len(data))] for _ in range(len(data))]

    # creates incident matrix
    for x in range(len(data)):
        for y in range(len(data)):
            if data[x] == data[y] and data[x] != '-1':
                incident_matrix[x][y] = 1
            else:
                incident_matrix[x][y] = 0

    return np.array(incident_matrix)


# This function gets the incident matrix of the ground truth points
# param ground_truth: ground truth points
# return: The incident matrix of the ground truth
def get_ground_truth_matrix(ground_truth):
    # initializes nxn matrix
    ground_truth_matrix = [[[] for _ in range(len(ground_truth))] for _ in range(len(ground_truth))]

    # creates incident matrix
    for x in range(len(ground_truth)):
        for y in range(len(ground_truth)):
            if ground_truth[x] == ground_truth[y] and ground_truth[x] != '-1':
                ground_truth_matrix[x][y] = 1
            else:
                ground_truth_matrix[x][y] = 0

    return np.array(ground_truth_matrix)


# This function gets the jaccard index of the clusters
# param incident_matrix: the incident matrix of the data clusters
# param ground_truth_matrix: the incident matrix of the ground truth clusters
# return: The jaccard index of the clusters
def get_jaccard_index(incident_matrix, ground_truth_matrix):
    ss = 0
    sd = 0
    ds = 0
    dd = 0
    for i in range(len(incident_matrix) - 1):
        for j in range(1, len(incident_matrix)):
            if incident_matrix[i][j] == 1 and ground_truth_matrix[i][j] == 1:
                ss += 1
            elif incident_matrix[i][j] == 1 and ground_truth_matrix[i][j] == 0:
                sd += 1
            elif incident_matrix[i][j] == 0 and ground_truth_matrix[i][j] == 1:
                ds += 1
            else:
                dd += 1
    return ss / (ss + sd + ds)


# This function writes the jaccard index to the output file
# param filename: name of output file
# param jaccard_index: jaccard index of the clusters
# return: none
def output_to_file(filename, jaccard_index):
    file = open(filename, 'w')
    file.write('jaccard index = ' + str(jaccard_index))
    file.close()


def main():
    input_filename = 'assignment3_output_clusters.txt'
    data = get_input_data(input_filename)
    ground_truth = get_ground_truth('assignment3_input.txt')
    incident_matrix = get_incident_matrix(data)
    ground_truth_matrix = get_ground_truth_matrix(ground_truth)
    jaccard_index = get_jaccard_index(incident_matrix, ground_truth_matrix)
    output_to_file('assignment3_output.txt', jaccard_index)


if __name__ == "__main__":
    main()