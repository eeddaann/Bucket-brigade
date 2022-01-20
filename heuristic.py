from pulp import *
import numpy as np
import csv


def pack(capacity, picksize):
    '''
    optimizes the batching process
    :param capacity: how many items each picker can take
    :param picksize: how many pick faces exists 
    :return: optimal solution for the batching problem
    '''
    with open("data/" + str(picksize) + "p.csv", "r") as f:
        reader = csv.reader(f)
        a = list(reader)
    items = []
    for lst in a:
        tmp = list(map(int, lst))
        items.append((str(tmp), sum(tmp)))

    itemCount = len(items)
    maxBins = itemCount
    binCapacity = ([capacity] * maxBins)
    binCost = [10] * maxBins

    y = pulp.LpVariable.dicts('BinUsed', list(range(maxBins)), lowBound=0, upBound=1, cat='Integer')
    possible_ItemInBin = [(itemTuple[0], binNum) for itemTuple in items for binNum in range(maxBins)]
    x = pulp.LpVariable.dicts('itemInBin', possible_ItemInBin, lowBound=0, upBound=1, cat='Integer')

    # Model formulation
    prob = LpProblem("Bin Packing Problem", LpMinimize)

    # Objective
    prob += lpSum([binCost[i] * y[i] for i in range(maxBins)])

    # Constraints
    # each item should be packed to only one bin
    for j in items:
        prob += lpSum([x[(j[0], i)] for i in range(maxBins)]) == 1
    # volume constraint
    for i in range(maxBins):
        prob += lpSum([items[j][1] * x[(items[j][0], i)] for j in range(itemCount)]) <= binCapacity[i] * y[i]
    prob.solve(PULP_CBC_CMD(fracGap=0.00001, maxSeconds=60, threads=None))

    d = {}
    for i in list(x.keys()):
        if x[i].value() == 1:
            print(("Vector {} is packed in bin {}.".format(*i)))
            if i[1] in d:
                d[i[1]] += np.array(eval(i[0]))
            else:
                d[i[1]] = np.array(eval(i[0]))
    ordered = [list(d.values())[i] for i in solve_tsp_dynamic(list(d.values()))]
    for key in d:
        print("bin "+str(key) + ": " + str(d[key]))
    for i in range(len(ordered)):
        print(("batch "+str(i) + ": " + str(ordered[i]) + " sum: " + str(sum(ordered[i]))))
    return ordered

def euclidean(x,y):
    return np.sum(np.abs(x - y))

def chebyshev(x,y):
    return np.max(np.abs(x - y))

def solve_tsp_dynamic(points,distance=euclidean):
    '''
    solving n-dim TSP problem
    :param points: cities or batches in this context
    :param distance: distance metric
    :return: 
    '''
    # adopted from: https://gist.github.com/mlalevic/6222750
    # calc all lengths
    all_distances = [[distance(x,y) for y in points] for x in points]
    # initial value - just distance from 0 to every other point + keep the track of edges
    A = {(frozenset([0, idx + 1]), idx + 1): (dist, [0, idx + 1]) for idx, dist in enumerate(all_distances[0][1:])}
    cnt = len(points)
    for m in range(2, cnt):
        B = {}
        for S in [frozenset(C) | {0} for C in itertools.combinations(list(range(1, cnt)), m)]:
            for j in S - {0}:
                B[(S, j)] = min([(A[(S - {j}, k)][0] + all_distances[k][j], A[(S - {j}, k)][1] + [j]) for k in S if
                                 k != 0 and k != j])  # this will use 0th index of tuple for ordering, the same as if key=itemgetter(0) used
        A = B
    res = min([(A[d][0] + all_distances[0][d[1]], A[d][1]) for d in iter(A)])
    return res[1]

