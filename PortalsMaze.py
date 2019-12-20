import copy

class PortalsMaze:

    __portalChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, mapLines):
        self.__maze = {}
        self.__maxX, self.__maxY = 0, 0
        self.__portalsByPos = {}
        self.__unPairedPortalByLabel = {}
        self.__buildMaze(mapLines)
        if "AA" not in self.__unPairedPortalByLabel:
            raise Exception("Entry point AA not detected")
        self.__startPos = self.__unPairedPortalByLabel["AA"]
        if "ZZ" not in self.__unPairedPortalByLabel:
            raise Exception("Exit point ZZ not detected")
        self.__endPos = self.__unPairedPortalByLabel["ZZ"]

    def __isPortalChar(self, pos):
        if pos not in self.__maze:
            return False
        if self.__maze[pos] in self.__portalChars:
            return True
        return False

    def printMaze(self):
        for j in range(self.__maxY+1):
            s = ""
            for i in range(self.__maxX+1):
                if (i, j) in self.__portalsByPos:
                    s += "+"
                elif (i, j) in self.__maze:
                    s += self.__maze[(i, j)]
                else:
                    s += " "
            print(s)
        for x in self.__portalsByPos:
            print("Portal at:", x, ": ", self.__portalsByPos[x])
        for x in self.__unPairedPortalByLabel:
            print("Unpaired portal: ", x, " at ", self.__unPairedPortalByLabel[x])



    def __buildMaze(self, sMaze):
        for j in range(len(sMaze)):
            for i in range(len(sMaze[j])):
                if i > self.__maxX:
                    self.__maxX = i
                if j > self.__maxY:
                    self.__maxY = j
                s = sMaze[j][i]
                if s in {"#", "."} or s in self.__portalChars:
                    self.__maze[(i, j)] = s
                elif s != " ":
                    raise Exception("Unexpected character in map", (i, j), s)
        for y in range(self.__maxY):
            for x in range(self.__maxX):
                if self.__isPortalChar((x, y)):
                    pos = (x, y)
                    linkPos = None
                    c1 = self.__maze[pos]
                    del self.__maze[pos]
                    if self.__isPortalChar((x+1, y)):
                        label = c1 + self.__maze[(x+1, y)]
                        del self.__maze[(x+1, y)]
                        if self.__maze.get((x-1, y), "") == ".":
                            linkPos = (x-1, y)
                        if self.__maze.get((x+2, y), "") == ".":
                            if linkPos is not None:
                                raise Exception("Link spaces on both sides of label " + label)
                            linkPos = (x+2, y)
                        if linkPos is None:
                            raise Exception("No links on either side of label " + label)
                    elif self.__isPortalChar((x, y+1)):
                        label = c1 + self.__maze[(x, y+1)]
                        del self.__maze[(x, y+1)]
                        if self.__maze.get((x, y-1), "") == ".":
                            linkPos = (x, y-1)
                        if self.__maze.get((x, y+2), "") == ".":
                            if linkPos is not None:
                                raise Exception("Link spaces on both sides of label " + label)
                            linkPos = (x, y+2)
                        if linkPos is None:
                            raise Exception("No links on either side of label " + label)
                    else:
                        raise Exception("No second char in portal label", c1)
                    if label in self.__unPairedPortalByLabel:
                        otherPos = self.__unPairedPortalByLabel[label]
                        if linkPos in self.__portalsByPos or otherPos in self.__portalsByPos:
                            raise Exception("Unpaired portal already in portals list")
                        self.__portalsByPos[linkPos] = (label, otherPos)
                        self.__portalsByPos[otherPos] = (label, linkPos)
                        del self.__unPairedPortalByLabel[label]
                    else:
                        self.__unPairedPortalByLabel[label] = linkPos

    def __isAccessible(self, pos):
        if pos not in self.__maze:
            return False
        if self.__maze[pos] != ".":
            return False
        return True

    def __findNeighboursOf(self, pos):
        res = []
        nPos = (pos[0]-1, pos[1])
        if self.__isAccessible(nPos):
            res.append((nPos, None))
        nPos = (pos[0]+1, pos[1])
        if self.__isAccessible(nPos):
            res.append((nPos, None))
        nPos = (pos[0], pos[1]-1)
        if self.__isAccessible(nPos):
            res.append((nPos, None))
        nPos = (pos[0], pos[1]+1)
        if self.__isAccessible(nPos):
            res.append((nPos, None))
        if pos in self.__portalsByPos:
            portal = self.__portalsByPos[pos]
            label = portal[0]
            nPos = portal[1]
            res.append((nPos, label))
        return res

    def __seachFrom(self, startPos):
        visited = set()
        steps = 0
        searchNodes = [(startPos, [])]
        stop = False
        while not stop:
            newNodes = []
            for x in searchNodes:
                pos = x[0]
                portalsVisited = x[1]
                if pos == self.__endPos:
                    return steps, portalsVisited
                nodes = self.__findNeighboursOf(pos)
                for n in nodes:
                    if n[0] not in visited:
                        visited.add(n[0])
                        if n[1] is not None:
                            portal = n[1]
                            newPortalsVisited = copy.deepcopy(portalsVisited)
                            newPortalsVisited.append(portal)
                        else:
                            newPortalsVisited = portalsVisited
                        newNodes.append((n[0], newPortalsVisited))
            if len(newNodes) == 0:
                stop = True
            else:
                steps += 1
                searchNodes = newNodes
        return None, None

    def findPath(self):
        return self.__seachFrom(self.__startPos)



