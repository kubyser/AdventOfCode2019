def multiply(p, pos, params):
    a = params[0]["value"]
    b = params[1]["value"]
    r = params[2]["pos"]
    p[r] = a * b
    return p, pos+4

def sum(p, pos, params):
    a = params[0]["value"]
    b = params[1]["value"]
    r = params[2]["pos"]
    p[r] = a + b
    return p, pos+4

def inputAndSave(p, pos, params):
    a = input("Input value:")
    p[params[0]["pos"]] = a
    return p, pos+2

def readAndOutput(p, pos, params):
    a = params[0]["value"]
    print("Output value: ", a)
    return p, pos+2

def jumpIfTrue(p, pos, params):
    if params[0]["value"] != 0:
        pos = params[1]["value"]
    else:
        pos = pos + 3
    return p, pos

def jumpIfFalse(p, pos, params):
    if params[0]["value"] == 0:
        pos = params[1]["value"]
    else:
        pos = pos + 3
    return p, pos

def lessThan(p, pos, params):
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

def compute(p):
    pos = 0
    while True:
        op = p[pos];
        if op == 99:
            return p;
        opCode = op % 100
        parModes = op // 100
        if not opCode in operSet:
            print("Error - opcode ",opCode, " not found")
            break
        opDef = operSet[opCode]
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
        p,pos = opDef["action"](p,pos,params)
        continue;

def readProgram(fileName):
    f = open(fileName, "r")
    p = f.read().split(",")
    return p


#p = [1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,23,6,27,2,9,27,31,1,5,31,35,1,35,10,39,1,39,10,43,2,43,9,47,
#     1,6,47,51,2,51,6,55,1,5,55,59,2,59,10,63,1,9,63,67,1,9,67,71,2,71,6,75,1,5,75,79,1,5,79,83,1,9,83,87,2,87,10,91,2,
#     10,91,95,1,95,9,99,2,99,9,103,2,10,103,107,2,9,107,111,1,111,5,115,1,115,2,119,1,119,6,0,99,2,0,14,0];
#p = [1002,4,3,4,33]
#p = [1101,1,5,0,4,0,99]

#p=[3,0,4,0,99]

p = readProgram("day5_input_test.txt")
r = compute(p)
#print("Result: ",p[0])