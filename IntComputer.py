from queue import Queue, Empty
from threading import Thread, Lock
import time


class IntComputer:
    class Operation:
        def __init__(self, numParams, action):
            self.numParams = numParams
            self.action = action

    class Parameter:
        def __init__(self, parMode):
            self.parMode = parMode
            self.value = None
            self.address = None

    def __init__(self, program, inQueue=None, outQueue=None, inQueueBlocking=True, inQueueTimeout=None, inQueueDefaultValue=-1):
        self.lock = Lock()
        self.mem = {}
        for i in range(0, len(program)):
            self.mem[i] = program[i]
        self.inQueue = inQueue
        self.__inQueueBlocking = inQueueBlocking
        self.__inQueueTimeout = inQueueTimeout
        self.__inQueueDefaultValue = inQueueDefaultValue
        self.__asciiMode = False
        self.outQueue = outQueue
        self.base = 0
        self.pPos = 0
        self.errorHalt = False

    def setAsciiInputMode(self, asciiMode):
        self.__asciiMode = asciiMode

    def readMem(self, pos):
        if pos < 0:
            print("ERROR: attempt to read from negative memory address")
            self.errorHalt = True
            return None
        if pos in self.mem:
            return self.mem[pos]
        else:
            return 0

    def writeMem(self, pos, value):
        if pos < 0:
            print("ERROR: attempt to write to negative memory address")
            self.errorHalt = True
            return
        self.mem[pos] = value

    def multiply(self, pos, params):
        a = params[0].value
        b = params[1].value
        r = params[2].address
        self.writeMem(r, a * b)
        return pos+4

    def summ(self, pos, params):
        a = params[0].value
        b = params[1].value
        r = params[2].address
        self.writeMem(r, a + b)
        return pos+4

    def inputAndSave(self, pos, params):
        if self.inQueue is None:
            a = int(input("Input value:"))
        else:
            try:
                self.lock.acquire()
                a = self.inQueue.get(self.__inQueueBlocking, self.__inQueueTimeout)
            except Empty:
                a = self.__inQueueDefaultValue
            finally:
                self.lock.release()
            if a == "TERM":
                a = 0
                self.errorHalt = True
        self.writeMem(params[0].address,  a)
        return pos+2

    def readAndOutput(self, pos, params):
        a = params[0].value
        if self.outQueue is None:
            print("Output value: ", a)
        else:
            self.outQueue.put(a)
        return pos+2

    def jumpIfTrue(self, pos, params):
        if params[0].value != 0:
            pos = params[1].value
        else:
            pos = pos + 3
        return pos

    def jumpIfFalse(self, pos, params):
        if params[0].value == 0:
            pos = params[1].value
        else:
            pos = pos + 3
        return pos

    def lessThan(self, pos, params):
        self.writeMem(params[2].address, 1 if params[0].value < params[1].value else 0)
        return pos+4

    def checkEqual(self, pos, params):
        self.writeMem(params[2].address, 1 if params[0].value == params[1].value else 0)
        return pos+4

    def adjustBase(self, pos, params):
        self.base += params[0].value
        return pos+2

    operSet = {
        1 : Operation(3, summ),
        2 : Operation(3, multiply),
        3 : Operation(1, inputAndSave),
        4 : Operation(1, readAndOutput),
        5 : Operation(2, jumpIfTrue),
        6 : Operation(2, jumpIfFalse),
        7 : Operation(3, lessThan),
        8 : Operation(3, checkEqual),
        9 : Operation(1, adjustBase)
    }

    def compute(self):
        self.pPos = 0
        while not self.errorHalt:
            if self.pPos not in self.mem:
                print("ERROR: operand read from unallocated memory")
                return None
            op = self.mem[self.pPos]
            if op == 99:
                return
            opCode = op % 100
            parModes = op // 100
            if not opCode in self.operSet:
                print("Error - opcode ",opCode, " not found")
                break
            opDef = self.operSet[opCode]
            params = []
            for i in range(self.pPos+1, self.pPos+1+opDef.numParams):
                parMode = parModes % 10
                param = self.Parameter(parMode)
                if parMode == 0:
                    param.value = self.readMem(self.readMem(i))
                    param.address = self.readMem(i)
                elif parMode == 1:
                    param.value = self.readMem(i)
                    param.address = None
                elif parMode == 2:
                    param.value = self.readMem(self.base + self.readMem(i))
                    param.address = self.base + self.readMem(i)
                else:
                    print("ERROR: invalid parameter mode ",parMode)
                    self.errorHalt = True
                    break
                params.append(param)
                parModes = parModes // 10
            self.pPos = opDef.action(self, self.pPos, params)
            continue
        return

    @staticmethod
    def readProgram(fileName):
        f = open(fileName, "r")
        p = [int(x) for x in f.read().split(",")]
        f.close()
        return p

    @staticmethod
    def sendAsciiToQueue(asciiLine, queue):
        for x in list(asciiLine):
            a = ord(x)
            queue.put(a)
        queue.put(10)

    @staticmethod
    def sendAsciiListToQueue(asciiList, queue):
        for s in asciiList:
            for x in list(s):
                a = ord(x)
                queue.put(a)
            queue.put(10)


# IntComputerThread
class IntComputerThread(Thread):

    def __init__(self, computer):
        Thread.__init__(self)
        self.lock = computer.lock
        self.computer = computer

    def run(self):
        self.computer.compute()

    def terminate(self):
        self.computer.inQueue.put("TERM")


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

class IntComputerAsciiTerminal:

    def __init__(self, program):
        self.__inQueue = Queue()
        self.__outQueue = Queue()
        self.__computer = IntComputerThread(IntComputer(program, self.__inQueue, self.__outQueue))

    def run(self):
        self.__computer.start()
        s = ""
        while True:
            if not self.__outQueue.empty():
                a = self.__outQueue.get()
                if a == 10:
                    print(s)
                    s = ""
                else:
                    s += chr(a)
            else:
                c = input(">")
                IntComputer.sendAsciiToQueue(c, self.__inQueue)
                time.sleep(0.5)
