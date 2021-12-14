from collections import Counter
from functools import lru_cache
from toolz import reduce

with open('input.txt') as f:
    data = f.read().splitlines()
"""
data = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''.splitlines()
"""
cur = data.pop(0)
start = cur
data.pop(0)
rule = {(a[0],a[1]):b for line in data for a,b in [line.split(' -> ')]}

def step(cur):
    ans = ''
    for i,c in enumerate(cur[:-1]):
        ans += c + rule[c, cur[i+1]]
    return ans + cur[-1]

for i in range(10):
    cur = step(cur)
    
counts = Counter(cur)
print(f'difference of most and least frequent is {max(counts.values()) - min(counts.values())}')

#part 2
@lru_cache(4001)
def freq(a:'str len 1',b:'str len 1',steps:int):
    'return the frequency of each letter after steps steps'
    if steps == 0:
        return Counter(a+b)
    return {val:freq(a,rule[a,b],steps -1)[val]
            + freq(rule[a,b],b,steps -1)[val]
            - (1 if val == rule[a,b] else 0)
            for val in 'BCFHKNOPSV'}

counts40 = reduce(lambda a,b:{val:a[val] + b[val] for val in 'BCFHKNOPSV'},[freq(x,y,40) for x,y in zip(start,start[1:])])
for val in start[1:-1]:
    counts40[val] -= 1 #remove double count
counts40 = {k:v for k,v in counts40.items() if v > 0}
print(f'difference of most and least frequent is {max(counts40.values()) - min(counts40.values())}')
