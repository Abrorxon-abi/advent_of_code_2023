import re

f = open("puzzle_input.txt", "r")
lines = f.read().splitlines()
f.close()

directions = re.sub(r'L', '0', lines[0])
directions = re.sub(r'R', '1', directions)

lines = lines[2:]
mapDict = {}
for x in lines:
    key = re.search(r'[A-Z]+', x).group()
    mappings = re.search(r'\(.+\)', x).group()
    mappings = re.findall(r'[A-Z]+', mappings)
    mapDict[key] = mappings

steps = 0
currKey = 'AAA'
mod = len(directions)
while (True):
    currKey = mapDict[currKey][int(directions[steps % mod])]
    steps += 1
    if currKey == 'ZZZ':
        break

print(steps)
