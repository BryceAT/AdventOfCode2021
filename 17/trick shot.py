#target area: x=217..240, y=-126..-69
#max value, does not depend on x.
#Use the fact that after shooting up prob must pass same level then not skip the target in one step.

from functools import lru_cache
target_box = ((217,240),(-126,-69))
#target_box = ((20,30),(-10,-5))
def hit(x:int,y:int,tb = target_box) -> bool:
    return tb[0][0] <= x <= tb[0][1] and tb[1][0] <= y <= tb[1][1]

@lru_cache(4000)
def maxy_if_hit(vx:int,vy:int,x=0,y=0,max_y=0) -> int or None:
    if y < target_box[1][0]:
        return None
    if hit(x,y):
        return max_y
    x += vx
    y += vy
    if vx != 0:
        vx += 1 if vx < 0 else -1
    return maxy_if_hit(vx,vy -1,x,y,max(y,max_y))

print(maxy_if_hit(21,abs(target_box[1][0]) - 1))
#print(maxy_if_hit(6,abs(target_box[1][0]) - 1))
#part 2
print(len([vx for vy in range(target_box[1][0],abs(target_box[1][0]))
           for vx in range(21,241) if maxy_if_hit(vx,vy) is not None]))

