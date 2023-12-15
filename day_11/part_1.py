
f = open("puzzle_input.txt", "r")
lines = f.read().splitlines()
f.close()

newLines = []

for x in lines:
    newLines.append(x)
    if '#' not in x:
        newLines.append(x)

lines = list(map(list, zip(*newLines)))

newLines = []

for x in lines:
    y = ''.join(x)
    newLines.append(y)
    if '#' not in y:
        newLines.append(y)


lines = list(map(list, zip(*newLines)))

newLines = []

for x in lines:
    y = ''.join(x)
    newLines.append(y)

lines = newLines

coords = []
for i, x in enumerate(lines):
    for j, y in enumerate(x):
        if (y == '#'):
            tup = (i, j)
            coords.append(tup)

total = 0
for i, x in enumerate(coords):
    for j in range(i+1, len(coords)):
        sub = abs(coords[j][0] - x[0]) + abs((coords[j][1] - x[1]))
        total += sub

print(total)
