with open('input.txt') as f:
    data = f.read().splitlines()

nums = [int(x) for x in data.pop(0).split(',')]

def get_board() -> 'list[list[int]]':
    b = []
    data.pop(0) #blank
    for _ in range(5):
        b.append([int(x) for x in data.pop(0).split()])
    return b

def score(b:'board: list[list[int]]') -> 'moves,score':
    for ct,n in enumerate(nums):
        for r,row in enumerate(b):
            for c,x in enumerate(row):
                if x == n:
                    b[r][c] = -1
                    if sum(b[r]) == -5 or sum([b[k][c] for k in range(5)]) == -5:
                        return ct, sum([x for row in b for x in row if x != -1]) * n
    return 0,None

boards = []
while data:
    boards.append(get_board())

scores = [score(b) for b in boards]
min_time = min([s[0] for s in scores])
print(f'First board score is: {[s[1] for s in scores if s[0] == min_time][0]}')
max_time = max([s[0] for s in scores])
print(f'Last board score is: {[s[1] for s in scores if s[0] == max_time][0]}')
