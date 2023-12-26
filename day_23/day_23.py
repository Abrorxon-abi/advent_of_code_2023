import sys
import collections
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx

input_file = 'puzzle_input.txt'


class matrix:
    def __init__(self, l=[], default=0):
        self._l = [[e for e in il] for il in l]
        self.dim()
        self._default = default

    def dim(self):
        self._nr = len(self._l)
        if len(self._l):
            self._nc = len(self._l[0])
        else:
            self._nc = 0
        return self._nr, self._nc

    def __iter__(self):
        for x in self._l:
            yield x

    def inbound(self, p):
        return p[0] >= 0 and p[0] < self._nr and p[1] >= 0 and p[1] < self._nc

    def __getitem__(self, tup):
        if type(tup) == type((0, 0)):
            return self._l[tup[0] % self._nr][tup[1] % self._nc]
        else:
            return self._l[tup]

    def __setitem__(self, tup, val):
        if type(tup) == type((0, 0)):
            if tup[0] >= self._nr:
                for i in range(self._nr, tup[0]+1):
                    self._l.append([])
            self.dim()
            if tup[1] >= self._nc:
                for r in range(0, self._nr):
                    for c in range(self._nc, tup[1]+1):
                        self._l[r].append(self._default)

            self._l[tup[0]][tup[1]] = val
            self.dim()
        else:
            if tup >= self._nr:
                for i in range(self._nr, tup+1):
                    self._l.append([])
            self._l[tup] = val
            self.dim()

    def __str__(self):
        s = ""
        for l in self:
            for e in l:
                s += str(e)
            s += "\n"
        return s


def tuple_add(a, b):
    return (a[0]+b[0], a[1]+b[1])


def parse():
    m = matrix()
    with open(input_file, 'r') as file:
        for i, line in enumerate(file):
            m[i] = [i for i in line.strip()]
    return m


def find_start_end(m):
    s = None
    e = None
    for i, c in enumerate(m[0]):
        if c == ".":
            s = (0, i)
    for i, c in enumerate(m[-1]):
        if c == ".":
            e = (m.dim()[0] - 1, i)
    return (s, e)


def walk(pos, m, l_visited, sol2):
    """
    yield one by one all possible direction to go
    """
    slope = [">", "v", "<", "^"]
    if not sol2:
        if m[pos] in slope:
            di = slope.index(m[pos])
            new_pos = tuple_add(pos, direction_map[diDecode[di]])
            yield (di, new_pos)
            return

    for di in range(4):
        new_pos = tuple_add(pos, direction_map[diDecode[di]])
        if new_pos in l_visited:
            continue
        if not m.inbound(new_pos):
            continue
        if m[new_pos] == "#":
            continue
        if not sol2:
            if m[new_pos] in slope and di != slope.index(m[new_pos]):
                continue
        yield (di, new_pos)
    pass


def sol_bf(m, sol2):
    """
    brute force first
    disadvantage: there's a lot of list copy and addition, memory use intensive. And slow due to all possibility explored.
        10s for part 1
        part 2 > 10min

    cannot use due to data format change
    """
    (start, end) = find_start_end(m)
    q = collections.deque([[start]])
    max_length = 0
    while len(q):
        l_visited = q.popleft()
        if l_visited[-1] == end:
            max_length = max(max_length, len(l_visited))
            continue
        for _, new_pos in walk(l_visited[-1], m, l_visited, sol2):
            q.append(l_visited + [new_pos])

    return max_length - 1


direction_map = {
    "r": (0,  1),
    "d": (1,  0),
    "l": (0, -1),
    "u": (-1, 0),

    "R": (0,  1),
    "D": (1,  0),
    "L": (0, -1),
    "U": (-1, 0),
}

diDecode = [
    "R", "D", "L", "U"
]


def check_surrounding(pos, prevpos, m):
    """
    check possible direction to go
    if it's <=2, keep going forward
    """
    l_possible_sol1 = []
    l_possible_sol2 = []
    slope = [">", "v", "<", "^"]
    for di in range(4):
        new_pos = tuple_add(pos, direction_map[diDecode[di]])
        if prevpos == new_pos:
            continue
        if m[new_pos] == "#":
            continue
        if not m.inbound(new_pos):
            continue
        l_possible_sol2.append(new_pos)
        if m[new_pos] in slope and di != slope.index(m[new_pos]):
            continue
        l_possible_sol1.append(new_pos)
    return l_possible_sol1, l_possible_sol2


def conversion(c, d_graph, pos):
    if c == "#":
        return 0
    elif pos in d_graph:
        return 2
    else:
        return 1


def plot(d_graph, m, sol2, solution):

    num_m = [[conversion(c, d_graph, (irow, icol))
              for icol, c in enumerate(row)] for irow, row in enumerate(m)]

    map = np.array(num_m)

    fig, ax = plt.subplots()
    im = ax.imshow(map)

    G = nx.DiGraph()

    for i in range(len(solution)-1):
        start = solution[i]
        end = solution[i+1]
        for end2, step in d_graph[start]:
            if end != end2:
                continue

            G.add_edge(f"{(start[0], start[1])}", f"{(end[0], end[1])}",
                       weight=1, length=step, color="tab:red")
            break
        pass

    esolution = [(u, v) for (u, v, d) in G.edges(
        data=True) if d["color"] == "tab:red"]

    for start, l in d_graph.items():
        for end, step in l:
            if (end, start) in esolution or (start, end) in esolution:
                continue
            G.add_edge(f"{(start[0], start[1])}",
                       f"{(end[0], end[1])}", weight=1, length=step, color="k")

    eother = [(u, v) for (u, v, d) in G.edges(
        data=True) if d["color"] != "tab:red"]

    options = {
        'node_size': 1000,
        'font_size': 7,
        'width': 6,
    }

    fig, ax = plt.subplots(figsize=(30, 30))
    pos = nx.spectral_layout(G)
    nx.draw_networkx_nodes(G, pos=pos, node_size=options['node_size'])
    nx.draw_networkx_labels(G, pos=pos, font_size=options['font_size'])
    if sol2:
        nx.draw_networkx_edges(G, pos, edgelist=eother,    edge_color="k",
                               arrows=True, width=6, arrowsize=15, arrowstyle="-")
    else:
        nx.draw_networkx_edges(G, pos, edgelist=eother,
                               edge_color="k", arrows=True, width=6, arrowsize=15)
    nx.draw_networkx_edges(G, pos, edgelist=esolution,
                           edge_color="tab:red", arrows=True, width=6, arrowsize=15)
    labels = nx.get_edge_attributes(G, 'length')
    nx.draw_networkx_edge_labels(
        G, pos=pos, edge_labels=labels, font_size=options["font_size"])

    pass


def sol(m, sol2):
    """
    find the graph feature and then loop inside
    """
    (start, end) = find_start_end(m)
    q = [(start, (-1, -1))]

    d_graph = {}
    while len(q):
        startpos, prevpos = q.pop()
        if startpos in d_graph:
            continue
        d_graph[startpos] = []
        pos = startpos
        for pos in check_surrounding(pos, prevpos, m)[sol2]:
            prevpos = startpos
            step = 1

            while True:
                l_possible = check_surrounding(pos, prevpos, m)[1]
                if len(l_possible) != 1:
                    break

                prevpos = pos
                pos = l_possible[0]
                step += 1

            d_graph[startpos].append((pos, step))

            if pos in d_graph:
                continue

            if pos != end:
                q.append((pos, (-1, -1)))

    if len(sys.argv) <= 2:
        max_s = [-999]

        l_mapped = list(d_graph.keys()) + [end]
        istart = l_mapped.index(start)
        iend = l_mapped.index(end)
        graph_I = [[] for i in l_mapped]
        visited = [False for i in l_mapped]
        for this, l in d_graph.items():
            ithis = l_mapped.index(this)
            for next, step in l:
                inext = l_mapped.index(next)
                graph_I[ithis].append((inext, step))
            pass

        def dfs(graph_I, visited, this, step, max_s):
            if this == iend:
                max_s[0] = max(max_s[0], step)
                return

            for next, added_step in graph_I[this]:
                if visited[next]:
                    continue
                visited[next] = True
                dfs(graph_I, visited, next, step+added_step, max_s)
                visited[next] = False

        visited[istart] = True
        dfs(graph_I, visited, istart, 0, max_s)
        return max_s[0]

    if len(sys.argv) > 2:
        q = [([start], 0)]
        solution = []
        max_s = 0
        while len(q):
            visited_nodes, step = q.pop()
            this = visited_nodes[-1]
            if this == end:
                max_s = max(max_s, step)
                if max_s == step:
                    solution = visited_nodes
                continue

            for next, added_step in d_graph[this]:
                if next in visited_nodes:
                    continue
                q.append((visited_nodes + [next], step+added_step))

        plot(d_graph, m, sol2, solution)

    return max_s


def main():
    m = parse()
    print('Day 23 Part 1:', sol(m, False))
    print('Day 23 Part 2:', sol(m, True))


main()
