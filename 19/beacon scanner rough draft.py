from collections import defaultdict
with open('input.txt') as f:
    data = f.read().splitlines()

scans = defaultdict(list)
for line in data:
    if line.startswith('---'):
        scan_num = int(line.replace('---','').split()[-1])
    elif line == '':
        pass
    else:
        scans[scan_num].append(tuple([int(x) for x in line.split(',')]))
        
def dist2(p:tuple,q:tuple) -> int:
    return (p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2
def instersect(list1,list2) -> int:
    'count of numbers that appear on both list1 and list2'
    st = set(list1)
    return len([x for x in list2 if x in st])

dists = {}
for k,v in scans.items():
    dists[k] = [[dist2(p,q) for q in v] for p in v]

count_hits = {}
for k1,v1 in dists.items():
    for k2,v2 in dists.items():
        if k2 > k1:
            count_hits[k1,k2] = [[instersect(p,q) for q in v2] for p in v1]
#now we have count_hits[k1,k2][i][j] >= 12 is a strong indicator that
#beacon i on scanner k1 is the same as beacon j on scanner k2
guess = {k:{} for k in count_hits}
for k,v in count_hits.items():
    for i, row in enumerate(v):
        mr = max(row)
        guess[k][i] = row.index(mr) if mr >= 12 else -1

#guess[k1,k2][i] = j for some j such that j != -1
#means beacon i on scanner k1 maps to beacon j on scanner k2

pairs = {k:[(i,j) for i,j in v.items() if j != -1] for k,v in guess.items()}
#pairs[k1,k2] = list of pairs (i,j) such that j on scan k1 maps to i on scan k2 if not empty
#then trim pairs to only overlapping scanners (not all scanners overlap)
pairs = {k:v for k,v in pairs.items() if v != []}

def sgn(x):
    if x > 0:
        return 1
    return -1 if x < 0 else 0

def direction(p1,p2):
    return (sgn(p2[0] - p1[0]),sgn(p2[1] - p1[1]),sgn(p2[2] - p1[2]))

def list_directions(l:'list of points') -> 'list of directions for every pair':
    return [direction(p1,p2) for p1 in l for p2 in l]

def dir_test(l1,l2,f) -> bool:
    return all([(x == f(y)) for x,y in zip(list_directions(l1),
                                           list_directions(l2))])
##need to find the change in relative orientation of the scanners before translation
#x,y,z -> z,-x,-y? there are 24 orientations
#since we have a mapping of points we take the first orientation that
#agrees with all of the relative positions of the points in the mapping


def get_orient(k):
    for perm in [lambda x,y,z: (x,y,z),
                 lambda x,y,z: (x,z,y),
                 lambda x,y,z: (y,x,z),
                 lambda x,y,z: (y,z,x),
                 lambda x,y,z: (z,x,y),
                 lambda x,y,z: (z,y,x)]:
        for flip in [lambda x,y,z: (x,y,z),
                     lambda x,y,z: (x,y,-z),
                     lambda x,y,z: (x,-y,z),
                     lambda x,y,z: (x,-y,-z),
                     lambda x,y,z: (-x,y,z),
                     lambda x,y,z: (-x,y,-z),
                     lambda x,y,z: (-x,-y,z),
                     lambda x,y,z: (-x,-y,-z)]:
            if dir_test(*[[scans[k[i]][p[i]] for p in pairs[k]] for i in (0,1)],lambda x:perm(*flip(*x))):
                return lambda x:perm(*flip(*x))
orient = {k:get_orient(k) for k in pairs}        


        
        













