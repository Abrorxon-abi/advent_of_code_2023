from functools import cache

f = open("puzzle_input.txt", "r")
lines = f.read().splitlines()
f.close()

inputs = []
for x in lines:
    springs, groups = x.split()
    groups = tuple(map(int, groups.split(',')))
    inputs.append((springs, groups))


@cache
def checkValid(springs, groups, count=0):
    if not springs:
        lasG = len(groups)
        if ((lasG == 1 and groups[0] == count) or (lasG == 0 and count == 0)):
            return 1
        return 0

    currSpring = springs[0]
    springs = springs[1:]
    currGroup, *newGroups = groups or [0]
    newGroups = tuple(newGroups)

    if currSpring == '?':
        return checkValid('#'+springs, groups, count) + checkValid('.'+springs, groups, count)

    if currSpring == '#':
        if count == currGroup:
            return 0
        else:
            return checkValid(springs, groups, count+1)

    if currSpring == '.':
        if count == 0:
            return checkValid(springs, groups, 0)
        if count == currGroup:
            return checkValid(springs, newGroups, 0)
        return 0


unfoldedInputs = []
for x in inputs:
    unfoldedInputs.append(('?'.join([x[0]]*5), x[1]*5))


total = 0
for x in unfoldedInputs:
    total += checkValid(x[0], x[1])

print(total)
