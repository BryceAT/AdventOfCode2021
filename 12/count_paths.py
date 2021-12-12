from collections import Counter

with open('input.txt') as f:
    data = [d.split('-') for d in f.read().splitlines()]
    
big = [cave for pair in data for cave in pair if cave[0] == cave[0].upper()]

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

#part 2
def dfs2(path, ct = 0):
    for a,b in data:
        counts = Counter([c for c in path if c not in big])
        if (a == path[-1]
            and b != 'start'
            and max(counts.values()) <= 2
            and Counter(counts.values())[2] < 2):
            if b == 'end':
                ct += 1
            else:
                ct = dfs2(path + [b], ct)
    return ct
print(f"path count with double_small {dfs2(['start'])}")
