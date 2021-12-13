from collections import Counter

with open('input.txt') as f:
    data = [d.split('-') for d in f.read().splitlines()]
    
big = [cave for pair in data for cave in pair if cave[0] == cave[0].upper()]
small = [cave for pair in data for cave in pair if cave[0] == cave[0].lower()]

#add the reverse direction
data += [[b,a] for a,b in data if [b,a] not in data]
data.sort()
def dfs(path, ct = 0):
    for a,b in data:
        if a == path[-1] and (b not in path or b in big):
            if b == 'end':
                ct += 1
            else:
                ct = dfs(path + [b], ct)
    return ct

print(f"path count {dfs(['start'])}")
not_big = {c:0 for c in small if c not in ('start','end')}

#part 2
def dfs2(cur,counts, ct = 0):
    for a,b in data:
        if (a == cur
            and b != 'start'
            and max(counts.values()) <= 2
            and Counter(counts.values())[2] < 2):
            if b == 'end':
                ct += 1
            elif b in counts:
                ct = dfs2(b,{**counts,b:counts[b]+1}, ct)
            else:                
                ct = dfs2(b,counts, ct)
    return ct
print(f"path count with double_small {dfs2('start',not_big)}")
