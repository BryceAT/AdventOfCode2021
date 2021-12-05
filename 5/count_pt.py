from collections import defaultdict
with open('input.txt') as f:
    data = f.read().splitlines()


class Visited:
    visited = defaultdict(int)
    ct = 0
    def visit(self,x,y) -> None:
        self.visited[x,y] += 1
        if self.visited[x,y] == 2:
            self.ct += 1

V = Visited()

for line in data:
    x1,y1,x2,y2 = [int(x) for pt in line.split('->') for x in pt.split(',')]
    if x1 == x2:
        for k in range(min(y1,y2),max(y1,y2) + 1):
            V.visit(x1,k)
    elif y1 == y2:
        for k in range(min(x1,x2),max(x1,x2) + 1):
            V.visit(k,y1)
print(f'There are {V.ct} dangerous points only horizontal and vertical')

#part 2
for line in data:
    x1,y1,x2,y2 = [int(x) for pt in line.split('->') for x in pt.split(',')]
    if x1 != x2 and y1 != y2:
        sgn_x,sgn_y = 1 if x1 < x2 else -1, 1 if y1 < y2 else -1
        for xk,yk in zip(range(x1,x2 + sgn_x,sgn_x),range(y1,y2 +sgn_y,sgn_y)):
            V.visit(xk,yk)
print(f'There are {V.ct} dangerous points including diagonals')
