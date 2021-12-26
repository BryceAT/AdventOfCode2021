data = [list(line) for line in 
'''#############
#...........#
###B#C#A#B###
  #C#D#D#A#
  #########'''.splitlines()]
data2 = [list(line) for line in 
'''#############
#...........#
###B#C#A#B###
  #D#C#B#A#
  #D#B#A#C#
  #C#D#D#A#
  #########'''.splitlines()]
##14352 as too high
def sidedown(a,b) -> list:
    ans = [a]
    while a[1] < b[1]:
        a = (a[0],a[1]+1)
        ans.append(a)
    while a[1] > b[1]:
        a = (a[0],a[1]-1)
        ans.append(a)
    while a[0] < b[0]:
        a = (a[0] + 1,a[1])
        ans.append(a)
    return ans
scores = {'A':1,'B':10,'C':100,'D':1000}
class Burrow:
    def __init__(self,data,new = True, big = False):
        self.b = [[x for x in row] for row in data]
        self.ct_moves = {k:0 for k in range(1,17 if big else 9)}
        self.big = big
        self.path = []
        self.energy = 0
        self.ave_val = 0
        self.pos = {}
        if new and not big:
            latter_val = {'A':[7,8],'B':[5,6],'C':[3,4],'D':[1,2]}
            for r,row in enumerate(data):
                for c,x in enumerate(row):
                    if x in latter_val:
                        self.pos[latter_val[x].pop()] = (r,c)
        elif new and big:
            latter_val = {'A':[13,14,15,16],'B':[9,10,11,12],'C':[5,6,7,8],'D':[1,2,3,4]}
            for r,row in enumerate(data):
                for c,x in enumerate(row):
                    if x in latter_val:
                        self.pos[latter_val[x].pop()] = (r,c)
    def ave(self):
        self.ave_val = self.energy / ( 5 ** sum([v for k,v in self.ct_moves.items()]))
    def done(self) -> bool:
        return sum(self.ct_moves.values()) == (32 if self.big else 16)
    def get_letter(self,k) -> str:
        loc = self.pos[k]
        return self.b[loc[0]][loc[1]]
    def next_slot(self,cur_letter):
        if not self.big:
            if cur_letter == 'A':
                target = (2,3) if self.b[3][3] == 'A' else (3,3)
            elif cur_letter == 'B':
                target = (2,5) if self.b[3][5] == 'B' else (3,5)
            elif cur_letter == 'C':
                target = (2,7) if self.b[3][7] == 'C' else (3,7)
            elif cur_letter == 'D':
                target = (2,9) if self.b[3][9] == 'D' else (3,9)
            else:
                raise Exception(f'what is target {cur_letter}')
            return target
        if cur_letter == 'A':
            target = (max([i for i in range(2,6) if self.b[i][3] != 'A']),3)
        elif cur_letter == 'B':
            target = (max([i for i in range(2,6) if self.b[i][5] != 'B']),5)
        elif cur_letter == 'C':
            target = (max([i for i in range(2,6) if self.b[i][7] != 'C']),7)
        elif cur_letter == 'D':
            target = (max([i for i in range(2,6) if self.b[i][9] != 'D']),9)
        else:
            raise Exception(f'what is target {cur_letter}')
        return target
    def possible_moves(self,k) -> list:
        cur_letter = self.get_letter(k)
        if cur_letter not in 'ABCD':
            self.print()
            raise Exception(f'missing letter at {self.pos[k]}')
        if self.ct_moves[k] == 0:
            if cur_letter == 'A':
                arr = sorted([(1,4),(1,6),(1,8),(1,1),(1,10),(1,2),(1,11)],
                             key = lambda x: abs(x[1] - self.pos[k][1]) + abs(x[1] - 3),
                             reverse = True)
            elif cur_letter == 'B':
                arr = sorted([(1,4),(1,6),(1,8),(1,10),(1,1),(1,2),(1,11)],
                             key = lambda x: abs(x[1] - self.pos[k][1]) + abs(x[1] - 5),
                             reverse = True)
            elif cur_letter == 'C':
                arr = sorted([(1,4),(1,6),(1,8),(1,10),(1,1),(1,2),(1,11)],
                             key = lambda x: abs(x[1] - self.pos[k][1]) + abs(x[1] - 7),
                             reverse = True)
            elif cur_letter == 'D':
                arr = sorted([(1,4),(1,6),(1,8),(1,10),(1,1),(1,2),(1,11)],
                             key = lambda x: abs(x[1] - self.pos[k][1]) + abs(x[1] - 9),
                             reverse = True)
            return [(x,y) for x,y in arr
                if all([self.b[q][r] == '.' for q,r in sidedown((x,y),self.pos[k])[:-1]])]
        elif self.ct_moves[k] == 1:
            target = self.next_slot(cur_letter)
            if all([self.b[q][r] == '.' for q,r in sidedown(self.pos[k],target)[1:]]):
                return [target]
        return []
    def all_moves(self) -> list:
        return [(k,move) for k in range(1,17 if self.big else 9) for move in self.possible_moves(k)]
    def move(self,k,target) -> None:
        self.path.append((k,target))
        loc = self.pos[k]
        cur_letter = self.get_letter(k)
        if cur_letter not in 'ABCD':
            raise Exception(f'cur_letter {k} at {loc} is {cur_letter}')
        self.energy += (abs(loc[0] - target[0]) + abs(loc[1] - target[1])) * 10**(ord(cur_letter) - 65)
        self.b[loc[0]][loc[1]] = '.'
        self.b[target[0]][target[1]] = cur_letter
        self.ct_moves[k] += 1
        self.pos[k] = target
        self.ave()
    def copy(self) -> 'Burrow':
        c = Burrow(self.b,False,big = self.big)
        c.pos = self.pos.copy()
        c.ct_moves = self.ct_moves.copy()
        c.path = self.path.copy()
        c.energy = self.energy
        return c
    def print(self):
        for line in self.b:
            print(''.join(line))
def get_best(working,top = 1000):
    best = float('inf')
    ct = 0
    #ans = []
    while working:
        working = [w for w in working if w.energy < best]
        #working.sort(key = lambda x: x.ave_val)
        cur = working.pop()
        for k,target in cur.all_moves():
            c = cur.copy()
            c.move(k,target)
            if c.done():
                best = min(best,c.energy)
                ct += 1
                if ct >= top:
                    return best
            else:
                working.append(c)
    print(f'ct {ct}')
    return best
b = Burrow(data)
b.print()
b_big = Burrow(data2,big = True)
complete = get_best([b])
print(f'part 1: min energy {complete}')
complete_big = get_best([b_big])
print(f'part 2: min energy {complete_big}')
       
                
            









