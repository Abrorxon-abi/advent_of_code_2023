import re

f = open("puzzle_input.txt", "r")
lines = f.read().splitlines()
f.close()

inputs = []
for x in lines:
    inputs.append(list(map(int, re.findall(r'[-]*[\d]+', x))))

total = 0
for x in inputs:
    steps = []
    steps.append(x)
    end = False
    iteration = 0
    while (not end):
        currStep = []
        totalCheck = 0
        for y in range(0, len(steps[iteration])-1):
            temp = steps[iteration][y+1] - steps[iteration][y]
            totalCheck += abs(temp)
            currStep.append(temp)
        steps.append(currStep)
        iteration += 1
        if (totalCheck == 0):
            end = True

    steps.reverse()
    steps[0].append(0)
    for y in range(0, len(steps)-1):
        temp = steps[y+1][0] - steps[y][0]
        steps[y+1].insert(0, temp)
    total += steps[-1][0]

print(total)
