import time
import sys
start = time.time()

def formatprint(p):
    for i in range(0, 73, 9):
        print(" ".join( [p[j] for j in range(i,i+9)] ))
    print()

def getbox(tl, br):
    return {9*c + r for c in range(tl[0], br[0]) \
            for r in range(tl[1], br[1])}

groups = [set(range(9*k, 9*k+9)) for k in range(9)] + \
         [set(range(k, k+73,9)) for k in range(9)] + \
         [getbox( (tlc, tlr), (tlc+3, tlr+3)) \
         for tlc in [0,3,6] for tlr in [0,3,6]]

mapping = [set() for i in range(81)]
mygroups = [[] for i in range(81)]

for group in groups:
    for val in group:
        mapping[val] = (mapping[val] | group) - {val}
        mygroups[val].append(group)

symbols = "123456789"

def initialize(p):
    possmapping = {i : symbols for i in range(81)}
    for i,symbol in enumerate(p):
        if symbol != ".":
            place(possmapping, symbol, i)
    return possmapping
def place(possmapping, symbol, index):
    return possmapping if all((makeDeductions(possmapping, sym, index) \
            for sym in symbols if sym != symbol)) else False

def makeDeductions(possmapping, symbol, index):
    if symbol not in possmapping[index]:
        return possmapping
    possmapping[index] = possmapping[index].replace(symbol, '')
    if len(possmapping[index]) == 0 or (len(possmapping[index]) == 1 \
       and not all((makeDeductions(possmapping, possmapping[index], neighbor) \
       for neighbor in mapping[index]))):
        
       return False
   
    for group in mygroups[index]:
        positions = []
        for i in group:
            if symbol in possmapping[i]:
                positions.append(i)
                if len(positions) > 1:
                    break
        if len(positions) == 0 or (len(positions) == 1 and not \
                place(possmapping, symbol, positions[0])):
            
            return False
    return possmapping

def bruteForce(possmapping):
    isInvalid = lambda p: not p 
    isSolved = lambda p : all(len(p[i]) == 1 for i in p) 
    if isInvalid(possmapping): 
        return False
    if isSolved(possmapping): 
        return possmapping

    bestposition = None
    minlen = 10
    for i in range(81):
        if len(possmapping[i]) > 1 and len(possmapping[i]) < minlen:
            minlen = len(possmapping[i])
            bestposition = i

    if minlen > 2:
        bestsymbol = None
        bestpositions = [0]*10
        for symbol in symbols:
            for group in groups:
                positions = [i for i in group if symbol in \
                            possmapping[i] and len(possmapping[i]) > 1]
                if len(positions) > 1 and len(positions) < len(bestpositions):
                    bestsymbol = symbol
                    bestpositions = positions
        if bestsymbol and len(bestpositions) < minlen:
            for pos in bestpositions:
                sol = bruteForce(place(possmapping.copy(), bestsymbol, pos))
                if sol:
                    return sol
            return False
    for sym in possmapping[bestposition]:
        sol = bruteForce(place(possmapping.copy(), sym, bestposition))
        if sol:
            return sol
    return False

if __name__ == "__main__":
    
    path = "puzzle.txt"

    if len(sys.argv) > 1:
        path = sys.argv[1]

    f = open(path, "r")

    for i, line in enumerate(f):
        puzzle = line.strip()
        print("Puzzle:")
        formatprint(puzzle)
        print("Solved:")
        formatprint(bruteForce(initialize(puzzle)))

    print(time.time()-start, "seconds")

