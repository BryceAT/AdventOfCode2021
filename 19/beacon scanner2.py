from collections import defaultdict
from toolz import reduce

def dist2(p:tuple,q:tuple) -> int:
    return (p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2
def dist_mad(p,q) -> int:
    return abs(p[0]-q[0]) + abs(p[1]-q[1]) + abs(p[2]-q[2]) 
def instersect(list1,list2) -> int:
    'count of numbers that appear on both list1 and list2'
    st = set(list1)
    return len([x for x in list2 if x in st])
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
def get_orient(k1,k2, invert = False) -> 'orientation function':
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
            if invert and dir_test([scan[k2][p2] for p1,p2 in pairs[k1,k2].items()],
                        [scan_unknown[k1][p1] for p1,p2 in pairs[k1,k2].items()],
                        lambda x:perm(*flip(*x))):
                return lambda x:perm(*flip(*x))
            elif not invert and dir_test([scan[k1][p1] for p1,p2 in pairs[k1,k2].items()],
                        [scan_unknown[k2][p2] for p1,p2 in pairs[k1,k2].items()],
                        lambda x:perm(*flip(*x))):
                return lambda x:perm(*flip(*x))
def get_translate(k1,k2, invert = False) -> 'translation function after orientation':
    p1 = list(pairs[k1,k2].keys())[0]
    p2 = pairs[k1,k2][p1]
    if not invert: # move p2 to p1
        return lambda x: (x[0] + scan[k1][p1][0] - scan[k2][p2][0],
                          x[1] + scan[k1][p1][1] - scan[k2][p2][1],
                          x[2] + scan[k1][p1][2] - scan[k2][p2][2])
    elif invert: # move p1 to p2
        return lambda x: (x[0] - scan[k1][p1][0] + scan[k2][p2][0],
                          x[1] - scan[k1][p1][1] + scan[k2][p2][1],
                          x[2] - scan[k1][p1][2] + scan[k2][p2][2])
        
            
if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()
    scan = defaultdict(list)
    scan_unknown = defaultdict(list)
    for line in data:
        if line.startswith('---'):
            scan_num = int(line.replace('---','').split()[-1])
        elif line == '':
            pass
        elif scan_num == 0:
            scan[scan_num].append(tuple([int(x) for x in line.split(',')]))
        else:
            scan_unknown[scan_num].append(tuple([int(x) for x in line.split(',')]))
    dists = {0:[[dist2(p,q) for q in scan[0]] for p in scan[0]]}
    for k,v in scan_unknown.items():
        dists[k] = [[dist2(p,q) for q in v] for p in v]
    guess = {}
    for k1,v1 in dists.items():
        for k2,v2 in dists.items():
            guess[k1,k2] = {}
            if k2 > k1:
                cur = [[instersect(p,q) for q in v2] for p in v1]
                for i, row in enumerate(cur):
                    mr = max(row)
                    if mr >= 12:
                        guess[k1,k2][i] = row.index(mr)
    #pairs[k1,k2] = list of pairs (i,j) such that j on scan k1 maps to i on scan k2 
    pairs = {k:v for k,v in guess.items() if v}
    scanner_loc = [(0,0,0)]
    while scan_unknown:
        for k1,k2 in pairs:
            if k1 in scan and k2 in scan_unknown:
                f = get_orient(k1,k2)
                scan[k2] = [f(p) for p in scan_unknown.pop(k2)]
                g = get_translate(k1,k2)
                scanner_loc.append(g((0,0,0)))
                scan[k2] = [g(p) for p in scan[k2]]
            elif k2 in scan and k1 in scan_unknown:
                f = get_orient(k1,k2,True)
                scan[k1] = [f(p) for p in scan_unknown.pop(k1)]
                g = get_translate(k1,k2,True)
                scanner_loc.append(g((0,0,0)))
                scan[k1] = [g(p) for p in scan[k1]]
    allpoints = reduce(lambda x,y:x.union(y),scan.values(),set([]))
    print(f'part 1: the total number of points {len(allpoints)}')
    print(f'part 2: max manhattan dist between scanners {max([dist_mad(p,q) for p in scanner_loc for q in scanner_loc])}')
