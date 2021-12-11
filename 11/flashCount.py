with open('input.txt') as f:
    data = {(r,c):int(x) for r,row in enumerate(f.read().splitlines()) for c,x in enumerate(row)}
#data is 10 by 10 digits
def inc(r,c,flash):
    data[r,c] += 1
    if data[r,c] == 10:
        flash.append((r,c))
        if r > 0:
            flash = inc(r - 1,c,flash)
            if c > 0:
                flash = inc(r - 1, c - 1,flash)
            if c < 9:
                flash = inc(r - 1, c + 1,flash)
        if r < 9:
            flash = inc(r + 1,c,flash)
            if c > 0:
                flash = inc(r + 1, c - 1,flash)
            if c < 9:
                flash = inc(r + 1, c + 1,flash)
        if c > 0:
            flash = inc(r, c - 1,flash)
        if c < 9:
            flash = inc(r, c + 1,flash)
    return flash

def step(data):
    flash = []
    for r,c in data:
        flash = inc(r, c, flash)
    for r,c in flash:
        data[r,c] = 0
    return len(flash)

print(f'flash count is {sum([step(data) for _ in range(100)])}')
ct = 100
while sum(data.values()) > 0:
    step(data)
    ct += 1
print(f'simultaneously flash first on step {ct}')
            
