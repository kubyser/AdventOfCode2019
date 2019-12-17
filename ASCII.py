from IntComputer import IntComputer, IntComputerThread
from queue import Queue, Empty
import pygame

class ASCII:
    (WINWIDTH, WINHEIGHT) = (800, 800)

    BACKGROUDCOLOR = pygame.color.THECOLORS['gray']
    SCAFFCOLOR = pygame.color.THECOLORS["black"]
    ROBOTCOLORS = (pygame.color.THECOLORS["green"], pygame.color.THECOLORS["blue"])

    def __init__(self, fileName, interactive = False):
        self.program = IntComputer.readProgram(fileName)
        if interactive:
            self.program[0] = 2
        self.field = {}
        self.inQueue = Queue()
        self.outQueue = Queue(10)
        self.computer = IntComputerThread(IntComputer(self.program, self.inQueue, self.outQueue))
        self.screen = None
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        self.blockWidth = 0
        self.blockHeight = 0
        self.rescalingRequired = False
        self.halt = False

    def sendToRobot(self, instruction):
        for x in list(instruction):
            a = ord(x)
            self.inQueue.put(a)
        self.inQueue.put(10)


    def __initDraw(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINWIDTH, self.WINHEIGHT))
        pygame.display.set_caption("ASCII")
        self.screen.fill(self.BACKGROUDCOLOR)

    def __getTileRect(self, xPos, yPos):
        if self.rescalingRequired:
            self.blockWidth = self.WINWIDTH // (self.maxX - self.minX + 1)
            self.blockHeight = self.WINHEIGHT // (self.maxY - self.minY + 1)
            self.rescalingRequired = False
        return (xPos - self.minX) * self.blockWidth, (yPos - self.minY) * self.blockHeight

    def __drawScaffolding(self, x, y, width, height):
        pygame.draw.rect(self.screen, self.SCAFFCOLOR, pygame.Rect(x+1, y+1, width-2, height-2))

    def __drawRobot(self, x, y, width, height, direction):
        x1 = None
        x2 = None
        y1 = None
        y2 = None
        if direction == 0:
            x1 = x+width//2 - width//8
            y1 = y
            x2 = x+width//2 + width//8
            y2 = y + height//2
        elif direction == 1:
            x1 = x+width//2
            y1 = y+height//2 - height//8
            x2 = x + width
            y2 = y+height//2 + height//8
        elif direction == 2:
            x1 = x+width//2 - width//8
            y1 = y + height//2
            x2 = x+width//2 + width//8
            y2 = y + height
        elif direction == 3:
            x1 = x
            y1 = y+height//2 - height//8
            x2 = x + width//2
            y2 = y+height//2 + height//8
        else:
            x1 = x
            x2 = x + width
            y1 = y
            y2 = y + height
        pygame.draw.rect(self.screen, self.ROBOTCOLORS[1], pygame.Rect(x1, y1, x2-x1+1, y2-y1+1))
        pygame.draw.ellipse(self.screen, self.ROBOTCOLORS[0], pygame.Rect(x+width//2-width//4, y+height//2-height//4,
                                                                          width//2, height//2))

    def __isIntersection(self, x, y):
        if (x-1, y) not in self.field or (x+1, y) not in self.field \
                or (x, y-1) not in self.field or (x, y+1) not in self.field:
            return False
        if self.field[(x-1, y)] not in ("#", "^", "v", ">", "<"):
            return False
        if self.field[(x+1, y)] not in ("#", "^", "v", ">", "<"):
            return False
        if self.field[(x, y-1)] not in ("#", "^", "v", ">", "<"):
            return False
        if self.field[(x, y+1)] not in ("#", "^", "v", ">", "<"):
            return False
        return True

    def calculateIntersectionsAlignment(self):
        res = 0
        for i in range(self.minX, self.maxX + 1):
            for j in range(self.minY, self.maxY + 1):
                if (i, j) not in self.field:
                    continue
                t = self.field[(i, j)]
                if t in ("#", "^", "v", ">", "<"):
                    if self.__isIntersection(i, j):
                        res += i * j
        return res



    def __drawField(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Close the program any way you want, or troll users who want to close your program.
                print("QUIT received")
                #self.halt = True
        self.screen.fill(self.BACKGROUDCOLOR)
        for i in range(self.minX, self.maxX + 1):
            for j in range(self.minY, self.maxY + 1):
                if (i, j) not in self.field:
                    continue
                t = self.field[(i, j)]
                x, y = self.__getTileRect(i, j)
                if t == "#":
                    self.__drawScaffolding(x, y, self.blockWidth, self.blockHeight)
                elif t == "^":
                    self.__drawRobot(x, y, self.blockWidth, self.blockHeight, 0)
                elif t == "v":
                    self.__drawRobot(x, y, self.blockWidth, self.blockHeight, 2)
                elif t == ">":
                    self.__drawRobot(x, y, self.blockWidth, self.blockHeight, 1)
                elif t == "<":
                    self.__drawRobot(x, y, self.blockWidth, self.blockHeight, 3)
                elif t == "X":
                    self.__drawRobot(x, y, self.blockWidth, self.blockHeight, 4)
        pygame.display.update()

    def run(self):
        xPos = 0
        yPos = 0
        s = ""
        self.__initDraw()
        self.computer.start()
        n = None
        while not self.halt and (self.computer.is_alive() or not self.outQueue.empty()):
#            if self.outQueue.empty():
#                self.__drawField()
            try:
                n = self.outQueue.get(True, 5)
            except Empty:
                continue
            c = chr(n)
            if n == 10:
                #print(s)
                if s == "":
                    xPos = 0
                    yPos = 0
                    self.__drawField()
                else:
                    yPos += 1
                    xPos = 0
                s = ""
            else:
                self.field[(xPos, yPos)] = c
                s += c
                if xPos < self.minX:
                    self.minX = xPos
                    self.rescalingRequired = True
                if xPos > self.maxX:
                    self.maxX = xPos
                    self.rescalingRequired = True
                if yPos < self.minY:
                    self.minY = yPos
                    self.rescalingRequired = True
                if yPos > self.maxY:
                    self.maxY = yPos
                    self.rescalingRequired = True
                xPos += 1
        if n is not None:
            print(n)
        #self.__drawField()
        self.computer.join()
        return n

    def waitToClose(self):
        running = True
        while running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                running = False  # Be IDLE friendly
        pygame.quit()
