from IntComputer import IntComputer, IntComputerThread
from queue import Queue, Empty


class HullPaintingRobot:
    def __init__(self, program):
        self.program = program.copy()
        self.pos = (0, 0)
        self.visited = {}
        self.direction = 0

    def paintTurnAndMove(self, newColor, turnDirection):
        self.visited[self.pos] = newColor
        if turnDirection == 0:
            self.direction = 3 if self.direction == 0 else self.direction - 1
        elif turnDirection == 1:
            self.direction = 0 if self.direction == 3 else self.direction + 1
        else:
            print("ERROR: invalid turn direction: ", turnDirection)
            return None
        x, y = self.pos[0], self.pos[1]
        if self.direction == 0:
            self.pos = (x, y+1)
        elif self.direction == 1:
            self.pos = (x+1, y)
        elif self.direction == 2:
            self.pos = (x, y-1)
        elif self.direction == 3:
            self.pos = (x-1, y)
        else:
            print("ERROR: invalid direction: ", self.direction)
            return None
        if self.pos in self.visited:
            return self.visited[self.pos]
        else:
            return 0

    def run(self):
        inQueue = Queue()
        outQueue = Queue()
        computer = IntComputer(self.program, inQueue, outQueue)
        cThread = IntComputerThread(computer)
        inQueue.put(0)
        cThread.start()
        color = None
        turn = None
        while cThread.is_alive():
            if color is None:
                try:
                    color = outQueue.get(True,5)
                except Empty:
                    continue
            if turn is None:
                try:
                    turn = outQueue.get(True,5)
                except Empty:
                    continue
            newColor = self.paintTurnAndMove(color, turn)
            color = None
            turn = None
            inQueue.put(newColor)

