from __future__ import annotations
from toolz import reduce
    
class SnailNum:
    def __init__(self, l: list):
        self.reg = {}
        if l:
            self.mk_reg(l)
            self.reduce()
    def mk_reg(self, l: list or int,loc = '') -> dict:
        if type(l) == int:
            self.reg[loc] = l
            return None
        self.mk_reg(l[0],loc + '0')
        self.mk_reg(l[1],loc + '1')
    def __add__(self, other) -> SnailNum:
        n = SnailNum([])
        n.reg = {**{'0'+k:v for k,v in self.reg.items()},
                 **{'1'+k:v for k,v in other.reg.items()}}
        n.reduce()
        return n
    def explode(self) -> bool:
        'do an explode and return True if any, else False'
        mx = max([len(x) for x in self.reg])
        if mx > 4:
            mx_left = sorted([x for x in self.reg if len(x) == mx])[0]
            mx_right = mx_left[:-1] + '1'
            order_keys = sorted(list(self.reg))
            mx_left_ind = order_keys.index(mx_left)
            mx_right_ind = order_keys.index(mx_right)
            if mx_left_ind > 0:
                self.reg[order_keys[mx_left_ind - 1]] += self.reg[mx_left]
            if mx_right_ind < len(order_keys) - 1:
                self.reg[order_keys[mx_right_ind + 1]] += self.reg[mx_right]
            self.reg.pop(mx_left)
            self.reg.pop(mx_right)
            self.reg[mx_left[:-1]] = 0
            return True
        return False
    def split(self) -> bool:
        'True if any split'
        need = sorted([k  for k,v in self.reg.items() if v > 9])
        if need:
            k = need[0]
            self.reg[k+'0'] = self.reg[k] // 2
            self.reg[k+'1'] = (self.reg.pop(k) + 1)// 2
            return True
        return False
    def reduce(self):
        while True:
            while self.explode():
                pass
            if not self.split():
                break
        return None
    def to_list(self,d = None):
        'for testing output'
        if d is None:
            d = self.reg
        if d:
            return [d['0'] if ('0' in d) else self.to_list({k[1:]:v for k,v in d.items() if k[0] =='0'}),
                    d['1'] if ('1' in d) else self.to_list({k[1:]:v for k,v in d.items() if k[0] =='1'})]
    def magnitude(self,loc = '') -> int:
        return (3 * (self.reg[loc+'0'] if loc+'0' in self.reg else self.magnitude(loc + '0')) +
                2 * (self.reg[loc+'1'] if loc+'1' in self.reg else self.magnitude(loc + '1')))
    
    
if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()
    c = reduce(lambda a,b:a + b,[SnailNum(eval(line)) for line in data])
    print(f'part 1:{c.magnitude()}')
    print(f'part 2: {max([(a+b).magnitude() for i,a in enumerate([SnailNum(eval(line)) for line in data]) for j,b in enumerate([SnailNum(eval(line)) for line in data]) if i != j])}')
