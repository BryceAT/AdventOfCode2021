with open('input.txt') as f:
    data = [[int(x) for x in y] for y in f.read().splitlines()]
counts = [sum(x) for x in zip(*data)]
gamma = int(''.join([('1' if d > 500 else '0') for d in counts]),2)
epsilon = int(''.join([('0' if d > 500 else '1') for d in counts]),2)
print(f'Power is {gamma * epsilon}')

def mean(l:list) -> float:
    return sum(l)/len(l)

#deep copy
data_ox = [[x for x in y] for y in data]
digit_ind = 0
while len(data_ox) > 1:
    if mean([y[digit_ind] for y in data_ox]) >= .5:
        digit = 1
    else:
        digit = 0
    data_ox = [y for y in data_ox if y[digit_ind] == digit]
    digit_ind += 1
#deep copy
data_co2 = [[x for x in y] for y in data]
digit_ind = 0
while len(data_co2) > 1:
    if mean([y[digit_ind] for y in data_co2]) >= .5:
        digit = 0
    else:
        digit = 1
    data_co2 = [y for y in data_co2 if y[digit_ind] == digit]
    digit_ind += 1

oxygen = int(''.join([str(x) for x in data_ox[0]]),2)
CO2 = int(''.join([str(x) for x in data_co2[0]]),2)
print(f'Life support rating of the submarine is {oxygen * CO2}')
