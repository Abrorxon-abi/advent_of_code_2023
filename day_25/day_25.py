import fileinput
from collections import defaultdict, deque
input_file = 'puzzle_input.txt'


def parse():
    d = defaultdict(set)
    l_full = []
    for line in fileinput.input(input_file, encoding="utf-8"):
        key, l = line.strip().split(":")
        key = key.strip()

        if key not in l_full:
            l_full.append(key)

        for val in l.split():
            if val not in l_full:
                l_full.append(val)
                pass
            d[l_full.index(key)].add(l_full.index(val))
            d[l_full.index(val)].add(l_full.index(key))
    return d, l_full


def sol1(m):
    n_node = len(m)

    def bfs(m, src, target):
        prev = {src: None}
        q = deque([src])
        while len(q):
            curr = q.popleft()
            if curr == target:
                break

            for next_node in m[curr]:
                if next_node in prev:
                    continue
                prev[next_node] = curr
                q.append(next_node)
        if curr == target:
            path = []
            while curr != None:
                path.append(curr)
                curr = prev[curr]
            return path
        else:
            return list(prev.keys())

    ngroup0 = 1
    for j in range(1, n_node):
        removed = []
        for _ in range(3):
            path = bfs(m, 0, j)
            for i in range(len(path)-1):
                m[path[i]].remove(path[i+1])
                m[path[i+1]].remove(path[i])
                removed.append((path[i], path[i+1]))

        path = bfs(m, 0, j)

        if path[0] == j:
            ngroup0 += 1

        for src, goal in removed:
            m[src].add(goal)
            m[goal].add(src)

    return ngroup0 * (n_node - ngroup0)


def main():
    m, l_full = parse()

    print('Day 25:', sol1(m))


main()
