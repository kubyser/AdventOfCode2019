from IntComputer import IntComputerThread, IntComputer
from queue import Queue, Empty

class ArcadeCabinet:

    def __init__(self, program):
        self.field = {}
        self.program = program

    def getNumTiles(self, t = None):
        if t is None:
            return len(self.field.keys())
        c = 0
        for x in self.field.values():
            if x == t:
                c += 1
        return c

    def run(self):
        inQueue = Queue()
        outQueue = Queue()
        computer = IntComputerThread(IntComputer(self.program, inQueue, outQueue))
        computer.start()
        x = None
        y = None
        t = None
        while computer.is_alive() or not outQueue.empty():
            if x is None:
                try:
                    x = outQueue.get(True, 5)
                except Empty:
                    continue
            if y is None:
                try:
                    y = outQueue.get(True, 5)
                except Empty:
                    continue
            if t is None:
                try:
                    t = outQueue.get(True, 5)
                except Empty:
                    continue
            self.field[(x,y)] = t
            print("Got tile: (", x, ",", y,") : ", t)
            x = None
            y = None
            t = None
        computer.join()


