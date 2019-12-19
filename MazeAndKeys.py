import copy

class MazeAndKeys:

    __keysSet = "abcdefghijklmnopqrstuvwxyz"
    __doorsSet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, mazeStrings):
        self.__maze = {}
        self.__keysInMap = {}
        self.__startPos = (None, None)
        self.__maxX = 0
        self.__maxY = 0
        self.__exploredKeySets = {}
        self.__minTotalDistance = None
        self.__buildMaze(mazeStrings)

    def __buildMaze(self, sMaze):
        for j in range(len(sMaze)):
            for i in range(len(sMaze[j])):
                if i > self.__maxX:
                    self.__maxX = i
                if j > self.__maxY:
                    self.__maxY = j
                s = sMaze[j][i]
                if s == "#":
                    self.__maze[(i, j)] = "#"
                elif s == "@":
                    self.__startPos = (i, j)
                elif s in self.__keysSet:
                    self.__keysInMap[s] = (i, j)
                    self.__maze[(i, j)] = s
                elif s in self.__doorsSet:
                    self.__maze[(i, j)] = s

    def printMaze(self):
        for j in range(self.__maxY+1):
            s = ""
            for i in range(self.__maxX+1):
                if (i, j) == self.__startPos:
                    s += "@"
                elif (i, j) in self.__maze:
                    s += self.__maze[(i, j)]
                else:
                    s += " "
            print(s)

    def __printMazeDebug(self, visited, newNodes):
        for j in range(self.__maxY+1):
            s = ""
            for i in range(self.__maxX+1):
                if (i, j) in visited:
                    s += "%"
                elif (i,j) in newNodes:
                    s += "+"
                elif (i, j) == self.__startPos:
                    s += "@"
                elif (i, j) in self.__maze:
                    s += self.__maze[(i, j)]
                else:
                    s += " "
            print(s)


    def __keyChar(self, doorChar):
        return doorChar.lower()

    def __isAccessible(self, pos, keysCollected, visited):
        if pos in visited:
            return False
        if pos not in self.__maze:
            return True
        s = self.__maze[pos]
        if s in self.__doorsSet:
            if self.__keyChar(s) in keysCollected:
                return True
        if s in self.__keysSet:
            return True
        return False


    def __findAccessibleNeighbours(self, pos, keysCollected, visited):
        res = []
        nPos = (pos[0]-1, pos[1])
        if self.__isAccessible(nPos, keysCollected, visited):
            res.append(nPos)
        nPos = (pos[0]+1, pos[1])
        if self.__isAccessible(nPos, keysCollected, visited):
            res.append(nPos)
        nPos = (pos[0], pos[1]-1)
        if self.__isAccessible(nPos, keysCollected, visited):
            res.append(nPos)
        nPos = (pos[0], pos[1]+1)
        if self.__isAccessible(nPos, keysCollected, visited):
            res.append(nPos)
        return res

    def __exploreNode(self, pos, keysCollected, visited):
        if pos in visited:
            print("ERROR: pos in visited: ", pos)
            return None, None
        visited.add(pos)
        newNodes = self.__findAccessibleNeighbours(pos, keysCollected, visited)
        return newNodes, visited

    def __exploreFrom(self, pos, keysCollected):
        visited = set()
        dist = 0
        stop = False
        searchNodes = [pos]
        keysInSearch = {}
        skipNodes = set()
        while not stop:
            newNodes = []
            for x in searchNodes:
                if x not in skipNodes and  x in self.__keysInMap.values():
                    k = self.__maze[x]
                    if k in keysInSearch:
                        print("ERROR: key already in search: ", k)
                    if k not in keysCollected:
                        keysInSearch[k] = dist
                        skipNodes.add(x)
                nodes, visited = self.__exploreNode(x, keysCollected, visited)
                for n in nodes:
                    if n not in newNodes:
                        newNodes.append(n)
                        if x in skipNodes:
                            skipNodes.add(x)
            if len(newNodes) == 0:
                stop = True
            else:
                dist += 1
                #self.__printMazeDebug(visited, newNodes)
                #print("Depth ", dist)
                #input("Enter to continue...")
                searchNodes = newNodes
        return keysInSearch

    def __routeAlreadyExplored(self, k, keysCollected, distance):
        if k not in self.__exploredKeySets:
            return False
        routes = self.__exploredKeySets[k]
        c = "".join(sorted(keysCollected))
        if c not in routes:
            return False
        prevDist = routes[c]
        return distance >= prevDist

    def __addRouteToAlreadyExplored(self, k, keysCollected, distance):
        if k not in self.__exploredKeySets:
            self.__exploredKeySets[k] = {}
        self.__exploredKeySets[k]["".join(sorted(keysCollected))] = distance

    def __buildRoutesWide(self):
        minDistance = None
        bestRoute = None
        pos = self.__startPos
        keysCollected = []
        keysToExplore = [(pos, keysCollected, 0)]
        stop = False
        depth = 0
        while not stop:
            print("At depth ", depth)
            depth += 1
            newKeysToExplore = []
            for (pos, keysCollected, dist) in keysToExplore:
                newKeysCollected = copy.deepcopy(keysCollected)
                if pos in self.__maze:
                    if self.__maze[pos] in self.__keysSet:
                        newKeysCollected.append(self.__maze[pos])
                newKeys = self.__exploreFrom(pos, newKeysCollected)
                if not newKeys:
                    if True if minDistance is None else dist < minDistance:
                        minDistance = dist
                        bestRoute = newKeysCollected
                else:
                    for k in newKeys.keys():
                        newKeyPos = self.__keysInMap[k]
                        newDist = dist + newKeys[k]
                        if not self.__routeAlreadyExplored(k, newKeysCollected, newDist):
                            newKeysToExplore.append((newKeyPos, newKeysCollected, newDist))
                            self.__addRouteToAlreadyExplored(k, newKeysCollected, newDist)
            if len(newKeysToExplore) == 0:
                stop = True
            else:
                keysToExplore = newKeysToExplore
        return minDistance, bestRoute


    def __buildRoutesFrom(self, pos, keysCollected = [], startDist = 0, bestDistance = None):
        minTotalDistance = bestDistance
        bestKeysCollected = None
        keysInSearch = self.__exploreFrom(pos, keysCollected)
        if not keysInSearch:
            print("Found route with steps ", startDist, "route: ", keysCollected)
            return startDist, keysCollected
        keysSorted = [k for k, v in sorted(keysInSearch.items(), key=lambda item: item[1])]
        for k in keysSorted:
            if minTotalDistance is not None:
                if startDist + keysInSearch[k] >= minTotalDistance:
                    #print("Skipping a route")
                    continue
            if self.__routeAlreadyExplored(k, keysCollected, startDist + keysInSearch[k]):
                #print("Route already explored, skipping")
                continue
            else:
                if k not in self.__exploredKeySets:
                    self.__exploredKeySets[k] = {}
                self.__exploredKeySets[k]["".join(sorted(keysCollected))] = startDist + keysInSearch[k]
            newKeysCollected = copy.deepcopy(keysCollected)
            newKeysCollected.append(k)
            #print("Trying route ", newKeysCollected)
            dist, totalKeysCollected = self.__buildRoutesFrom(self.__keysInMap[k], newKeysCollected, startDist + keysInSearch[k], minTotalDistance)
            if dist is not None:
                if len(totalKeysCollected) != len(self.__keysInMap):
                    print("ERROR: searching completed but not all keys found")
                else:
                    if True if minTotalDistance is None else dist < minTotalDistance:
                        minTotalDistance = dist
                        bestKeysCollected = totalKeysCollected
        if bestKeysCollected is None:
            return None, None
        else:
            return minTotalDistance, bestKeysCollected

    def solve(self):
        #minDist, keysCollected = self.__buildRoutesFrom(self.__startPos)
        minDist, keysCollected = self.__buildRoutesWide()
        return minDist, keysCollected


