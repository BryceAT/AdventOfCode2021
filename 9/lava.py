with open('input.txt') as f:
    data = [[int(x) for x in row] for row in f.read().splitlines()]
    
ct = 0
len_data = len(data) - 1
len_row = len(data[0]) - 1
for r,row in enumerate(data):
    for c,x in enumerate(row):
        if ((r == 0 or data[r - 1][c] > x) and
            (r == len_data or data[r + 1][c] > x) and
            (c == 0 or data[r][c - 1] > x) and
            (c == len_row or data[r][c + 1] > x)):
            ct += x + 1
print(f'sum + count of points is {ct}')

bump = {'left':lambda x,y: (x -1,y) if x > 0 else (x,y),
        'up':lambda x,y: (x,y - 1) if y > 0 else (x,y),
        'right':lambda x,y: (x +1,y) if x < len_data else (x,y),
        'down':lambda x,y: (x, y + 1) if y < len_row else (x,y)}
def flood(i,j,ct = 1):
    data[i][j] = 9
    for x,y in [f(i,j) for d,f in bump.items()]:
        if data[x][y] != 9:
            ct = flood(x,y,ct + 1)
    return ct

ans = []

for i in range(len(data)):
    for j in range(len(data[0])):
        if data[i][j] != 9:
            ans.append(flood(i,j))
a,b,c = sorted(ans)[-3:]
print(f'product of areas of largest 3 basins is {a * b * c}')
