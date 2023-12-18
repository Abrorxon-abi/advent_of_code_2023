f = open("puzzle_input.txt", "r")
lines = f.read().splitlines()
f.close()

distance = 1000000
coords = []
for i, x in enumerate(lines):
    for j, y in enumerate(x):
        if (y == '#'):
            tup = [i, j]
            coords.append(tup)

currMultiplier = 0

cordMults = []
for x in lines:
    if '#' not in x:
        currMultiplier += distance - 1
    cordMults.append(currMultiplier)

for x in range(len(cordMults)-1, -1, -1):
    for y in coords:
        if y[0] == x:
            y[0] += cordMults[x]

currMultiplier = 0
lines = list(map(list, zip(*lines)))
cordMults = []
for x in lines:
    if '#' not in x:
        currMultiplier += distance - 1
    cordMults.append(currMultiplier)

for x in range(len(cordMults)-1, -1, -1):
    for y in coords:
        if y[1] == x:
            y[1] += cordMults[x]

total = 0
for i, x in enumerate(coords):
    for j in range(i+1, len(coords)):
        sub = abs(coords[j][0] - x[0]) + abs((coords[j][1] - x[1]))
        total += sub

print('Day 11 Part 2:', total)
