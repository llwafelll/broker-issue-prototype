import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
import itertools as it

# Unit transportation costs
costs = np.array([
        [8, 14, 17],
        [12, 9, 19]
    ]
)

# Popyt i podaż dla odbiorców O1, O2... o dostawców D1, D2, ...
supply = np.array([20, 30]) # podaż
demand = np.array([10, 28, 27])  #popyt 

# Handling unbalanced scenario (fictional supplier/receiver)
profit = np.array([])
if (demand_sum := demand.sum()) != (supply_sum := supply.sum()):
    supply = np.append(supply, [demand_sum])
    demand = np.append(demand, [supply_sum])
    profit = np.zeros((supply.size, demand.size))


# Koszty zakupów / Cena sprzedaży
order_costs = np.array([10, 12])
sell_costs = np.array([30, 25, 30])

SHAPE = costs.shape
# SIZE = costs.shape[0]

transportation = np.zeros((supply.size, demand.size))

# List of tuples (x, y) which describes position allowed to read
path: list[tuple] = []

# Zysk jednostkowy
if profit.size == 0:
    profit = np.zeros(SHAPE)

for i, j in it.product(range(SHAPE[0]), range(SHAPE[1])):
    profit[i, j] = sell_costs[j] - order_costs[i] - costs[i, j]
    
d, s = 0, 0
# supply, demand
profit_sorted = np.argsort(np.absolute(profit), axis=1).tolist()
while(True):
    if supply[s] != 0:
#         print(d)
        d = profit_sorted[s].pop() 
        if demand[d] == 0:
            continue
        path.append((s, d))
        
        if demand[d] >= supply[s]:
            demand[d] -= supply[s]
            transportation[s, d] = supply[s]
            supply[s] = 0
            
#             path.append((d, s))
            
        else:
            supply[s] -= demand[d]
            transportation[s, d] = demand[d]
            demand[d] = 0

#             path.append((d, s))

    else:
        s += 1

    if s >= supply.size:
        break

assert False
costs = np.array(
    [[3,  5,  7],
    [12, 10, 9],
    [13, 3,  9]]
)
supply = np.array([20, 40, 90]) # podaż
demand = np.array([50, 70, 30])  #popyt 

SIZE = costs.shape[0]

transportation = np.empty((SIZE, SIZE))

# List of tuples (x, y) which describes position allowed to read
path: list[tuple] = []

# ALGORITHM
d, s = 0, 0
while(True):
    if demand[d] >= supply[s]:
        demand[d] -= supply[s]
        path.append((d, s))
        transportation[path[::-1][0]] = supply[s]
        s += 1
    
    else:
        supply[s] -= demand[d]
        path.append((d, s))
        transportation[path[::-1][0]] = demand[d]
        d += 1
    
    if d == SIZE - 1 and s == SIZE - 1:
        break

O = np.zeros((SIZE,))
D = np.zeros((SIZE,))
sO = np.full((SIZE,), False, dtype=bool) # state O
sO[0] = True
sD = np.full((SIZE,), False, dtype=bool) # state D

c_path = path[:] # copy of path for modification

c = 0 # counter
while(True):
    i, j = c_path[c]
    # If one of the values is True and remaining False
    if sO[i] ^ sD[j]:
        if sO[i]:
            D[j] = -1 * (O[i] + D[j] + costs[i, j])
            sD[j] = True
        else:
            O[i] = -1 * (O[i] + D[j] + costs[i, j])
            sO[i] = True
        c += 1
    
    # If both values are True
    elif sO[i] & sD[j]:
        c_path.append(c_path.pop(c))
    
    # If both values are False
    else:
        print("Error - both values sO[i] and sD[j] contain False value!")
        break

    if c > SIZE:
        break
        