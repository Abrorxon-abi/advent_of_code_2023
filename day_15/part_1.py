input_file = 'puzzle_input.txt'

f = open(input_file).read().strip()

steps = f.split(',')
values = []
for s in steps:
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value %= 256
    values.append(value)

print('Day 15 Part 1:', sum(values))
