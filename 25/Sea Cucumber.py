class Map:
    def __init__(self,data):
        self.d = {(r,c):x for r,row in enumerate(data) for c,x in enumerate(row)}
        self.rows = len(data) 
        self.cols = len(data[0]) 
    def step(self) -> int:
        'east then south'
        east_list = []
        for (r,c),x in self.d.items():
            if x == '>' and self.d[r,(c+1)%self.cols] == '.':
                east_list.append((r,c))
        for r,c in east_list:
            self.d[r,c], self.d[r,(c+1)%self.cols] = '.', '>'
        south_list = []
        for (r,c),x in self.d.items():
            if x == 'v' and self.d[(r+1)%self.rows,c] == '.':
                south_list.append((r,c))
        for r,c in south_list:
            self.d[r,c], self.d[(r+1)%self.rows,c] = '.', 'v'
        return len(east_list) + len(south_list)
    def __str__(self):
        return '\n'.join([''.join([self.d[r,c]
                                  for c in range(self.cols)])
                         for r in range(self.rows)])

if __name__ == '__main__':
    with open('input.txt') as f:
        data = [list(line) for line in f.read().splitlines()]
    m = Map(data)
    i = 1
    while m.step() > 0:
        i += 1
    print(i)
    #print(m)
