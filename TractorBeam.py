from IntComputer import IntComputer, IntComputerThread
from queue import  Queue, Empty
import copy
import pygame

class TractorBeam:

    (WINWIDTH, WINHEIGHT) = (1000, 1000)

    BACKGROUDCOLOR = pygame.color.THECOLORS['gray']
    PULLEDCOLOR = pygame.color.THECOLORS["blue"]
    STATIONARYCOLOR = pygame.color.THECOLORS["green"]
    SANTACOLOR = pygame.color.THECOLORS["red"]

    def __initDraw(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINWIDTH, self.WINHEIGHT))
        pygame.display.set_caption("Tractor Beam")
        self.screen.fill(self.BACKGROUDCOLOR)

    def __drawPoint(self, pos, t):
        if t == 0:
            color = self.STATIONARYCOLOR
        else:
            color = self.PULLEDCOLOR
        self.screen.set_at(pos, color)
        # pygame.draw.circle(self.screen, color, pos, 5)
        pygame.display.update()

    def __drawCircle(self, pos, t):
        if t == 0:
            color = self.STATIONARYCOLOR
        else:
            color = self.PULLEDCOLOR
        pygame.draw.circle(self.screen, color, pos, 5)
        pygame.display.update()

    def __drawSmart(self, point, pos, width):
        scale = self.WINWIDTH // width
        t = self.checkOrGet(point)
        if self.checkSanta(point):
            color = self.SANTACOLOR
        elif t == 0:
            color = self.STATIONARYCOLOR
        else:
            color = self.PULLEDCOLOR
        spos = (pos[0] * scale, pos[1] * scale)
        pygame.draw.circle(self.screen, color, spos, 2)
        pygame.display.update()


    def __init__(self, filename):
        self.program = IntComputer.readProgram(filename)
        self.inQueue = Queue()
        self.outQueue = Queue()
        self.field = {}
        self.width = 0
        self.height = 0
        self.screen = None
        self.__initDraw()
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

    def scanArea(self, width, height, xOffset = 0, yOffset = 0):
        self.width = width
        self.height = height
        self.field = {}
        numPulls = 0
        for y in range(yOffset, yOffset + self.height + 1):
            for x in range(xOffset, xOffset + self.width + 1):
                self.__clearEvents()
                res = self.checkAtPosition((x, y))
                self.field[(x, y)] = res
                self.__drawPoint((x-xOffset, y-yOffset), res)
                if res == 1:
                    numPulls += 1
        return numPulls

    def findSanta1(self, santaWidth, santaHeight, maxWidth, maxHeight):
        self.width = maxWidth
        self.height = maxHeight
        self.field = {}
        stop = False
        xOffset = 500
        yOffset = 00
        minx = 9
        maxx = 20
        y = 500
        while not stop:
            minxCur = minx
            maxxCur = maxx
            onLeft = True
            for x in range(minxCur, maxxCur + 1):
                self.__clearEvents()
                res = self.checkAtPosition((x, y))
                self.field[(x, y)] = res
                self.__drawPoint((x, y), res)
                if res == 1:
                    onLeft = False
                    if maxx < x+5:
                        maxx = x+5
                elif onLeft:
                    if minx < x-5:
                        minx = x-5
            y += 1
            if y > self.height:
                stop = True

    def checkOrGet(self, pos):
        if pos not in self.field:
            self.field[pos] = self.checkAtPosition(pos)
        return self.field[pos]

    def isPulled(self, pos):
        return self.checkOrGet(pos) == 1

    def checkSanta(self, pos):
        x, y = pos[0], pos[1]
        return self.isPulled((x, y)) and self.isPulled((x+99, y)) \
               and self.isPulled((x, y+99)) and self.isPulled((x+99, y+99))

    def findSanta(self, santaWidth, santaHeight, maxWidth, maxHeight):
        # self.width = maxWidth
        # self.height = maxHeight
        self.field = {}
        stop = False
        xOffset = 1820
        yOffset = 1980
        startx = xOffset
        starty = yOffset
        interval = 1
        numpoints = 20
        self.width = interval * numpoints
        self.height = interval * numpoints
        step = 0
        while not stop:
            self.__clearEvents()
            x = startx + interval * step
            for y in range(starty, starty+interval*(step + 1), interval):
                self.__drawSmart((x, y), (x-xOffset, y-yOffset), self.width)
            y = starty + interval * step
            for x in range(startx, startx+interval*step, interval):
                self.__drawSmart((x, y), (x-xOffset, y-yOffset), self.width)
            step += 1
            if startx+interval*step-xOffset > self.width or starty+interval*step-yOffset > self.height:
                stop = True


    def __clearEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Close the program any way you want, or troll users who want to close your program.
                print("QUIT received")
                # self.halt = True


    def waitToClose(self):
        running = True
        while running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                running = False  # Be IDLE friendly
        pygame.quit()
