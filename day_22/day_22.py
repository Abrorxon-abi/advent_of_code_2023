from collections import namedtuple, deque

input_file = 'puzzle_input.txt'

Brick = namedtuple("LongBrick", "x, y, z")


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


def parse():
    m = []
    with open(input_file, 'r') as file:
        for i, line in enumerate(file):
            start_str, end_str = line.strip().split("~")
            start = [int(i) for i in start_str.split(",")]
            end = [int(i) for i in end_str.split(",")]
            brick = Brick((start[0], end[0]+1),
                          (start[1], end[1]+1),
                          (start[2], end[2]+1),
                          )
            m.append(brick)
    return sorted(m, key=lambda x: x.z)


def fall(bricks_ss):
    nbrick = len(bricks_ss)
    minx, miny = min(b.x[0] for b in bricks_ss), min(b.y[0] for b in bricks_ss)
    assert minx == 0
    assert miny == 0
    maxx, maxy = max(b.x[0] for b in bricks_ss), max(b.y[0] for b in bricks_ss)
    m_hold = [[False for i in range(nbrick + 1)] for j in range(nbrick + 1)]

    highest_brick = matrix([[(0, 0) for i in range(maxy+1)]
                           for j in range(maxx+1)])

    for ib, b in enumerate(bricks_ss):
        expected_zpos = 0
        zlength = b.z[1] - b.z[0]
        for x in range(*b.x):
            for y in range(*b.y):
                expected_zpos = max(
                    highest_brick[(x, y)][0] + 1, expected_zpos)

        for x in range(*b.x):
            for y in range(*b.y):
                if highest_brick[(x, y)][0] == expected_zpos - 1:
                    m_hold[highest_brick[(x, y)][1]][ib+1] = True
                highest_brick[(x, y)] = (expected_zpos + zlength - 1, ib+1)

    return m_hold


def sol(m_hold):
    nbricks = len(m_hold) - 1
    nbrick = 0

    l_cannot_remove = []

    for ibrick in range(1, nbricks + 1):
        can_remove = True
        for isb, supported_brick in enumerate(m_hold[ibrick]):
            if not supported_brick:
                continue

            found_other_support = False
            for i_other_support in range(1, nbricks + 1):
                if i_other_support != ibrick and m_hold[i_other_support][isb]:
                    found_other_support = True

            if not found_other_support:
                can_remove = False
        if can_remove:
            nbrick += 1
        else:
            l_cannot_remove.append(ibrick)

    d_dependents = {}
    d_dependees = {}

    for i in range(1, nbricks+1):
        d_dependents[i] = []
        d_dependees[i] = []

    for i in range(1, nbricks+1):
        for j in range(1, nbricks+1):
            if m_hold[i][j]:
                d_dependents[i].append(j)
                d_dependees[j].append(i)

    nfall = 0
    for remove in l_cannot_remove:
        this_fall = set()
        dq = deque([remove])
        while len(dq):
            ibrick = dq.popleft()
            if ibrick in this_fall:
                continue
            this_fall.add(ibrick)
            for isb in d_dependents[ibrick]:
                found_other_support = False
                for i_other_support in d_dependees[isb]:
                    if i_other_support not in this_fall:
                        found_other_support = True
                        break
                if not found_other_support:
                    dq.append(isb)
        nfall += len(this_fall) - 1
    return nbrick, nfall


def main():
    ss = parse()
    m_hold = fall(ss)
    print('Day 22 Part 1 and Part 2:', *sol(m_hold), sep="\n")


main()
