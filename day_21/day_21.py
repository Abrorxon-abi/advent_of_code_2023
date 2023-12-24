import math
import collections

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


diDecode = [
    "R", "D", "L", "U"
]

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


def parse():
    m = []
    si, sj = 0, 0
    with open(input_file, 'r') as file:
        for i, line in enumerate(file):
            line = line.strip()
            if "S" in line:
                si = i
                sj = line.find("S")
            m.append([c for c in line])
    return (si, sj), matrix(m)


def walk(pos, m):
    for di in range(4):
        di_vec = direction_map[diDecode[di]]
        newpos = tuple_add(pos, di_vec)
        if m[newpos] == "#":
            continue
        else:
            yield newpos


def find_for_one(s, m):
    visited = {}
    dq = collections.deque()
    dq.append((s, 0))
    step = 0
    while len(dq):
        pos, step = dq.popleft()
        if not m.inbound(pos):
            continue
        if pos in visited:
            continue
        visited[pos] = step
        for newpos in walk(pos, m):
            if not m.inbound(newpos):
                continue
            dq.append((newpos, step+1))

    tup = collections.namedtuple('StartEndMap', 'R, D, L, U, max')

    minR, minD, minL, minU = math.inf, math.inf, math.inf, math.inf
    posR, posD, posL, posU = [], [], [], []
    for r in range(m._nr):
        if visited[(r, 0)] < minL:
            minL = visited[(r, 0)]
            posL = [(r, 0)]
        if visited[(r, 0)] == minL:
            posL += [(r, 0)]

        if visited[(r, m._nc-1)] < minR:
            minR = visited[(r, m._nc-1)]
            posR = [(r, m._nc-1)]
        if visited[(r, m._nc-1)] == minR:
            posR += [(r, m._nc-1)]

    for c in range(m._nc):
        if visited[(0, c)] < minU:
            minU = visited[(0, c)]
            posU = [(0, c)]
        if visited[(0, c)] == minU:
            posU += [(0, c)]

        if visited[(m._nr-1, c)] < minD:
            minD = visited[(m._nr-1, c)]
            posD = [(m._nr-1, c)]
        if visited[(m._nr-1, c)] == minD:
            posD += [(m._nr-1, c)]

    max_step = max(visited.values())

    tup.R = [posR, minR]
    tup.D = [posD, minD]
    tup.L = [posL, minL]
    tup.U = [posU, minU]
    tup.max = max_step

    return tup, visited


def sol1(s, m, ns):
    visited = {}
    dq = collections.deque()
    dq.append((s, 0))
    step = 0
    while len(dq):
        pos, step = dq.popleft()
        if pos in visited:
            continue
        visited[pos] = step % 2
        if step >= ns:
            continue
        for newpos in walk(pos, m):
            if not m.inbound(newpos):
                continue
            dq.append((newpos, step+1))

    sum = 0
    for _, s in visited.items():
        if s == ns % 2:
            sum += 1
    return sum


def getN(l, m, ns):
    visited = {}
    output = 0
    dq = collections.deque()
    for pos in l:
        dq.append((pos, 1))
    while len(dq):
        pos, step = dq.popleft()
        if not m.inbound(pos):
            continue
        if pos in visited:
            continue
        visited[pos] = step

        if (ns - step) % 2 == 0:
            output += 1

        if step == ns:
            continue

        for newpos in walk(pos, m):
            if not m.inbound(newpos):
                continue
            dq.append((newpos, step+1))
    return output


def sol2_cheat(s, m, ns):
    _, visited = find_for_one(s, m)

    dim = m._nr
    center = s[0]

    l_even_odd = [0, 0]
    for steps in visited.values():
        l_even_odd[steps % 2] += 1

    output = 0
    nblock = ns // dim - 1

    s_outer = (nblock+1) ** 2
    s_inner = nblock ** 2

    sign_outer = (nblock + ns) % 2
    sign_inner = (nblock + ns + 1) % 2

    output += s_outer * l_even_odd[sign_outer]
    output += s_inner * l_even_odd[sign_inner]

    l = [(center, 0),
         (0, center),
         (center, dim-1),
         (dim-1, center)]
    for i, pos in enumerate(l):
        output += getN([pos], m, ns - dim * nblock - center)

    for pos in [(dim-1, dim-1), (dim-1, 0), (0, dim-1), (0, 0)]:
        output += getN([pos], m, ns - dim * (nblock - 1) -
                       2 * center - 1) * nblock
        output += getN([pos], m, ns - dim * nblock -
                       2 * center - 1) * (nblock + 1)

    return output


def main():
    s, m = parse()

    print('Day 21 Part 1:', sol1(s, m, 64))
    print('Day 21 Part 2:', sol2_cheat(s, m, 26501365))


main()
