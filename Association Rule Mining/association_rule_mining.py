# Author: John Boyle
# Project: Association Rule Mining

MIN_SUPPORT = 30
MIN_CONFIDENCE = .6
MIN_SIZE = 3


# This function reads a file under filename and extracts all transactions and a set of distinct items
# param filename: The name of the input file (should provide path if necessary)
# return: A list of transactions and a list of distinct items
def get_input_data(filename):
    input_file = open(filename, 'r')
    transactions = list()
    itemset = list()
    for line in input_file:
        transaction = line.split()
        transactionsMod = set()
        for i in range(1, len(transaction) - 1):
            transactionsMod.add('gene' + str(i) + ' ' + transaction[i])
        transactionsMod.add(transaction[len(transaction) - 1])
        transactions.append(transactionsMod)

    for i in range(1, 101):
        itemset.append({'gene' + str(i) + ' Down', 'ColonCancer'})
        itemset.append({'gene' + str(i) + ' Down', 'BreastCancer'})
        itemset.append({'gene' + str(i) + ' UP', 'ColonCancer'})
        itemset.append({'gene' + str(i) + ' UP', 'BreastCancer'})

    return transactions, itemset


# This function prunes itemsets that dont meet minimum support
# param transactions: The list of transactions
# return: A list of transactions and a list of distinct items
def prune_itemsets(transactions, itemsets):
    newItemsets = []
    for i in itemsets:
        if get_support(transactions, i) >= MIN_SUPPORT:
            newItemsets.append(i)
    return newItemsets


# This function calculates support of the itemset from transactions
# param transactions: The list of transactions
# param itemset: The itemset to calculate support
# return: The support count of the itemset
def get_support(transactions, itemset):
    support = 0
    for j in transactions:
        if j.issuperset(itemset):
            support += 1
    return support


# This function creates candidate itemsets from the current frequent itemsets
# param size: size of candidate itemsets
# param itemsets: The current frequent itemsets
# return: the candidate itemsets
def create_candidate_itemsets(itemsets, size):
    candidates = []
    for i in itemsets:
        for j in itemsets:
            if len(i.union(j)) == size:
                candidate = i.union(j)
                if (len(candidate.intersection({'BreastCancer'})) > 0 or len(
                        candidate.intersection({'ColonCancer'})) > 0) and not (
                        len(candidate.intersection({'BreastCancer'})) > 0 and
                        len(candidate.intersection({'ColonCancer'})) > 0):
                    if candidate not in candidates:
                        candidates.append(candidate)
    return candidates


# This function mines the rules of the frequent itemsets
# param transactions: The list of transactions
# param itemset: The itemset to calculate support
# return: the association rules
def association_mine(transactions, itemsets):
    rules = []
    for i in itemsets:
        if i.issuperset({'BreastCancer'}):
            supportWith = get_support(transactions, i)
            i.remove('BreastCancer')
            supportWithout = get_support(transactions, i)
            confidence = supportWith / supportWithout
            if confidence >= MIN_CONFIDENCE:
                rules.append([i, {'BreastCancer'}, supportWith, confidence])
            i.add('BreastCancer')
        elif i.issuperset({'ColonCancer'}):
            supportWith = get_support(transactions, i)
            i.remove('ColonCancer')
            supportWithout = get_support(transactions, i)
            confidence = supportWith / supportWithout
            if confidence >= MIN_CONFIDENCE:
                rules.append([i, {'ColonCancer'}, supportWith, confidence])
            i.add('ColonCancer')

    return rules


# This function writes all association rules along with their support and confidence to the output file with the
# given filename
# param filename: The name for the output file
# param association_rules: The association rules of the transactions
# return: void
def output_to_file(filename, association_rules):
    file = open(filename, 'w')

    # Prints all frequent itemsets  for each size itemset and formats output to
    # match the required specifications
    for j in association_rules:
        for i in j:
            file.write(str(i[0]) + " -> " + str(i[1]) + " support: " + str(i[2]) + "% confidence: " + str(
                format(i[3] * 100, '.2f')) + "%\n")

    file.close()


# This function mines the rules of all the frequent itemsets
# param transactions: The list of transactions
# param itemset: The itemset to calculate support
# param min_size: The minimum size of frequent itemset
# return: the association rules
def get_association_rules(transactions, itemsets, min_size):
    pruned_candidates = prune_itemsets(transactions, itemsets)
    size = min_size
    association_rules = []
    while len(create_candidate_itemsets(pruned_candidates, size)) > 0:
        candidates = create_candidate_itemsets(pruned_candidates, size)
        pruned_candidates = prune_itemsets(transactions, candidates)
        association_rules.append(association_mine(transactions, pruned_candidates))
        size += 1
    return association_rules


# The main function
def main():
    input_filename = 'assignment4_input.txt'
    output_filename = 'result.txt'
    transactions, itemsets = get_input_data(input_filename)
    association_rules = get_association_rules(transactions, itemsets, MIN_SIZE)
    output_to_file(output_filename, association_rules)


if __name__ == '__main__':
    main()
