# Author: John Boyle
# Project: Apriori

from math import ceil
from itertools import combinations

MIN_SUPPORT_PERCENT = 0.035

# This function reads a file under filename and extracts all transactions and a set of distinct items
# param filename: The name of the input file (should provide path if necessary)
# return: A dictionary of transactions and a set of distinct items
def get_input_data(filename):
    input_file = open(filename, 'r')
    transactions = dict()
    # Parses input and picks out the transactions and unique items
    # within those transactions
    itemset = set()
    for line in input_file:
        transaction = line.split()
        transactions[transaction[0]] = transaction[1:]
        for i in transaction[1:]:
            if i not in itemset:
                itemset.add(i)

    return transactions, itemset


# This function calculates support of the itemset from transactions
# param transactions: All transactions in a dictionary
# param itemset: The itemset to calculate support
# return: The support count of the itemset
def support(transactions, itemset):
    support_count = 0

    # Calculates # of occurrences by iterating throught the list
    for i in transactions.values():
        transactionSet = set(i)
        if itemset.issubset(transactionSet):
            support_count += 1

    return support_count


# This function generates a combination from the frequent itemsets of size (itemset_size - 1) and accepts joined itemsets if they share (itemset_size - 2) items
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of joined itemsets
# return: All valid joined itemsets
def generate_selectively_joined_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = list()

    # Case if itemset size is two so every combination
    # of two items is valid
    if itemset_size == 2:
        i = 0
        while i < len(frequent_itemsets[1]) - 1:
            j = i + 1
            while j < len(frequent_itemsets[1]):
                joined_itemsets.append(frequent_itemsets[1][i].union(frequent_itemsets[1][j]))
                j += 1
            i += 1

    # Case if itemset size is greater than two and itemsets must be checked
    # to have common elements before they can be unioned and added to the candidates
    else:
        i = 0
        while i < len(frequent_itemsets[itemset_size - 1]) - 1:
            j = i + 1
            while j < len(frequent_itemsets[itemset_size - 1]):
                if len(frequent_itemsets[itemset_size - 1][i].union(frequent_itemsets[itemset_size - 1][j])) == itemset_size:
                    if frequent_itemsets[itemset_size - 1][i].union(frequent_itemsets[itemset_size - 1][j]) not in joined_itemsets:
                        joined_itemsets.append(frequent_itemsets[itemset_size - 1][i].union(frequent_itemsets[itemset_size - 1][j]))
                j += 1
            i += 1

    return joined_itemsets


# This function checks all the subsets of selected itemsets whether they all are frequent or not and prunes the itemset if anyone of the subsets is not frequent
# param selected_itemsets: The itemsets which are needed to be checked
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: The itemsets whose all subsets are frequent
def apply_apriori_pruning(joined_itemsets, frequent_itemsets, itemset_size):

    # Generates all combinations of size - 1 itemsets for each itemset and prunes
    # if any of those itemsets are not frequent
    for i in joined_itemsets:
        subSets = list(combinations(list(i), itemset_size - 1))
        j = 0
        while j < len(subSets):
            if set(subSets[j]) in frequent_itemsets[itemset_size - 1]:
                j += 1
            else:
                j = len(subSets)
                joined_itemsets.remove(i)

    return joined_itemsets


# This function generates candidate itemsets of size (itemset_size) by selective joining and apriori pruning
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: candidate itemsets formed by selective joining and apriori pruning
def generate_candidate_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = generate_selectively_joined_itemsets(frequent_itemsets, itemset_size)
    candidate_itemsets = apply_apriori_pruning(joined_itemsets, frequent_itemsets, itemset_size)
    return candidate_itemsets


# This function generates a table of itemsets with all frequent items from transactions based on a given minimum support
# param transactions: The transactions based upon which support is calculated
# param items: The unique set of items present in the transaction
# param min_support: The minimum support to find frequent itemsets
# return: The table of all frequent itemsets of different sizes
def generate_all_frequent_itemsets(transactions, items, min_support):
    frequent_itemsets = dict()
    itemset_size = 0
    frequent_itemsets[itemset_size] = list()
    frequent_itemsets[itemset_size].append(frozenset())

    # Frequent itemsets of size 1
    itemset_size += 1
    frequent_itemsets[itemset_size] = list()

    for i in items:
        if support(transactions, {i}) >= min_support:
            frequent_itemsets[itemset_size].append({i})

    # frequent itemsets of greater size
    itemset_size += 1

    while frequent_itemsets[itemset_size - 1]:
        frequent_itemsets[itemset_size] = list()
        candidate_itemsets = generate_candidate_itemsets(frequent_itemsets, itemset_size)
        pruned_itemset = list()

        # If the support for a candidate itemset is greater than the minimum support,
        # it is a frequent itemset so it is added to the list
        for i in candidate_itemsets:
            if support(transactions, i) >= min_support:
                pruned_itemset.append(i)

        frequent_itemsets[itemset_size] = pruned_itemset
        itemset_size += 1
    return frequent_itemsets


# This function writes all frequent itemsets along with their support to the output file with the given filename
# param filename: The name for the output file
# param frequent_itemsets_table: The dictionary which contains all frequent itemsets
# param transactions: The transactions from which the frequent itemsets are found
# return: void
def output_to_file(filename, frequent_itemsets_table, transactions):
    file = open(filename, 'w')

    # Prints all frequent itemsets  for each size itemset and formats output to
    # match the required specifications
    for i in frequent_itemsets_table:
        if i > 1:
            for j in frequent_itemsets_table[i]:
                data = str(j)
                data = data.replace("'","")
                file.write(data + " " + "%.2f" % (support(transactions, j)/len(transactions)*100) + "% support\n")

    file.close()


# The main function
def main():
    input_filename = 'assignment1_input.txt'
    output_filename = 'result.txt'
    cellular_functions, genes_set = get_input_data(input_filename)
    min_support = ceil(MIN_SUPPORT_PERCENT * len(cellular_functions))
    frequent_itemsets_table = generate_all_frequent_itemsets(cellular_functions, genes_set, min_support)
    output_to_file(output_filename, frequent_itemsets_table, cellular_functions)


if __name__ == '__main__':
    main()