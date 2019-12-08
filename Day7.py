from queue import Queue
from threading import Thread

class IntComputer:
    def __init__(self, program, inQueue=None, outQueue=None):
        self.program = program
        self.inQueue = inQueue
        self.outQueue = outQueue

    def multiply(self, p, pos, params):
        a = params[0]["value"]
        b = params[1]["value"]
        r = params[2]["pos"]
        p[r] = a * b
        return p, pos+4

    def sum(self, p, pos, params):
        a = params[0]["value"]
        b = params[1]["value"]
        r = params[2]["pos"]
        p[r] = a + b
        return p, pos+4

    def inputAndSave(self, p, pos, params):
        if self.inQueue is None:
            a = int(input("Input value:"))
        else:
            a = self.inQueue.get()
        p[params[0]["pos"]] = a
        return p, pos+2

    def readAndOutput(self, p, pos, params):
        a = params[0]["value"]
        if self.outQueue is None:
            print("Output value: ", a)
        else:
            self.outQueue.put(a)
        return p, pos+2

    def jumpIfTrue(self, p, pos, params):
        if params[0]["value"] != 0:
            pos = params[1]["value"]
        else:
            pos = pos + 3
        return p, pos

    def jumpIfFalse(self, p, pos, params):
        if params[0]["value"] == 0:
            pos = params[1]["value"]
        else:
            pos = pos + 3
        return p, pos

    def lessThan(self, p, pos, params):
        p[params[2]["pos"]] = 1 if params[0]["value"] < params[1]["value"] else 0
        return p, pos+4

    def checkEqual(self, p, pos, params):
        p[params[2]["pos"]] = 1 if params[0]["value"] == params[1]["value"] else 0
        return p, pos+4

    operSet = {
        1 : {"numParams" : 3, "action" : sum},
        2 : {"numParams" : 3, "action" : multiply},
        3 : {"numParams" : 1, "action" : inputAndSave},
        4 : {"numParams" : 1, "action" : readAndOutput},
        5 : {"numParams" : 2, "action" : jumpIfTrue},
        6 : {"numParams" : 2, "action" : jumpIfFalse},
        7 : {"numParams" : 3, "action" : lessThan},
        8 : {"numParams" : 3, "action" : checkEqual}
    }

    def compute(self):
        p = self.program
        pos = 0
        while True:
            op = p[pos]
            if op == 99:
                return
            opCode = op % 100
            parModes = op // 100
            if not opCode in self.operSet:
                print("Error - opcode ",opCode, " not found")
                break
            opDef = self.operSet[opCode]
            params = []
            for i in range(pos+1, pos+1+opDef["numParams"]):
                parMode = parModes % 10
                param = {
                    "mode": parMode,
                    "pos": p[i]
                }
                if parMode == 0:
                    param["value"] = p[p[i]]
                elif parMode == 1:
                    param["value"] = p[i]
                else:
                    print("Error - invalid parameter mode ",parMode)
                    break
                params.append(param)
                parModes = parModes // 10
            p,pos = opDef["action"](self,p,pos,params)
            continue
        return


# IntComputerThread
class IntComputerThread(Thread):

    def __init__(self, computer):
        Thread.__init__(self)
        self.computer = computer

    def run(self):
        self.computer.compute()


class Chain:
    def __init__(self, program, count, inputValue = None, initValues = None, loop = False):
        self.program = program
        self.inputValue = inputValue
        self.initValues = initValues
        self.loop = loop
        self.computers = []
        for i in range(count):
            self.computers.append(IntComputerThread(IntComputer(program.copy(),
                                                    self.computers[i-1].computer.outQueue if i>0 else Queue(),
                                                    Queue())))
        if self.loop:
            self.computers[0].computer.inQueue = self.computers[-1].computer.outQueue

    def compute(self):
        if self.initValues is not None:
            for i in range(len(self.initValues)):
                self.computers[i].computer.inQueue.put(self.initValues[i])
        if self.inputValue is not None:
            self.computers[0].computer.inQueue.put(self.inputValue)
        for x in self.computers:
            x.start()
        for x in self.computers:
            x.join()
        if self.computers[-1].computer.outQueue.empty():
            return None
        else:
            return self.computers[-1].computer.outQueue.get()

def readProgram(fileName):
    f = open(fileName, "r")
    p = [int(x) for x in f.read().split(",")]
    f.close()
    return p

def findMaxThrust(program, loop):
    if not loop:
        phaseLowRange = 0
        phaseHighRange = 5
    else:
        phaseLowRange = 5
        phaseHighRange = 10
    maxThrust = 0
    bestPhases = []
    for p1 in range(phaseLowRange, phaseHighRange):
        used = {p1}
        for p2 in range(phaseLowRange, phaseHighRange):
            if p2 in used:
                continue
            used.add(p2)
            for p3 in range(phaseLowRange, phaseHighRange):
                if p3 in used:
                    continue
                used.add(p3)
                for p4 in range(phaseLowRange, phaseHighRange):
                    if p4 in used:
                        continue
                    used.add(p4)
                    for p5 in range(phaseLowRange, phaseHighRange):
                        if p5 in used:
                            continue
                        phases = [p1, p2, p3, p4, p5]
                        thrust = Chain(program, 5, 0, phases, loop).compute()
                        if thrust > maxThrust:
                            maxThrust = thrust
                            bestPhases = phases
                            # print("Found new max. Phases: ", bestPhases,", thrust: ", maxThrust)
                    used.remove(p4)
                used.remove(p3)
            used.remove(p2)
        used.remove(p1)
    return bestPhases, maxThrust


def main():
    p = readProgram("day7_input.txt")
    bestPhases, maxThrust = findMaxThrust(p, True)
    print("Done. Phases: ", bestPhases,", thrust: ", maxThrust)

if __name__ == '__main__':
    main()
