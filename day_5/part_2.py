import re

input_file = 'puzzle_input.txt'

q = {5: open(input_file).read().strip()}

sections = re.split(r'\n\n', q[5].strip())
seeds = list(map(int, sections[0].split()[1:]))
maps = sections[1:]

current = [(a, a+b) for a, b in zip(seeds[::2], seeds[1::2])]

for table in maps:
    rows = [tuple(map(int, row.split())) for row in table.split('\n')[1:]]
    i_start = [-99]
    offsets = [0]
    latest_end = -99
    for row in sorted(rows, key=lambda row: row[1]):
        latest_end = max(latest_end, row[1]+row[2])
        offset = row[0] - row[1]
        if i_start and i_start[-1] == row[1]:
            i_start[-1] = row[1]
            offsets[-1] = offset
        else:
            i_start.append(row[1])
            offsets.append(offset)
        i_start.append(row[1]+row[2])
        offsets.append(0)

    out = []

    for interval in current:
        splits = [interval[0]]
        start_index = None
        for idx, post in enumerate(i_start):
            if post <= splits[-1]:
                continue
            if start_index is None:
                start_index = idx - 1
            if post < interval[1]:
                if post != interval[1]:
                    splits.append(post)
            else:
                break
        splits.append(interval[1])
        start_index = start_index or len(offsets)
        for a, b in zip(splits, splits[1:]):
            dx = offsets[min(start_index or float('inf'), len(offsets)-1)]
            start_index += 1
            out.append((a+dx, b+dx))

    current = out

print('Day 5 Part 2:', min(c[0] for c in current))
