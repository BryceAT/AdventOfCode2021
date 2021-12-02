import pandas as pd
df = pd.read_csv('nums.txt',headers = False)
l = df[0].to_list()
ct_inc = 0
for a,b in zip(l,l[1:]):
    if b > a:
        ct_inc += 1
print(ct_inc)

ct_inc_window = 0
for a,b in zip(l,l[3:]):
    if a < b:
        ct_inc_window += 1
print(ct_inc_window)
