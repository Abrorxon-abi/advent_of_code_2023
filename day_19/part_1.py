import copy
import re

input_file = 'puzzle_input.txt'


def parse():
    d = {}
    l = []
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            key = re.search("(.*)(?=\{)", line).group(0)
            m = re.search("(?<=\{)(.*?)(?=\})", line).group(0)
            if key:
                d[key] = []
                for rule in m.split(","):
                    if ":" in rule:
                        eq, target = rule.split(":")
                        d[key].append((eq, target))
                    else:
                        #
                        d[key].append(("true", rule))
            else:
                p = property(m)
                l.append(p)
    return d, l


class property:
    def __init__(self, s):
        for i in s.split(","):
            l, val = i.split("=")
            if l == "x":
                self._x = int(val)
            elif l == "m":
                self._m = int(val)
            elif l == "a":
                self._a = int(val)
            elif l == "s":
                self._s = int(val)
        self._true = True

    def score(self, ):
        return self._x + self._a + self._m + self._s

    def operate(self, s):
        return eval(f"self._{s}")

    def __str__(self, ):
        return f"product x={self._x},m={self._m},a={self._a},s={self._s}"


def sol1(rulebook, l_p):
    s = 0
    for p in l_p:
        w = "in"
        while w != "A" and w != "R":
            for rule, target in rulebook[w]:
                if p.operate(rule):
                    w = target
                    break
                else:
                    continue
        if w == "A":
            s += p.score()
    return s


class prange:
    def __init__(self, p=None):
        self._d = {}
        self._d['x'] = range(1, 4001)
        self._d['m'] = range(1, 4001)
        self._d['a'] = range(1, 4001)
        self._d['s'] = range(1, 4001)

    def __getitem__(self, i):
        return self._d[i]

    def __setitem__(self, i, val):
        self._d[i] = val

    def fork(self, s):
        c = s[0]

        l_true = []
        l_false = []

        for i in self[c]:
            if eval(f"{i}{s[1:]}"):
                l_true.append(i)
            else:
                l_false.append(i)

        ptrue = copy.deepcopy(self)
        ptrue[c] = l_true
        self[c] = l_false
        return ptrue

    def score(self,):
        return len(self._d['x']) * len(self._d['m']) * len(self._d['a']) * len(self._d['s'])


def main():
    d, p = parse()
    print('Day 19 part 1:', sol1(d, p))


main()
