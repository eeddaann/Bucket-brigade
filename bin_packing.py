from pulp import *
import numpy as np
import csv

with open("data/6p.csv", "r") as f:
    reader = csv.reader(f)
    a = list(reader)
items = []
for lst in a:
    tmp = map(int, lst)
    items.append((str(tmp), sum(tmp)))

itemCount = len(items)
maxBins = itemCount
binCapacity = ([60] * maxBins)
binCost = [10] * maxBins

y = pulp.LpVariable.dicts('BinUsed', range(maxBins), lowBound=0, upBound=1, cat=pulp.LpInteger)
possible_ItemInBin = [(itemTuple[0], binNum) for itemTuple in items for binNum in range(maxBins)]
x = pulp.LpVariable.dicts('itemInBin', possible_ItemInBin, lowBound=0, upBound=1, cat=pulp.LpInteger)

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

print("Bins used: " + str(sum(([y[i].value() for i in range(maxBins)]))))
d = {}
for i in x.keys():
    if x[i].value() == 1:
        print("Vector {} is packed in bin {}.".format(*i))
        if i[1] in d:
            d[i[1]] += np.array(eval(i[0]))
        else:
            d[i[1]] = np.array(eval(i[0]))
for key in d:
    print str(key) + ": " + str(d[key])
    print "sum: " + str(sum(d[key]))
    print "std: " + str(np.std(d[key]))
    print "mean: " + str(np.mean(d[key]))
    print "median: " + str(np.median(d[key]))
