import math
import collections

input_file = 'puzzle_input.txt'


class baseModule:
    def addInput(self):
        '''
        dummy
        '''
        return 0


class Broadcaster:
    def __init__(self, line):
        self._output_st = line.split("->")[1]
        self._output = []
        self._name = "broadcast"

    def signal(self, i=0, v=False):
        return (self, v)


class FlipFlop(baseModule):
    def __init__(self, line):
        self._name, self._output_st = [i.strip() for i in line[1:].split("->")]
        self._output = []
        self._s = False

    def signal(self, i, v):
        if not v:
            self._s = not self._s
            return (self, self._s)
        else:
            return None

    def __str__(self,):
        return f"<FlipFlop \"{self._name}\" with state {self._s}, output = {self._output_st}>"

    def __repr__(self):
        return self.__str__()


class Conjunction(baseModule):
    def __init__(self, line):
        self._name, self._output_st = [i.strip() for i in line[1:].split("->")]
        self._input_s = []
        self._output = []

    def addInput(self):
        '''
        add the state to the list, return the input index
        '''
        self._input_s.append(False)
        return len(self._input_s) - 1

    def signal(self, i, v):
        self._input_s[i] = v
        if all(self._input_s):
            return (self, False)
        else:
            return (self, True)

    def __str__(self,):
        return f"<Conjunction \"{self._name}\" with {len(self._input_s)} inputs; output = {self._output_st}>"

    def __repr__(self):
        return self.__str__()


class OutputReg(baseModule):
    def __init__(self, name):
        self._get_low = False
        self._name = name

    def signal(self, i, v):
        if not v:
            self._get_low = True

    def received_low(self,):
        return self._get_low


class StateMachine:
    def __init__(self):
        self._bc = None
        self._l_module = []
        self.reset()

        self._rx = None
        self._l_module_watch = []
        self._l_loop = []
        self._lcm = 0

    def reset(self):
        self._nlow = 0
        self._nhigh = 0
        self._nbutton = 0

    def addBC(self, st):
        self._bc = Broadcaster(st)

    def addFF(self, st):
        ff = FlipFlop(st)
        self._l_module.append(ff)

    def addC(self, st):
        c = Conjunction(st)
        self._l_module.append(c)

    def __getitem__(self, name):
        if name == "rx":
            self._rx = OutputReg(name)
            return 0, self._rx

        for i, m in enumerate(self._l_module):
            if name == m._name:
                return i, m

        return 0, m

    def initialize(self):
        for name in self._bc._output_st.split(","):
            name = name.strip()
            iom, om = self[name]
            if not om:
                continue
            input_for_om = om.addInput()
            self._bc._output.append((om, input_for_om))

        m_input_for_rx = None
        for im, m in enumerate(self._l_module):
            for name in m._output_st.split(","):
                name = name.strip()
                if name == "rx":
                    m_input_for_rx = m
                iom, om = self[name]
                if not om:
                    continue
                input_for_om = om.addInput()
                m._output.append((om, input_for_om))

        for m in self._l_module:
            if m_input_for_rx._name in [om._name for om, i in m._output]:
                self._l_module_watch.append(m._name)
                self._l_loop.append([])

    def press_button(self):
        seq = collections.deque()
        self._nlow += 1
        self._nbutton += 1
        seq.append(self._bc.signal())
        while len(seq):
            tup = seq.popleft()
            if not tup:
                continue
            m, pulse = tup
            if m._name in self._l_module_watch and pulse:
                self._l_loop[self._l_module_watch.index(
                    m._name)].append(self._nbutton)
            for om, idx in m._output:
                if pulse:
                    self._nhigh += 1
                else:
                    self._nlow += 1
                seq.append(om.signal(idx, pulse))

        for l in self._l_loop:
            if len(l) < 1:
                return

        self._lcm = math.lcm(*[l[0] for l in self._l_loop])


def parse():
    sm = StateMachine()
    with open(input_file, 'r') as infile:
        for line in infile:
            if "broadcaster" in line:
                sm.addBC(line)
            elif "%" in line:
                sm.addFF(line)
            elif "&" in line:
                sm.addC(line)
    sm.initialize()
    return sm


def main():
    n = parse()

    i = 0
    while True:
        n.press_button()
        i += 1
        if i == 1000:
            print('Day 20 Part 1:', n._nhigh * n._nlow)
        if n._lcm > 0:
            print('Day 20 Part 2:', n._lcm)
            break


if __name__ == "__main__":
    main()
