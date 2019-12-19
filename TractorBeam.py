from IntComputer import IntComputer, IntComputerThread
from queue import  Queue, Empty
import copy

class TractorBeam:

    def __init__(self, filename):
        self.program = IntComputer.readProgram(filename)
        self.inQueue = Queue()
        self.outQueue = Queue()
        self.field = {}
        self.width = 0
        self.height = 0
        # self.computer = IntComputerThread(IntComputer(p, self.inQueue, self.outQueue))
        # self.computer.start()

    def checkAtPosition(self, pos):
        self.computer = IntComputer(self.program, self.inQueue, self.outQueue)
        while not self.outQueue.empty():
            self.outQueue.get()
        x, y = pos[0], pos[1]
        self.inQueue.put(x)
        self.inQueue.put(y)
        self.computer.compute()
        res = self.outQueue.get(True)
        # print("(", x, ",", y, ") : ", res)
        return res

    def printField(self):
        for y in range(self.height):
            s = ""
            for x in range(self.width):
                pos = (x, y)
                if pos in self.field:
                    res = self.field[pos]
                    s += "." if res == 0 else "#"
                else:
                    s += " "
            print(s)

    def scanArea(self, width, height):
        self.width = width
        self.height = height
        self.field = {}
        numPulls = 0
        for y in range(self.height):
            for x in range(self.width):
                res = self.checkAtPosition((x, y))
                self.field[(x, y)] = res
                if res == 1:
                    numPulls += 1
        return numPulls
