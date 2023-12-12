import re
import math

f = open("puzzle_input.txt", "r")
lines = f.read().splitlines()
f.close()

directions = re.sub(r'L', '0', lines[0])
directions = re.sub(r'R', '1', directions)

lines = lines[2:]
mapDict = {}
startA = []
for x in lines:
    key = re.search(r'[A-Z]+', x).group()
    mappings = re.search(r'\(.+\)', x).group()
    mappings = re.findall(r'[A-Z]+', mappings)
    mapDict[key] = mappings
    if re.match(r'..A', key):
        startA.append(key)

steps = 0
currentKeys = startA
mod = len(directions)
stepsList = [None] * len(currentKeys)
while (True):
    for i, k in enumerate(currentKeys):
        currKey = mapDict[k][int(directions[steps % mod])]
        currentKeys[i] = currKey
        if re.match(r'..Z', currKey):
            stepsList[i] = steps + 1
    steps += 1
    if None not in stepsList:
        break

total = math.lcm(*stepsList)
print(total)
