import re

input_file = 'puzzle_input.txt'
q = {2: open(input_file).read()}

games = re.findall(r'(\d+):((?: *\d+\s+\w+,?;?)+)', q[2])
power_num = 0
for g in games:
    dice = re.findall(r'(\d+)\s+(\w+)', g[1])
    t = {'red': [], 'green': [], 'blue': []}
    for d in dice:
        n, c = int(d[0]), d[1]
        t[c].append(int(n))
    power_num += max(t['red']) * max(t['green']) * max(t['blue'])

print('Day 2 Part 2:', power_num)
