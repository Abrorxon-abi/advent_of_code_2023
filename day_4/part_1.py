import re

f = open("puzzle_input.txt", "r")

lines = f.read().splitlines()
winningNums = []
cardNums = []
total = 0

for x in lines:
    y = re.sub(r'Card[\s]+[\d]+: ', "", x).split(" | ")
    winningNums.append(list(map(int, re.findall(r'[\d]+', y[0]))))
    cardNums.append(list(map(int, re.findall(r'[\d]+', y[1]))))

for i, x in enumerate(cardNums):
    matches = 0
    points = 0
    for y in x:
        if y in winningNums[i]:
            matches += 1
    if matches > 0:
        points = pow(2, matches-1)
    total += points

print('Day 4 Part 1:', total)
