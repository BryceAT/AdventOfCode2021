with open('input.txt') as f:
    data = f.read().splitlines()

points = {')':3,
          ']':57,
          '}':1197,
          '>':25137,
          0:0}
pair = {'(':')','{':'}','[':']','<':'>'}

def first_wrong(line):
    stack = []
    for c in line:
        if c in pair:
            stack.append(pair[c])
        elif stack[-1] == c:
            stack.pop()
        else:
            return c
    return 0
print(f'score is {sum([points[first_wrong(line)] for line in data])}')

#part 2
points = {')':1,
          ']':2,
          '}':3,
          '>':4}
def scorer(comp):
    if type(comp) == str:
        return 0
    ans = 0
    while comp:
        ans *= 5
        ans += points[comp.pop()]
    return ans
def complete_me(line):
    stack = []
    for c in line:
        if c in pair:
            stack.append(pair[c])
        elif stack[-1] == c:
            stack.pop()
        else:
            return c
    return stack
incompletes = [scorer(complete_me(line)) for line in data if scorer(complete_me(line)) > 0]
incompletes.sort()
while len(incompletes) > 1:
    incompletes.pop(0)
    incompletes.pop()

print(f'middle score is {incompletes[0]}')
