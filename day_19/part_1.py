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


def main():
    d, p = parse()
    print('Day 19 part 1:', sol1(d, p))


main()
