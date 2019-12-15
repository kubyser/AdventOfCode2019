from IntComputer import IntComputer, IntComputerThread
from queue import Queue


class RepairDroid:

    class Cell:
        def __init__(self, x, y, t = None):
            self.x = x
            self.y = y
            self.type = t
            self.distance = None
            self.previous = None

    def __init__(self, program):
        self.program = program
        self.field = {}
        self.unexplored = []
        self.xPos = 0
        self.yPos = 0
        startCell = self.Cell(0, 0, 1)
        startCell.distance = 0
        self.field[(0, 0)] = startCell
        self.inQueue = Queue()
        self.outQueue = Queue()
        self.computer = IntComputerThread(IntComputer(self.program, self.inQueue, self.outQueue))

    def sendAndRead(self, command):
        if not self.outQueue.empty():
            print("ERROR: going to send new command, but out queue is not empty")
            return None
        self.inQueue.put(command)
        r = self.outQueue.get(True)
        return r

    def exploreAndReturn(self, direction):
        x = self.xPos
        y = self.yPos
        cell = self.field[(self.xPos, self.yPos)]
        oppositeDirection = None
        if direction == 1:
            y += 1
            oppositeDirection = 2
        elif direction == 2:
            y -= 1
            oppositeDirection = 1
        elif direction == 3:
            x -= 1
            oppositeDirection = 4
        elif direction == 4:
            x += 1
            oppositeDirection = 3
        else:
            print("ERROR: invalid direction: ", direction)
        if (x,y) in self.field:
            nCell = self.field[(x, y)]
            if nCell.distance > cell.distance + 1:
                print("ERROR: neighbouring cell has distance ", nCell.distance, ", expected ", cell.distance + 1)
            return None, None
        nCell = self.Cell(x, y)
        nCell.distance = cell.distance + 1
        nCell.previous = cell
        res = self.sendAndRead(direction)
        if res == 0:
            nCell.type = 0
            #print("WALL   : (", x, ",", y, ")")
        elif res == 1 or res == 2:
            #print("TYPE", res, ": (", x, ",", y, ")")
            nCell.type = res
            r2 = self.sendAndRead(oppositeDirection)
            if r2 != 1:
                print("ERROR: returned back but cell no longer accessible")
                return None
        else:
            print("ERROR: invalid response: ", res)
            return None
        self.field[(x, y)] = nCell
        return res, nCell

    def exploreAround(self):
        if (self.xPos, self.yPos) not in self.field:
            print("ERROR: own position not in known field")
            return None
        for direction in range(1, 5):
            res, nCell = self.exploreAndReturn(direction)
            if res == 2:
                print("Success! Found the oxygen system and returning!")
                return nCell
        return None

    def getDirectionToNeighbour(self, targetCell, fromCell = None):
        if fromCell is None:
            x = self.xPos
            y = self.yPos
        else:
            x = fromCell.x
            y = fromCell.y
        xt = targetCell.x
        yt = targetCell.y
        if xt == x and yt == y + 1:
            return 1
        elif xt == x and yt == y - 1:
            return 2
        elif xt == x - 1 and yt == y:
            return 3
        elif xt == x + 1 and yt == y:
            return 4
        else:
            print("ERROR: neighbour not neighbour")
            return None

    def goTo(self, targetCell):
        if self.xPos == targetCell.x and self.yPos == targetCell.y:
            return
        pathCells = {}
        cCell = targetCell
        while cCell.x != 0 or cCell.y != 0:
            pathCells[cCell.previous] = cCell
            cCell = cCell.previous
        while self.xPos != 0 or self.yPos != 0:
            cCell = self.field[(self.xPos, self.yPos)]
            if cCell in pathCells.keys():
                break
            nCell = cCell.previous
            d = self.getDirectionToNeighbour(nCell)
            #print("Backtracking: at ", self.xPos, self.yPos, ", command = ", d)
            res = self.sendAndRead(d)
            if res != 1:
                print("ERROR: backtracking got unexpected cell type: ", res)
                return None
            self.xPos = nCell.x
            self.yPos = nCell.y
        cCell = self.field[(self.xPos, self.yPos)]
        while cCell != targetCell:
            nCell = pathCells[cCell]
            a = self.getDirectionToNeighbour(nCell, cCell)
            #print("Moving along path: command=", a)
            res = self.sendAndRead(a)
            if res != 1:
                print("ERROR: moving along path got unexpected cell type: ", res)
                return None
            cCell = nCell
        self.xPos = targetCell.x
        self.yPos = targetCell.y

    def exploreAllCellsWithDistance(self, targetDistance):
        cellsToExplore = []
        for a in self.field.values():
            if a.distance == targetDistance:
                cellsToExplore.append(a)
        for b in cellsToExplore:
            if b.type == 0:
                continue
            #print("I am at ", self.xPos, self.yPos, "Going to explore (", b.x, ",", b.y, ")")
            self.goTo(b)
            res = self.exploreAround()
            if res is not None:
                return res

    def explore(self):
        self.computer.start()
        distanceToExplore = 0
        res = None
        while distanceToExplore < 1000:
            print("Exploring cells with distance ", distanceToExplore)
            res = self.exploreAllCellsWithDistance(distanceToExplore)
            if res is not None:
                break
            distanceToExplore += 1
        print("Stopping computer")
        self.computer.terminate()
        self.computer.join()
        if res is not None:
            return res.distance
        print("ERROR: got too deep... something's not right")
        return None

    def printField(self):
        minX = 0
        maxX = 0
        minY = 0
        maxY = 0
        for a in self.field.keys():
            if a[0] < minX:
                minX = a[0]
            elif a[0] > maxX:
                maxX = a[0]
            if a[1] < minY:
                minY = a[1]
            elif a[1] > maxY:
                maxY = a[1]
        for j in range(0, maxY - minY + 1):
            line = ''
            for i in range(0, maxX - minX + 1):
                if (i+minX, maxY-j) in self.field:
                    c = self.field[(i+minX, maxY-j)].type
                else:
                    c = -1
                if i+minX == 0 and maxY-j == 0:
                    c = 3
                if c == 0:
                    p = "#"
                elif c == 1:
                    p = "."
                elif c == 2:
                    p = "@"
                elif c == 3:
                    p = "X"
                else:
                    p = " "
                line = line + p
            print(line)

