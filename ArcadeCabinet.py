from IntComputer import IntComputerThread, IntComputer
from queue import Queue, Empty
import pygame
import time

class ArcadeCabinet:

    (WINWIDTH, WINHEIGHT) = (640, 640)
    SCOREOFFSET = 30

    BACKGROUDCOLOR = pygame.color.THECOLORS['gray']
    WALLCOLOR = pygame.color.THECOLORS["black"]
    BLOCKCOLORS = ((pygame.color.THECOLORS["green"], pygame.color.THECOLORS["blue"]),
                   (pygame.color.THECOLORS["darkgreen"], pygame.color.THECOLORS["navyblue"]))
    PADDLECOLOR = pygame.color.THECOLORS["orange"]
    BALLCOLOR = pygame.color.THECOLORS["red"]
    TEXTCOLOR = pygame.color.THECOLORS["black"]
    SLEEPTIME = 0.01

    class Controller:
        def __init__(self):
            self.ballX = None
            self.paddleX = None

        def getAction(self):
            action = 0
            if self.paddleX is None or self.ballX is None:
                return 0
            if self.ballX < self.paddleX:
                action = -1
            elif self.ballX > self.paddleX:
                action = 1
            return action

    def __init__(self, program):
        self.field = {}
        self.program = program
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        self.blockSizeX = 0
        self.blockSizeY = 0
        self.screen = None
        self.score = 0
        self.controller = self.Controller()
        self.rescalingRequired = False

    def getNumTiles(self, t = None):
        if t is None:
            return len(self.field.keys())
        c = 0
        for x in self.field.values():
            if x == t:
                c += 1
        return c

    def getScreenPos(self, x, y):
        screenX = (x - self.minX) * self.blockSizeX
        screenY = (y - self.minY) * self.blockSizeY + self.SCOREOFFSET
        return screenX, screenY


    def initDraw(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINWIDTH, self.WINHEIGHT))
        pygame.display.set_caption("Advent of Code Arcade")
        self.screen.fill(self.BACKGROUDCOLOR)

    def drawTile(self, x, y):
        if self.rescalingRequired:
            self.drawField()
        else:
            item = self.field[(x, y)]
            sX, sY = self.getScreenPos(x, y)
            if item == 1:
                color = self.WALLCOLOR
            elif item == 2:
                cx = x % 2
                cy = x % 2
                color = self.BLOCKCOLORS[cx][cy]
            elif item == 3:
                color = self.PADDLECOLOR
            elif item == 4:
                color = self.BALLCOLOR
            else:
                color = self.BACKGROUDCOLOR
            pygame.draw.rect(self.screen, color, pygame.Rect(sX, sY, self.blockSizeX, self.blockSizeY))
            pygame.display.update()

    def drawScore(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(str(self.score), True, self.TEXTCOLOR)
        textRect = text.get_rect()
        textRect.center = (self.WINWIDTH // 2, self.SCOREOFFSET // 2)
        pygame.draw.rect(self.screen, self.BACKGROUDCOLOR, pygame.Rect(0, 0, self.WINWIDTH, self.SCOREOFFSET))
        self.screen.blit(text, textRect)
        pygame.display.update()


    def drawField(self):
        for a in self.field.keys():
            if a[0] < self.minX:
                self.minX = a[0]
            elif a[0] > self.maxX:
                self.maxX = a[0]
            if a[1] < self.minY:
                self.minY = a[1]
            elif a[1] > self.maxY:
                self.maxY = a[1]
        self.blockSizeX = self.WINWIDTH // (self.maxX - self.minX + 1)
        self.blockSizeY = (self.WINHEIGHT - self.SCOREOFFSET) // (self.maxY - self.minY + 1)
        self.rescalingRequired = False
        self.screen.fill(self.BACKGROUDCOLOR)
        for a in self.field.keys():
            x, y = self.getScreenPos(a[0], a[1])
            item = self.field[a]
            if item == 1:
                color = self.WALLCOLOR
            elif item == 2:
                cx = a[0] % 2
                cy = a[1] % 2
                color = self.BLOCKCOLORS[cx][cy]
            elif item == 3:
                color = self.PADDLECOLOR
            elif item == 4:
                color = self.BALLCOLOR
            else:
                color = self.BACKGROUDCOLOR
            pygame.draw.rect(self.screen, color, pygame.Rect(x, y, self.blockSizeX, self.blockSizeY))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(str(self.score), True, self.TEXTCOLOR)
        textRect = text.get_rect()
        textRect.center = (self.WINWIDTH // 2, self.SCOREOFFSET // 2)
        self.screen.blit(text, textRect)
        pygame.display.update()



    def run(self, initOnly = False):
        if not initOnly:
            self.program[0] = 2
        inQueue = Queue()
        outQueue = Queue()
        computer = IntComputerThread(IntComputer(self.program, inQueue, outQueue))
        computer.start()
        x = None
        y = None
        t = None
        self.initDraw()
        while computer.is_alive() or not outQueue.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                # Close the program any way you want, or troll users who want to close your program.
                    print("QUIT received")
                    #self.halt = True
            if inQueue.empty() and outQueue.empty():
                time.sleep(self.SLEEPTIME)
                inQueue.put(self.controller.getAction())
            if x is None:
                try:
                    x = outQueue.get(True, 0.1)
                except Empty:
                    continue
            if y is None:
                try:
                    y = outQueue.get(True, 0.1)
                except Empty:
                    continue
            if t is None:
                try:
                    t = outQueue.get(True, 0.1)
                except Empty:
                    continue
            if x == -1 and y == 0:
                #print("Score=", t)
                self.score = t
                self.drawScore()
            else:
                if x < self.minX or x > self.maxX or y < self.minY or y > self.maxY:
                    self.rescalingRequired = True
                self.field[(x,y)] = t
                if t == 3:
                    self.controller.paddleX = x
                elif t == 4:
                    self.controller.ballX = x
                self.drawTile(x, y)
            #print("Got tile: (", x, ",", y,") : ", t)
            x = None
            y = None
            t = None
        computer.join()
        running = True
        while running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                running = False  # Be IDLE friendly
        pygame.quit()


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
                    c = self.field[(i+minX, maxY-j)]
                else:
                    c = 0
                line = line + ('#' if c == 1 else ' ')



