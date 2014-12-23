from copy import deepcopy
import sys

def mark(arr, i, j):
    narr = deepcopy(arr)
    narr[i][j] -= 1
    if i > 0:
        narr[i-1][j] -= 1
        if j > 0:
            narr[i-1][j-1] -= 1
        if j < len(arr[0]) - 1:
            narr[i-1][j+1] -= 1
    if i < len(arr) - 1:
        narr[i+1][j] -= 1
        if j > 0:
            narr[i+1][j-1] -= 1
        if j < len(arr[0]) - 1:
            narr[i+1][j+1] -= 1
    if j > 0:
        narr[i][j-1] -= 1
    if j < len(arr[0]) - 1:
        narr[i][j+1] -= 1
    return narr

def markS(arr, i, j):
    narr = deepcopy(arr)
    narr[i][j] = True
    return narr

def isSolved(arr):
    temp = 0
    for i in range(len(arr)):
        temp = temp + sum(arr[i])
    return temp == 0

def recrsSolve(arr, sol):
    if isSolved(arr):
        return arr, sol

    x = len(arr)
    y = len(arr[0])
    for i in range(x):
        for j in range(y):
            if (i == 0 or j == 0 or arr[i-1][j-1] > 0) and \
               (i == 0 or j == y - 1 or arr[i-1][j+1]) and \
               (i == 0 or arr[i-1][j] > 0) and \
               (j == 0 or arr[i][j-1] > 0) and \
               (i == x - 1 or j == y - 1 or arr[i+1][j+1] > 0) and \
               (i == x - 1 or j == 0 or arr[i+1][j-1] > 0) and \
               (i == x - 1 or arr[i+1][j] > 0) and \
               (j == y - 1 or arr[i][j+1] > 0):
                temparr = mark(arr, i, j)
                tempsol = markS(sol, i, j)
                z = recrsSolve(temparr, tempsol)
                if z:
                    resa, ress = z
                    if isSolved(resa):
                        return resa, ress
    return None

def solver(arr):
    x = len(arr)
    y = len(arr[0])

    sol = [[False for i in range(y)] for j in range(x)]
    ans = recrsSolve(arr, sol)
    if ans:
        a, s = ans
        for row in s:
            for cell in row:
                if cell:
                    sys.stdout.write('X')
                else:
                    sys.stdout.write('_')
            print ""
    else:
        print "No solution!"

puzzle = [[2, 3, 2], [3, 5, 3], [2, 3, 2]]
solver(puzzle)
