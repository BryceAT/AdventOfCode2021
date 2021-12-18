from toolz import reduce

d_hex = {'0':'0000',
'1':'0001',
'2':'0010',
'3':'0011',
'4':'0100',
'5':'0101',
'6':'0110',
'7':'0111',
'8':'1000',
'9':'1001',
'A':'1010',
'B':'1011',
'C':'1100',
'D':'1101',
'E':'1110',
'F':'1111'}

def hex2bit(hex_str):
    return ''.join([d_hex[s] for s in hex_str])

class Packet:
    def __init__(self,bits):
        self.version = int(bits[:3],2) if bits else None
        self._type = int(bits[3:6],2) if len(bits) > 5 else None
        self.bits = bits[6:]
        self.val = None
        self.sub_packets = []
        if len(bits) > 3:
            self.parse()
    def literal(self):
        cur_len = 6
        ans = ''
        while self.bits[0] == '1':
            cur, self.bits = self.bits[1:5], self.bits[5:]
            ans += cur
            cur_len += 5
        ans += self.bits[1:5]
        self.bits = self.bits[5:]
        self.val = int(ans,2)
        cur_len += 5
        return None
    def operator(self):
        self.len_type_ID = self.bits[0]
        self.bits = self.bits[1:]
        if self.len_type_ID == '0':
            len_sub_packets = int(self.bits[:15],2)
            self.bits = self.bits[15:]
            sp = Packet(self.bits[:len_sub_packets])
            self.bits = self.bits[len_sub_packets:]
            self.sub_packets.append(sp)
            while sp.bits:
                sp = Packet(sp.bits)
                self.sub_packets.append(sp)
        else:
            ct_sub_packets = int(self.bits[:11],2)
            self.bits = self.bits[11:]
            for ind in range(ct_sub_packets):
                sp = Packet(sp.bits if ind > 0 else self.bits)
                self.sub_packets.append(sp)
            self.bits = sp.bits
        return None
    def parse(self):
        if self._type == 4:
            self.literal()
        else:
            self.operator()
    def sum_versions(self):
        return self.version + sum([sp.sum_versions()
                                   for sp in self.sub_packets
                                   if sp.version is not None])
    def eval(self):
        op = {0:lambda x: sum([sp.eval() for sp in x.sub_packets]),
              1:lambda x: reduce(lambda x,y:x*y,[sp.eval() for sp in x.sub_packets],1),
              2:lambda x: min([sp.eval() for sp in x.sub_packets]),
              3:lambda x: max([sp.eval() for sp in x.sub_packets]),
              4:lambda x: x.val,
              5:lambda x: 1 if x.sub_packets[0].eval() > x.sub_packets[1].eval() else 0,
              6:lambda x: 1 if x.sub_packets[0].eval() < x.sub_packets[1].eval() else 0,
              7:lambda x: 1 if x.sub_packets[0].eval() == x.sub_packets[1].eval() else 0}
        return op[self._type](self)
            
    
if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read()
    bits = hex2bit(data)
    p = Packet(bits)
    print(f'part 1: {p.sum_versions()}')
    print(f'part 2: {p.eval()}')
    #Packet(hex2bit('04005AC33890')).eval()


















    
