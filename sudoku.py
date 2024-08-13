import numpy as np
from pulp import *

def solve_sudoku(puzzle):
    I = range(1, 10)
    J = range(1, 10)
    K = range(1, 10)
    C = range(1, 10)

    celle = {
        1: [range(1, 4), range(1, 4)],
        2: [range(1, 4), range(4, 7)],
        3: [range(1, 4), range(7, 10)],
        4: [range(4, 7), range(1, 4)],
        5: [range(4, 7), range(4, 7)],
        6: [range(4, 7), range(7, 10)],
        7: [range(7, 10), range(1, 4)],
        8: [range(7, 10), range(4, 7)],
        9: [range(7, 10), range(7, 10)]
    }

    model = LpProblem("Sudoku", LpMinimize)
    x = LpVariable.dicts("x", (I, J, K), cat="Binary")

    model += 1, "FO"

    # Each cell must have only one number
    for i in I:
        for j in J:
            model += lpSum(x[i][j][k] for k in K) == 1, f"Cell {i} {j}"

    # A number can only appear once in a row
    for i in I:
        for k in K:
            model += lpSum(x[i][j][k] for j in J) == 1, f"Row {i}, nr. {k}"

    # A number can only appear once in a column
    for j in J:
        for k in K:
            model += lpSum(x[i][j][k] for i in I) == 1, f"Column {j}, nr. {k}"

    # A number can only appear once in a cell
    for c in C:
        range_i = celle[c][0]
        range_j = celle[c][1]
        for k in K:
            model += lpSum(x[i][j][k] for i in range_i for j in range_j) == 1, f"Cell {c}, nr. {k}"

    # Addition of starting numbers in the template
    for i in I:
        for j in J:
            if puzzle[i-1][j-1] != 0:
                model += x[i][j][puzzle[i-1][j-1]] == 1

    model.solve()

    M = np.zeros((len(I), len(J)))
    for i in I:
        for j in J:
            for k in K:
                if x[i][j][k].varValue == 1:
                    M[i-1, j-1] = k
    return M.astype(int).tolist()