from IntComputer import IntComputerThread, IntComputer
from queue import Queue, Empty
import pygame

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
            #print("Got tile: (", x, ",", y,") : ", t)
            x = None
            y = None
            t = None
        computer.join()

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

    def drawField(self):
        def getScreenPos(x, y):
            screenX = (x - minX) * blockSizeX
            screenY = (y - minY) * blockSizeY
            return screenX, screenY

        (winWidth, winHeight) = (640, 480)
        minX = 0
        maxX = 0
        minY = 0
        maxY = 0
        BACKGROUDCOLOR = pygame.color.THECOLORS['gray']
        WALLCOLOR = pygame.color.THECOLORS["black"]
        BLOCKCOLORS = ((pygame.color.THECOLORS["green"], pygame.color.THECOLORS["blue"]),
                       (pygame.color.THECOLORS["darkgreen"], pygame.color.THECOLORS["navyblue"]))
        PADDLECOLOR = pygame.color.THECOLORS["orange"]
        BALLCOLOR = pygame.color.THECOLORS["red"]
        for a in self.field.keys():
            if a[0] < minX:
                minX = a[0]
            elif a[0] > maxX:
                maxX = a[0]
            if a[1] < minY:
                minY = a[1]
            elif a[1] > maxY:
                maxY = a[1]
        blockSizeX = winWidth // (maxX - minX + 1)
        blockSizeY = winHeight // (maxY - minY + 1)
        pygame.init()
        screen = pygame.display.set_mode((winWidth, winHeight))
        pygame.display.set_caption("Advent of Code Arcade")
        screen.fill(BACKGROUDCOLOR)
        for a in self.field.keys():
            x, y = getScreenPos(a[0], a[1])
            item = self.field[a]
            if item == 1:
                color = WALLCOLOR
            elif item == 2:
                cx = a[0] % 2
                cy = a[1] % 2
                color = BLOCKCOLORS[cx][cy]
            elif item == 3:
                color = PADDLECOLOR
            elif item == 4:
                color = BALLCOLOR
            else:
                color = BACKGROUDCOLOR
            pygame.draw.rect(screen, color, pygame.Rect(x, y, blockSizeX, blockSizeY))
        pygame.display.update()
        running = True
        while running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                running = False  # Be IDLE friendly
        pygame.quit()


