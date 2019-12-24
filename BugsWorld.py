import pygame
from time import sleep
from sys import exit
from math import pow

class BugsWorld:

    (WINWIDTH, WINHEIGHT) = (1000, 1000)
    SCOREOFFSET = 30

    BACKGROUDCOLOR = pygame.color.THECOLORS['gray']
    LIVECOLOR = pygame.color.THECOLORS["red"]
    TEXTCOLOR = pygame.color.THECOLORS["black"]

    DELAY = 0.5

    def __init__(self, width, height, recursive = False, draw = True):
        self.__minutes = 0
        self.__recursive = recursive
        self.__draw = draw
        self.__width = width
        self.__height = height
        self.__field = {}
        self.__screen = None
        self.__initDraw()

    def __initDraw(self):
        if self.__draw:
            pygame.init()
            self.__screen = pygame.display.set_mode((self.WINWIDTH, self.WINHEIGHT))
            pygame.display.set_caption("Bugs World")
            self.__screen.fill(self.BACKGROUDCOLOR)

    def __clearEvents(self):
        if not self.__draw:
            return
        exit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Close the program any way you want, or troll users who want to close your program.
                print("QUIT received")
                exit = True
        return exit

    def __drawCell(self, pos, t):
        if t == 0:
            color = self.BACKGROUDCOLOR
        else:
            color = self.LIVECOLOR
        blockWidth = self.WINWIDTH // self.__width
        blockHeight = (self.WINHEIGHT - self.SCOREOFFSET) // self.__height
        pygame.draw.rect(self.__screen, color, pygame.Rect(blockWidth*pos[0], blockHeight*pos[1] + self.SCOREOFFSET, blockWidth-1, blockHeight-1))

    def __drawScore(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        pygame.draw.rect(self.__screen, self.BACKGROUDCOLOR, pygame.Rect(0, 0, self.WINWIDTH, self.SCOREOFFSET))
        text = font.render(str(self.getBiodiversity()), True, self.TEXTCOLOR)
        textRect = text.get_rect()
        textRect.center = (self.WINWIDTH // 4, self.SCOREOFFSET // 2)
        self.__screen.blit(text, textRect)
        textNum = font.render(str(self.getNumBugs()), True, self.TEXTCOLOR)
        textRect = textNum.get_rect()
        textRect.center = (3 * self.WINWIDTH // 4, self.SCOREOFFSET // 2)
        self.__screen.blit(textNum, textRect)

    def readField(self, field):
        for j in range(len(field)):
            for i in range(len(field[j])):
                c = field[j][i]
                if c == "#":
                    self.__field[(i, j, 0)] = 1
        if self.__draw:
            self.drawField()

    def getBiodiversity(self):
        bio = 0
        for a in self.__field:
            x = a[0]
            y = a[1]
            bio += int(pow(2, y*self.__width + x))
        return bio

    def getNumBugs(self):
        return len(self.__field)

    def drawField(self):
        if not self.__draw:
            return
        self.__screen.fill(self.BACKGROUDCOLOR)
        for a in self.__field:
            self.__drawCell(a, 1)
        self.__drawScore()
        pygame.display.update()

    def close(self):
        if self.__draw:
            pygame.display.quit()
            pygame.quit()
            exit(-1)

    def waitToClose(self):
        if self.__draw:
            running = True
            while running:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    running = False  # Be IDLE friendly
                else:
                    # self.halt = True
                    sleep(0.1)
        self.close()

    def __addToLiveOrEmpty(self, pos, live, empty):
        if pos in self.__field:
            live.add(pos)
        else:
            empty.add(pos)

    def __getNeighbours(self, pos):
        live = set()
        empty = set()
        midX = self.__width // 2
        midY = self.__height // 2
        if pos[0] == 0:
            if self.__recursive:
                self.__addToLiveOrEmpty((midX-1, midY, pos[2]-1), live, empty)
        elif pos[0] == midX+1 and pos[1] == midY and self.__recursive:
            for i in range(self.__height):
                self.__addToLiveOrEmpty((self.__width-1, i, pos[2]+1), live, empty)
        else:
            self.__addToLiveOrEmpty((pos[0] - 1, pos[1], pos[2]), live, empty)

        if pos[0] == self.__width-1:
            if self.__recursive:
                self.__addToLiveOrEmpty((midX+1, midY, pos[2]-1), live, empty)
        elif pos[0] == midX-1 and pos[1] == midY and self.__recursive:
            for i in range(self.__height):
                self.__addToLiveOrEmpty((0, i, pos[2]+1), live, empty)
        else:
            self.__addToLiveOrEmpty((pos[0] + 1, pos[1], pos[2]), live, empty)

        if pos[1] == 0:
            if self.__recursive:
                self.__addToLiveOrEmpty((midX, midY-1, pos[2]-1), live, empty)
        elif pos[1] == midY+1 and pos[0] == midX and self.__recursive:
            for i in range(self.__width):
                self.__addToLiveOrEmpty((i, self.__height-1, pos[2]+1), live, empty)
        else:
            self.__addToLiveOrEmpty((pos[0], pos[1]-1, pos[2]), live, empty)

        if pos[1] == self.__height-1:
            if self.__recursive:
                self.__addToLiveOrEmpty((midX, midY+1, pos[2]-1), live, empty)
        elif pos[1] == midY-1 and pos[0] == midX and self.__recursive:
            for i in range(self.__width):
                self.__addToLiveOrEmpty((i, 0, pos[2]+1), live, empty)
        else:
            self.__addToLiveOrEmpty((pos[0], pos[1]+1, pos[2]), live, empty)
        return live, empty

    def liveOneMinute(self):
        killList = set()
        birthList = set()
        visited = set()
        for a in self.__field:
            live, empty = self.__getNeighbours(a)
            if len(live) != 1:
                killList.add(a)
            for n in empty:
                if n not in visited:
                    visited.add(n)
                    nLive, nEmpty = self.__getNeighbours(n)
                    if len(nLive) in (1, 2):
                        birthList.add(n)
        for k in killList:
            del self.__field[k]
        for b in birthList:
            self.__field[b] = 1
        self.__minutes += 1

    def printField(self):
        minLevel = 0
        maxLevel = 0
        for a in self.__field:
            level = a[2]
            if level < minLevel:
                minLevel = level
            if level > maxLevel:
                maxLevel = level
        print("======= After ", self.__minutes, "minutes =======")
        for level in range(minLevel, maxLevel+1):
            print("Depth", level,":")
            for j in range(self.__height):
                s = ""
                for i in range(self.__width):
                    pos = (i, j, level)
                    if self.__recursive and i == self.__width // 2 and j == self.__height // 2:
                        s += "?"
                    elif pos in self.__field:
                        s += "#"
                    else:
                        s += "."
                print(s)
            print("")

    def run(self, minutes=0, stopOnRepeatingBiodiversities=False):
        bioDiversities = set()
        bioDiversities.add(self.getBiodiversity())
        running = True
        quitReceived = False
        doneMinutes = 0
        while running and not quitReceived and (minutes == 0 or doneMinutes < minutes):
            quitReceived = self.__clearEvents()
            self.liveOneMinute()
            if stopOnRepeatingBiodiversities:
                nBio = self.getBiodiversity()
                if nBio in bioDiversities:
                    print("Repeating biodiversity: ", nBio)
                    running = False
                else:
                    bioDiversities.add(nBio)
            self.drawField()
            if self.__draw:
                sleep(self.DELAY)
            doneMinutes += 1
        if quitReceived:
            self.close()
        else:
            self.waitToClose()

