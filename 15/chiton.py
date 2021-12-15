with open('input.txt') as f:
    data = [[int(x) for x in row] for row in f.read().splitlines()]
"""
data = [[int(x) for x in row] for row in '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''.splitlines()]
"""
#do down right first to get a bound, good enough
d = [[x for x in row] for row in data] #working copy
for i in range(len(d)):
    for j in range(len(d[0])):
        if i > 0 and j > 0:
            d[i][j] += min(d[i - 1][j],d[i][j - 1])
        elif i > 0:
            d[i][j] += d[i - 1][j]
        elif j > 0:
            d[i][j] += d[i][j-1]
        else:
            d[0][0] = 0
print(d[-1][-1])

#part 2
def lowestNext(x:int,y:int,known:dict) -> int or None:
    'return None if no neighbors are known'
    if x == y == 0:
        return 0
    vals = [known.get((a,b), None)
            for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]]
    return min([v for v in vals if v is not None] or [None])
d = [[x for x in row] for row in data]
for i in range(len(d)):
    for j in range(4):
        d[i] += [x%9 +1 for x in d[i][-len(data[0]):]]
for j in range(4):
    d += [[x%9 +1 for x in row] for row in d[-len(data):]]
known = {(0,0):0}
frontier = [(0,1),(1,0)]
rows = len(d) - 1
cols = len(d[0]) - 1
def neighbors(x,y) -> list:
    'list of neighbors'
    return [(a,b) for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
            if 0 <= a <= rows and 0 <= b <= cols]
step = 1
found = []
while (rows,cols) not in known:
    for x,y in frontier:
        lowNeigh = lowestNext(x,y,known)
        if lowNeigh is not None and lowNeigh + d[x][y] == step:
            known[x,y] = step
            found.append((x,y))
            frontier += [n for n in neighbors(x,y)
                         if n not in known
                         and n not in frontier]
    for x,y in found:
        frontier.pop(frontier.index((x,y)))
    found = []
    step += 1
    if step == 4000:
        break
        
print(known[rows,cols])
