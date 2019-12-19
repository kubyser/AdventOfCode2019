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
        self.__globalMap = {}
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

    def __isAccessibleThroughDoors(self, pos):
        if pos not in self.__maze:
            return True
        s = self.__maze[pos]
        if s in self.__doorsSet or s in self.__keysSet:
            return True
        return False

    def __findAccessibleNeighboursThroughtDoors(self, pos):
        res = []
        nPos = (pos[0]-1, pos[1])
        if self.__isAccessibleThroughDoors(nPos):
            res.append(nPos)
        nPos = (pos[0]+1, pos[1])
        if self.__isAccessibleThroughDoors(nPos):
            res.append(nPos)
        nPos = (pos[0], pos[1]-1)
        if self.__isAccessibleThroughDoors(nPos):
            res.append(nPos)
        nPos = (pos[0], pos[1]+1)
        if self.__isAccessibleThroughDoors(nPos):
            res.append(nPos)
        return res

    def __exploreNodeThroughDoors(self, pos):
        newNodes = self.__findAccessibleNeighboursThroughtDoors(pos)
        return newNodes

    def __backtrackFindingDoors(self, pos, visited):
        doors = set()
        stop = False
        p = pos
        while p is not None:
            if p not in visited:
                print("ERROR: backtracking pos not in visited")
                return None
            else:
                if p in self.__maze:
                    x = self.__maze[p]
                    if x in self.__doorsSet:
                        doors.add(self.__keyChar(x))
                p = visited[p]
        return doors

    def __exploreFromThroughDoors(self, pos):
        visited = {}
        dist = 0
        stop = False
        searchNodes = [pos]
        visited[pos] = None
        if pos in self.__globalMap:
            print("ERROR: source position ", pos, " already in globalmap")
            return None
        self.__globalMap[pos] = {}
        while not stop:
            newNodes = []
            for x in searchNodes:
                if x in self.__keysInMap.values() and x != pos:
                    k = self.__maze[x]
                    if k in self.__globalMap[pos]:
                        print("ERROR: key already in search: ", k)
                    else:
                        doors = self.__backtrackFindingDoors(x, visited)
                        self.__globalMap[pos][k] = (dist, doors)
                nodes = self.__exploreNodeThroughDoors(x)
                for n in nodes:
                    if n not in newNodes and n not in visited:
                        newNodes.append(n)
                        visited[n] = x
            if len(newNodes) == 0:
                stop = True
            else:
                dist += 1
                #self.__printMazeDebug(visited, newNodes)
                #print("Depth ", dist)
                #input("Enter to continue...")
                searchNodes = newNodes

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

    def __buildGlobalMap(self):
        self.__exploreFromThroughDoors(self.__startPos)
        for k in self.__keysInMap.keys():
            self.__exploreFromThroughDoors(self.__keysInMap[k])

    def __findAccessibleKeysInGlobalMap(self, pos, keysCollected):
        res = {}
        if pos not in self.__globalMap:
            print("ERROR: pos ", pos, " not in GlobalMap")
            return None
        mapEntry = self.__globalMap[pos]
        for k in mapEntry:
            if k in keysCollected:
                continue
            allKeysAvailable = True
            keysRequired = self.__globalMap[pos][k][1]
            for reqK in keysRequired:
                if reqK not in keysCollected:
                    allKeysAvailable = False
                    break
            if allKeysAvailable:
                res[k] = self.__globalMap[pos][k][0]
        return res

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
                newKeys = self.__findAccessibleKeysInGlobalMap(pos, newKeysCollected)
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

    def solve(self):
        self.__buildGlobalMap()
        minDist, keysCollected = self.__buildRoutesWide()
        return minDist, keysCollected


