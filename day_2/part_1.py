import re

input_file = 'puzzle_input.txt'
q = {2: open(input_file).read()}

games = re.findall(r'(\d+):((?: *\d+\s+\w+,?;?)+)', q[2])
count = sum([int(g[0]) for g in games])
for g in games:
    dice = re.findall(r'(\d+)\s+(\w+)', g[1])
    for d in dice:
        n, c = int(d[0]), d[1]
        if (n > 12 and c == 'red') or (n > 13 and c == 'green') or (n > 14 and c == 'blue'):
            count -= int(g[0])
            break

print('Day 2 Part 1:', count)
