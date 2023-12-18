import re
import math

f = open("puzzle_input.txt", "r")
lines = f.read().splitlines()
f.close()

timeList = list(map(int, re.findall(r'[\d]+', lines[0])))
distList = list(map(int, re.findall(r'[\d]+', lines[1])))

total = 1

for x, y in zip(timeList, distList):
    lowBound = 0
    for lowBound in range(math.ceil(x/2)):
        if lowBound * (x-lowBound) > y:
            break
    total *= (x - 2*lowBound)+1

print('Day 6 Part 1:', total)
