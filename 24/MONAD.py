from functools import lru_cache
from time import time

class ALU:
    def __init__(self,w=0,x=0,y=0,z=0):
        self.map = {'w':w,'x':x,'y':y,'z':z}
    def exec(self,line,num = 'w',show = False):
        if line[0] == 'inp':
            self.inp(line[1],num if num != 'w' else self.map['w'])
        elif line[0] == 'add':
            self.add(*line[1:])
        elif line[0] == 'mul':
            self.mul(*line[1:])
        elif line[0] == 'div':
            self.div(*line[1:])
        elif line[0] == 'mod':
            self.mod(*line[1:])
        elif line[0] == 'eql':
            self.eql(*line[1:])
        if show:
            print(line,self.out())
    def inp(self,a,val):
        self.map[a] = int(val)
    def add(self,a,b):
        if b in 'wxyz':
            self.map[a] += self.map[b]
        else:
            self.map[a] += int(b)
    def mul(self,a,b):
        if b in 'wxyz':
            self.map[a] *= self.map[b]
        else:
            self.map[a] *= int(b)
    def div(self,a,b):
        if b in 'wxyz':
            self.map[a] = (1 if self.map[a] * self.map[b] >= 0 else -1) * abs(self.map[a]) // abs(self.map[b])
        else:
            self.map[a] = (1 if self.map[a] * int(b) >= 0 else -1) * abs(self.map[a]) // abs(int(b))
    def mod(self,a,b):
        if b in 'wxyz':
            self.map[a] %= self.map[b]
        else:
            self.map[a] %= int(b)
    def eql(self,a,b):
        if b in 'wxyz':
            self.map[a] = 1 if self.map[a] == self.map[b] else 0
        else:
            self.map[a] = 1 if self.map[a] == int(b) else 0
    def out(self):
        return tuple(self.map.values())
identity = {'w':lambda val: lambda w,x,y,z:(val,x,y,z),
            'x':lambda val: lambda w,x,y,z:(w,val,y,z),
            'y':lambda val: lambda w,x,y,z:(w,x,val,z),
            'z':lambda val: lambda w,x,y,z:(w,x,y,val)}
def f_add(a:str,b:str):
    if b in 'wxyz':
        def add(w,x,y,z):
            check = {'w':w,'x':x,'y':y,'z':z}
            check[a] += check[b]
            return tuple(check.values())
    else:
        def add(w,x,y,z):
            check = {'w':w,'x':x,'y':y,'z':z}
            check[a] += int(b)
            return tuple(check.values())
    return add
def f_mul(a:str,b:str):
    if b in 'wxyz':
        def mul(w,x,y,z):
            check = {'w':w,'x':x,'y':y,'z':z}
            check[a] *= check[b]
            return tuple(check.values())
    else:
        def mul(w,x,y,z):
            check = {'w':w,'x':x,'y':y,'z':z}
            check[a] *= int(b)
            return tuple(check.values())
    return mul
def f_div(a:str,b:str):
    if b in 'wxyz':
        def div(w,x,y,z):
            check = {'w':w,'x':x,'y':y,'z':z}
            if check[a] * check[b] >= 0:
                check[a] =  abs(check[a]) // abs(check[b])
            else:
                check[a] =  -abs(check[a]) // abs(check[b])
            return tuple(check.values())
    else:
        def div(w,x,y,z):
            check = {'w':w,'x':x,'y':y,'z':z}
            if check[a] * int(b) >= 0:
                check[a] =  abs(check[a]) // abs(int(b))
            else:
                check[a] =  -abs(check[a]) // abs(int(b))
            return tuple(check.values())
    return div
def f_mod(a:str,b:str):
    if b in 'wxyz':
        def mod(w,x,y,z):
            check = {'w':w,'x':x,'y':y,'z':z}
            check[a] %= check[b]
            return tuple(check.values())
    else:
        def mod(w,x,y,z):
            check = {'w':w,'x':x,'y':y,'z':z}
            check[a] %= int(b)
            return tuple(check.values())
    return mod
def f_eql(a:str,b:str):
    if b in 'wxyz':
        def eql(w,x,y,z):
            check = {'w':w,'x':x,'y':y,'z':z}
            check[a] = 1 if check[a] == check[b] else 0
            return tuple(check.values())
    else:
        def eql(w,x,y,z):
            check = {'w':w,'x':x,'y':y,'z':z}
            check[a] = 1 if check[a] == int(b) else 0
            return tuple(check.values())
    return eql
def f_inp(a:str,b:str):
    return identity[a](int(b))
def line_func(line,num = 'w'):
    if line[0] == 'inp':
        return f_inp(line[1],num)
    elif line[0] == 'add':
        return f_add(line[1],line[2])
    elif line[0] == 'mul':
        return f_mul(line[1],line[2])
    elif line[0] == 'div':
        return f_div(line[1],line[2])
    elif line[0] == 'mod':
        return f_mod(line[1],line[2])
    elif line[0] == 'eql':
        return f_eql(line[1],line[2])
def compose(f,g):
    return lambda w,x,y,z:f(*g(w,x,y,z))


if __name__ == '__main__':
    with open('input.txt') as f:
        data = [line.split() for line in f.read().splitlines()]
    chunk = []
    for line in data:
        if line[0] == 'inp':
            chunk.append([line])
        else:
            chunk[-1].append(line)
    def ALU_def(block,w,z):
        A = ALU(w,z%26,0,z)
        for line in chunk[block][4:]:
            A.exec(line)
        return A.out()
    blocks = 12
    """
    brute = {-1:{0:(0,0,0,0)}}
    t1 = time()
    for j in range(blocks):
        print(f'{j} def:{time() - t1}')
        brute[j] = {}
        for w in range(1,10):
            for z in set([z for w,x,y,z in brute[j-1].values()]):
                A = ALU(w,z%26,0,z)
                for line in chunk[j][4:]:
                    A.exec(line)
                brute[j][w,0,0,z] = A.out()
    print(f'def:{time() - t1}')
    """
    comp_f = {}
    for block in range(14):
        comp_f[block] = {}
        for w in range(1,10):
            comp_f[block][w] = lambda a,b,c,d:(a,b,c,d)
            for line in chunk[block]:
                comp_f[block][w] = compose(line_func(line,w),comp_f[block][w])
    
    @lru_cache()
    def f(block,w,z):
        return comp_f[block][w](w,0,0,z)
    def f2(ws:list) -> int:
        ans = 0
        for block,w in enumerate(ws):
            ans = f(block,w,ans)[-1]
        return ans
    def g(block,w,z):
        if block == 0:
            return 26*z+(w+12) 
        if block == 1:
            return 26*z+(w+7) 
        if block == 2:
            return 26*z+(w+1) 
        if block == 3:
            return 26*z +(w+2) 
        if block == 4:
            return 26*(z//26)+(w+4) if w!=(z%26 -5) else (z//26)
        if block == 5:
            return 26*z + (w+15) 
        if block == 6:
            return 26*z + (w+11) 
        if block == 7:
            return 26*(z//26)+(w+5) if w!=(z%26 -13) else (z//26)
        if block == 8:
            return 26*(z//26)+(w+3) if w!=(z%26 -16) else (z//26)
        if block == 9:
            return 26*(z//26)+(w+9) if w!=(z%26 -8 ) else (z//26)
        if block == 10:
            return 26*z + (w+2) 
        if block == 11:
            return 26*(z//26) + (w+3) if w!=(z%26 -8) else (z//26)
        if block == 12:
            return 26*(z//26) + (w+3) if w!=(z%26) else (z//26)
        if block == 13:
            return 26*(z//26) + (w+11) if w!=(z%26 - 4) else (z//26)
    def g2(ws:list) -> int:
        ans = 0
        for block,w in enumerate(ws):
            #print(block,w,ans,f(block,w,ans))
            ans = g(block,w,ans)
        return ans
    """
    brute2 = {-1:{0:(0,0,0,0)}}
    t2 = time()
    for j in range(blocks):
        brute2[j] = {(w,0,0,z):f(j,w,z) for w in range(1,10)
                     for z in [z for w,x,y,z in brute2[j-1].values()]}
    print(f'func:{time() - t2}')
    """
    """
    brute3 = {-1:{0:0}}
    t3 = time()
    for block in range(blocks):
        print(f'{block} reduced:{time() - t3}')
        brute3[block] = {}
        for z in brute3[block -1]:
            for w in range(1,10):
                brute3[block][z] = max(w,brute3[block].get(f(block,w,z)[-1],0))
    print(f'reduced:{time() - t3}')
    """
    #"""
    brute4 = {-1:{0:0}}
    t4 = time()
    for block in range(blocks):
        print(f'{block} reduced g:{time() - t4}')
        brute4[block] = {}
        for z in brute4[block -1].values():
            for w in range(1,10):
                brute4[block][w,z] = g(block,w,z)
    print(f'reduced g:{time() - t4}')
    #"""
'''
ans = 1
cur = [9] * 14
while ans != 0:
    cur = [int(d) for d in str(int(''.join(str(d) for d in cur)) - 1)]
    while 0 in cur:
        cur = [int(d) for d in str(int(''.join(str(d) for d in cur)) - 1)]
    ans = f2(cur)
'''
'''
A = ALU(1,0,0,26)
for line in chunk[12]:
    A.exec(line,show= True)
'''
'''
for i in range(-10000,10000):
	for j in range(1,10):
		if f(13,j,i)[-1] == 0:
			print(i,j,f(13,j,i))

			
5 1 (1, 0, 0, 0)
6 2 (2, 0, 0, 0)
7 3 (3, 0, 0, 0)
8 4 (4, 0, 0, 0)
9 5 (5, 0, 0, 0)
10 6 (6, 0, 0, 0)
11 7 (7, 0, 0, 0)
12 8 (8, 0, 0, 0)
13 9 (9, 0, 0, 0)
#for block 13, 5 <= z <= 13 in order to make z == 0.
#for block 12, lambda w,z: (z//26)*(26 if w!=(z%26) else 1) + ((w+3) if w!=(z%26) else 0)
#so z in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 131, 132, 133, 134, 135, 136, 137, 138, 139, 157, 158, 159, 160, 161, 162, 163, 164, 165, 183, 184, 185, 186, 187, 188, 189, 190, 191, 209, 210, 211, 212, 213, 214, 215, 216, 217, 235, 236, 237, 238, 239, 240, 241, 242, 243, 261, 262, 263, 264, 265, 266, 267, 268, 269, 287, 288, 289, 290, 291, 292, 293, 294, 295, 313, 314, 315, 316, 317, 318, 319, 320, 321]
#for block 11, lambda w,z: (z//26)*(26 if w!=(z%26 -8 ) else 1) + ((w+3) if w!=(z%26 -8 ) else 0)
#for block 10, lambda w,z: (z//1 )*(26 if w!=(z%26 +15) else 1) + ((w+2) if w!=(z%26 +15) else 0)
#for block 9,  lambda w,z: 26*(z//26)+(w+9) if w!=(z%26 -8 ) else (z//26)
#for block 8,  lambda w,z: 26*(z//26)+(w+3) if w!=(z%26 -16) else (z//26)
#for block 7,  lambda w,z: 26*(z//26)+(w+5) if w!=(z%26 -13) else (z//26)
#for block 6,  lambda w,z: 26*(z//1)+(w+11) if w!=(z%26 +15) else (z//1)
#for block 5,  lambda w,z: 26*(z//1)+(w+15) if w!=(z%26 +14) else (z//1)
#for block 4,  lambda w,z: 26*(z//26)+(w+4) if w!=(z%26 -5) else (z//26)
#for block 3,  lambda w,z: 26*(z//1)+(w+2) if w!=(z%26 +11) else (z//1)
'''
out13 = [0]
out12 = [5,6,7,8,9,10,11,12,13]
out11 = [z for w in range(1,10) for z in range(100000) if g(12,w,z) in out12]
pos = {}
pos[11] = {k:v for k,v in brute4[11].items() if v in out11}
for block in range(10,-1,-1):
    pos[block] = {k:v for k,v in brute4[block].items() if v in [z for w,z in pos[block + 1]]}
'''
pos = {14:{0:w for w in range(1,10)}}
for block in range(13,-1,-1):
    print(block)
    pos[block] = {}
    for z in range(1000000):
        for w in range(1,10):
            if f(block,w,z)[3] in pos[block+1]:
                pos[block][z] = max(w,pos[block].get(z,0))
print(len(pos[0]))
'''

ds = [max([w for w,z in pos[0]])]
for block in range(1,12):
    ds.append(max([w for w,z in pos[block] if z in [v for k,v in pos[block-1].items() if k[0] == ds[block -1]]]))
ds.append(max([w for w,z in {(w,z):g(12,w,z) for w in range(1,10) for z in (346,347) if g(12,w,z) in out12}]))
ds.append(9) #because g(13,9,13) == 0 and g(12,9,347) == 13
print(f"part 1: {''.join([str(x) for x in ds])}")

ds_min = [min([w for w,z in pos[0]])]
for block in range(1,12):
    ds_min.append(min([w for w,z in pos[block] if z in [v for k,v in pos[block-1].items() if k[0] == ds_min[block -1]]]))

#[1, 1, 8, 4, 1, 2, 3, 1, 1, 1, 7, 1]
    
