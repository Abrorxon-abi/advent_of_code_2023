from heapq import heappop, heappush as push

F = {i + j*1j: int(c) for i, r in enumerate(open('puzzle_input.txt'))
     for j, c in enumerate(r.strip())}


def f(min, max, end=[*F][-1], x=0):
    todo = [(0, 0, 0, 1), (0, 0, 0, 1j)]
    seen = set()

    while todo:
        val, _, pos, dir = heappop(todo)

        if (pos == end):
            return val
        if (pos, dir) in seen:
            continue
        seen.add((pos, dir))

        for d in 1j/dir, -1j/dir:
            for i in range(min, max+1):
                if pos+d*i in F:
                    v = sum(F[pos+d*j] for j in range(1, i+1))
                    push(todo, (val+v, (x := x+1), pos+d*i, d))


print('Day 17 Part 2:', f(4, 10))
