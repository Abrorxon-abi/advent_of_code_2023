input_file = 'puzzle_input.txt'

f = open(input_file).read().strip()

steps = f.split(',')
boxes = [[] for _ in range(256)]
for s in steps:
    label = ''.join([c for c in s if c.isalpha()])
    operation = ''.join([c for c in s if not c.isalnum()])
    focal = ''.join([c for c in s if c.isdigit()])
    lens = (label, focal)
    box = 0
    for c in label:
        box += ord(c)
        box *= 17
        box %= 256
    if operation == '=':
        if label not in [x[0] for x in boxes[box]]:
            boxes[box].append(lens)
        else:
            index = [x[0] for x in boxes[box]].index(label)
            boxes[box].pop(index)
            boxes[box].insert(index, lens)
    elif operation == '-':
        if label in [x[0] for x in boxes[box]]:
            boxes[box].pop([x[0] for x in boxes[box]].index(label))

score = 0
for i, box in enumerate(boxes):
    for j, lens in enumerate(box):
        score += (i+1)*(j+1)*int(lens[1])

print('Day 15 Part 2:', score)
