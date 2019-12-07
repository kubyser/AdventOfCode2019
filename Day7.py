class IntComputer:
    def __init__(self, program, inStream=None, outStream=None):
        self.program = program
        self.inStream = inStream
        self.outStream = outStream

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
        if self.inStream is None:
            a = input("Input value:")
        else:
            if len(self.inStream) == 0:
                # print("ERROR: no data at input")
                # a = None
                a = input("Input value:")
            else:
                a = self.inStream[0]
                self.inStream = self.inStream[1:]
# TODO: remove hack
        if a == '0':
            a = 0
        p[params[0]["pos"]] = a
        return p, pos+2

    def readAndOutput(self, p, pos, params):
        a = params[0]["value"]
        if self.outStream is None:
            print("Output value: ", a)
        else:
            self.outStream.append(a)
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

    def checkEqual(p, pos, params):
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
            op = p[pos];
            if op == 99:
                return p;
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
        return p

def printInput(inStream):
    while len(inStream)>0:
        s = inStream[0]
        print(s)
        inStream = inStream[1:]

class Chain:
    def __init__(self, program, count, inStream = None, outStream = None, preInputs = None):
        self.program = program
        self.inStream = inStream
        self.outStream = outStream
        self.preInputs = preInputs
        self.computers = []
        self.buffer = []
        for i in range(count):
            self.computers.append(IntComputer(program.copy(), inStream if i==0 else None, outStream if i==count-1 else None))

    def buildInput(self, comp, num):
        if self.preInputs is None:
            return comp.inStream
        if len(self.preInputs)-1 < num:
            return comp.inStream
        if comp.inStream is None:
            return self.preInputs[num]
        else:
            return self.preInputs[num] + comp.inStream

    def compute(self):
        for i in range(len(self.computers)):
            c = self.computers[i]
#            print("Computer ",i, " running. Input before preInput: ", c.inStream)
            c.inStream = self.buildInput(c, i)
#            print("Computer ",i, " running. Input after preInput: ", c.inStream)
            if i<len(self.computers)-1:
                self.buffer = []
                c.outStream = self.buffer
                self.computers[i+1].inStream = self.buffer
            c.compute()
#            print("Buffer after run of computer ", i, ": ", self.buffer)
            i = i+1

def makeListOfLists(s):
    r = []
    for x in s:
        n = []
        n.append(x)
        r.append(n)
    return r

def readProgram(fileName):
    f = open(fileName, "r")
    p = [int(x) for x in f.read().split(",")]
    f.close()
    return p

#p=[3,0,4,0,99]
#p=[1105,1,10,0,0,0,0,0,0,0,3,0,4,0,1005,0,10,99]
#p=[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0] #43210
#p=[3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0] #01234
#p=[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0] #10432
#p=[1101,1,5,0,4,0,99]

p=readProgram("day7_input.txt")
inStream = [0]

maxThrust = 0
bestPhases = []
for p1 in range(5):
    used = {p1}
    for p2 in range(5):
        if p2 in used:
            continue
        used.add(p2)
        for p3 in range(5):
            if p3 in used:
                continue
            used.add(p3)
            for p4 in range(5):
                if p4 in used:
                    continue
                used.add(p4)
                for p5 in range(5):
                    if p5 in used:
                        continue
                    phases = makeListOfLists([p1, p2, p3, p4, p5])
                    res = []
                    chain = Chain(p, 5, inStream, res, phases)
                    chain.compute()
                    thrust = res[0]
                    if thrust > maxThrust:
                        maxThrust = thrust
                        bestPhases = str(p1)+str(p2)+str(p3)+str(p4)+str(p5)
                        print("Found new max. Phases: ", bestPhases,", thrust: ", maxThrust)
                used.remove(p4)
            used.remove(p3)
        used.remove(p2)
    used.remove(p1)
print("Done. Phases: ", bestPhases,", thrust: ", maxThrust)


