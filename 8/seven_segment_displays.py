with open('input.txt') as f:
    data = f.read().splitlines()

lines = [[[word for word in side.split()]
          for side in d.split('|')]
         for d in data]

print(f'''There are {len([word for line in lines for word in line[1] if len(word) in (2,4,3,7)])} instances of 1, 4, 7, or 8 in the output''')

#part 2
def decode(line: list,output: list):
    'line contains one instance of each number'
    n1 = [x for x in line if len(x) == 2][0]
    n4 = [x for x in line if len(x) == 4][0]
    n7 = [x for x in line if len(x) == 3][0]
    n8 = [x for x in line if len(x) == 7][0]
    n9 = [x for x in line if len(x) == 6 and all(v in x for v in n4)][0]
    n6 = [x for x in line if len(x) == 6 and not all(v in x for v in n1)][0]
    n0 = [x for x in line if len(x) == 6 and x not in (n9,n6)][0]
    n3 = [x for x in line if len(x) == 5 and all(v in x for v in n1)][0]
    n2 = [x for x in line if len(x) == 5 and
          len([v for v in n4 if v in x]) == 2][0]
    n5 = [x for x in line if len(x) == 5 and x not in (n3,n2)][0]
    d = {''.join(sorted(v)):str(i) for i,v in
         enumerate((n0,n1,n2,n3,n4,n5,n6,n7,n8,n9))}
    return int(''.join([d[''.join(sorted(v))] for v in output]))
    
print(f'sum all output {sum([decode(*line) for line in lines])}')
