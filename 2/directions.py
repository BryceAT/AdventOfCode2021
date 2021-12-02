import pandas as pd
df = pd.read_csv('input.txt',sef = ' ')
grp = df.groupby('face').sum()
print((grp.loc['down'] - grp.loc['up']) * grp.loc['forward'])

aim, horizontal, depth = 0,0,0
for face,amt in df.values:
    if face == 'forward':
        horizontal += amt
        depth += aim * amt
    elif face == 'down':
        aim += amt
    else:
        aim -= amt
print(horizontal * depth)
    
