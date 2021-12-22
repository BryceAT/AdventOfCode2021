from collections import defaultdict

class Map:
    def __init__(self,d:defaultdict):
        self.d = d
        self.boundary = '.'
        x_coord, y_coord = [x for x,y in d],[y for x,y in d]
        self.top, self.bottom = min(x_coord), max(x_coord)
        self.left, self.right = min(y_coord), max(y_coord)
    def get_val(self,r,c):
        return ''.join([('1' if self.d[i,j] == '#' else '0')
                        for i,j in [(r-1,c-1),(r-1,c),(r-1,c+1),
                                    (r  ,c-1),(r  ,c),(r  ,c+1),
                                    (r+1,c-1),(r+1,c),(r+1,c+1)]])
    def step(self):
        nd = defaultdict(lambda : self.boundary)
        for r in range(self.top -1, self.bottom +2):
            for c in range(self.left -1, self.right +2):
                nd[r,c] = decode[int(self.get_val(r,c),2)]
        self.d = nd
        self.boundary = decode[0] if self.boundary == '.' else decode[511]
        self.top -= 1
        self.bottom += 1
        self.left -= 1
        self.right += 1
    def count_lit(self):
        return sum([1 for k,v in self.d.items()
                    if v == '#'])
    def print(self):
        for r in range(self.top, self.bottom +1):
            print(''.join([self.d[r,c] for c in range(self.left, self.right +1)]))
        print('\n')
if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()
    decode = list(data.pop(0))
    data.pop(0)
    d = defaultdict(lambda : '.')
    for r,row in enumerate(data):
        for c,x in enumerate(row):
            d[r,c] = x
    cur = Map(d)
    #cur.print()
    cur.step()
    #cur.print()
    cur.step()
    #cur.print()
    print(f'part 1: there are {cur.count_lit()} lit points after 2 steps.')
    for _ in range(48):
        cur.step()
    print(f'part 2: there are {cur.count_lit()} lit points after 50 steps.')
