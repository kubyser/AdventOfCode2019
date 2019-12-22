from IntComputer import IntComputer
from queue import Queue

class SpringDroid:

    def __init__(self, fileName):
        self.__inQueue = Queue()
        self.__outQueue = Queue()
        self.__outputString = ""
        self.__computer = IntComputer(IntComputer.readProgram(fileName), self.__inQueue, self.__outQueue)

    def sendScriptToDroid(self, script):
        IntComputer.sendAsciiListToQueue(script, self.__inQueue)

    def __saveOutputAsString(self):
        s = ""
        while not self.__outQueue.empty():
            val = self.__outQueue.get()
            if val > 255:
                s += str(val)
            else:
                s += chr(val)
        self.__outputString = s

    def getState(self):
        return self.__outputString

    def getStateWithLabels(self):
        state = self.__outputString.splitlines()
        res = ""
        prevIsMap = False
        posDroid = 0
        for s in state:
            if s == "" and prevIsMap:
                res += " " * posDroid
                res += " ABCDEFGHI\n"
                prevIsMap = False
            if len(s) > 0:
                if s[0] in ("#", ".", "@"):
                    prevIsMap = True
            res += s + "\n"
            if s.find("@") != -1:
                posDroid = s.find("@")
        return res

    def run(self):
        self.__computer.compute()
        self.__saveOutputAsString()
