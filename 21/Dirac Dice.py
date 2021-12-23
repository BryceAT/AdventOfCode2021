from functools import lru_cache
from toolz import reduce

class Player:
    def __init__(self,pos):
        self.pos = pos
        self.score = 0
    def play(self,rolls = (0,0,0)) -> None:
        step = sum([x for x in rolls])
        self.pos = (self.pos + step) % 10
        self.score += 10 if self.pos == 0 else self.pos

class Dice:
    'forced dice'
    def __init__(self,up_facing_side):
        self.roll_ct = 0
        self.prev_val = up_facing_side
    def roll(self):
        self.roll_ct += 1
        self.prev_val = (self.prev_val  %100) + 1
        return self.prev_val

@lru_cache(None)
def dfs(p1_pos,p1_score,p2_pos,p2_score,turn = 1):
    if p1_score >= 21:
        return 1,0
    if p2_score >= 21:
        return 0,1
    return reduce(lambda x,y:[a+b for a,b in zip(x,y)],
                  [(dfs((p1_pos +x+y+z)%10,
                        p1_score + (10 if (p1_pos +x+y+z) == 10 else (p1_pos +x+y+z)%10),
                        p2_pos,p2_score,2) if turn == 1 else
                   dfs(p1_pos,p1_score,
                        (p2_pos+x+y+z)%10,p2_score + (10 if (p2_pos +x+y+z) == 10 else (p2_pos +x+y+z)%10),
                        1)) for x in range(1,4) for y in range(1,4) for z in range(1,4)])
if __name__ == '__main__':
    p1 = Player(8)
    p2 = Player(2)
    d = Dice(100)
    turn = 1
    while max(p1.score, p2.score) < 1000:
        if turn == 1:
            p1.play([d.roll(),d.roll(),d.roll()])
            turn = 2
        else:
            p2.play([d.roll(),d.roll(),d.roll()])
            turn = 1
    print(f'part 1: rolls by lossing score = {d.roll_ct * min(p1.score, p2.score)}')
    print(f'part 2: {max(dfs(8,0,2,0))}')
