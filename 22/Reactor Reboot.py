
with open('input.txt') as f:
    data = [line.split() for line in f.read().splitlines()]
for i,(a,b) in enumerate(data):
    data[i] = [a,{chunk.split('=')[0]:[int(x) for x in chunk.split('=')[1].split('..')]
                  for chunk in b.split(',')}]

def test(x,y,z): #brute
    for d in data[::-1]:
        if (d[1]['x'][0] <= x <= d[1]['x'][1] and
            d[1]['y'][0] <= y <= d[1]['y'][1] and
            d[1]['z'][0] <= z <= d[1]['z'][1]):
            return 1 if d[0] == 'on' else 0
    return 0

print(f'in center 50s {sum([test(x,y,z) for x in range(-50,51) for y in range(-50,51) for z in range(-50,51)])}')

def intersect(d1,d2) -> dict:
    return {'x':(max(d1['x'][0],d2['x'][0]),min(d1['x'][1],d2['x'][1])),
            'y':(max(d1['y'][0],d2['y'][0]),min(d1['y'][1],d2['y'][1])),
            'z':(max(d1['z'][0],d2['z'][0]),min(d1['z'][1],d2['z'][1]))}

def volume(d):
    if d['x'][0] > d['x'][1] or d['y'][0] > d['y'][1] or d['z'][0] > d['z'][1]:
        return 0
    return ((d['x'][1] - d['x'][0] + 1) *
            (d['y'][1] - d['y'][0] + 1) *
            (d['z'][1] - d['z'][0] + 1))

recs = {(i,):b for i,(a,b) in enumerate(data) if a == 'on'}
int_ct = 1
cur = [k for k in recs if len(k) == int_ct]
while cur:
    for k in cur:
        for i,(a,b) in enumerate(data):
            if i > k[-1] and volume(intersect(recs[k],b)) > 0:
                recs[(*k,i)] = intersect(recs[k],b)
    int_ct += 1
    cur = [k for k in recs if len(k) == int_ct]
ans = 0
for i in range(1,int_ct):
    ans += sum([volume(d) for k,d in recs.items() if len(k) == i]) * (1 if i%2 == 1 else -1)
        
print(f'part 2: {ans}')











