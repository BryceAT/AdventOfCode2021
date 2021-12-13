with open('input.txt') as f:
    data = f.read().splitlines()

instructions = []
i = 0
while i < len(data):
    if data[i] == '':
        data.pop(i)
    elif data[i].startswith('fold'):
        instructions.append(data.pop(i))
    else:
        i += 1
instructions = [(ins.split('=')[0][-1],int(ins.split('=')[-1])) for ins in instructions]    
data = [[int(a) for a in line.split(',')] for line in data ]

def fold(direction,val):
    global data
    if direction == 'x':
        data = set([(x, y) for x, y in data if x < val] + [((2 * val) - x, y) for x, y in data if x > val])
        return None
    if direction == 'y':
        data = set([(x, y) for x, y in data if y < val] + [(x, (2 * val) - y) for x, y in data if y > val])
        return None
fold(*instructions.pop(0))
print(len(data))
#part 2
while instructions:
    fold(*instructions.pop(0))

max_y = max([y for x,y in data])
max_x = max([x for x,y in data])
out = [''.join([('#' if (x,y) in data else ' ')  for x in range(max_x + 1)]) for y in range(max_y + 1)]
for row in out:
    print(row)
