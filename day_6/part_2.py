import re
import math

f = open("puzzle_input.txt", "r")
lines = f.read().splitlines()
f.close()

lines[0] = re.sub(r'[\s]+', '', lines[0])
lines[1] = re.sub(r'[\s]+', '', lines[1])
time = int(re.search(r'[\d]+', lines[0]).group())
dist = int(re.search(r'[\d]+', lines[1]).group())

lowBound = 0
for lowBound in range(math.ceil(time/2)):
    if lowBound * (time-lowBound) > dist:
        break

total = (time - 2*lowBound)+1

print('Day 6 Part 2:', total)
