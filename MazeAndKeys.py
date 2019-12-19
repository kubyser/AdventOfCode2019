import copy


class MazeAndKeys:

    __keysSet = "abcdefghijklmnopqrstuvwxyz"
    __doorsSet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, mazeStrings):
        self.__maze = {}
        self.__keysInMap = {}
        self.__startPos = []
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
                    self.__startPos.append((i, j))
                elif s in self.__keysSet:
                    self.__keysInMap[s] = (i, j)
                    self.__maze[(i, j)] = s
                elif s in self.__doorsSet:
                    self.__maze[(i, j)] = s

    def printMaze(self):
        for j in range(self.__maxY+1):
            s = ""
            for i in range(self.__maxX+1):
                if (i, j) in self.__startPos:
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
                elif (i, j) in newNodes:
                    s += "+"
                elif (i, j) in self.__startPos:
                    s += "@"
                elif (i, j) in self.__maze:
                    s += self.__maze[(i, j)]
                else:
                    s += " "
            print(s)

    def __printGlobalMap(self):
        for x in self.__globalMap:
            print(x, ":", self.__globalMap[x])

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
                searchNodes = newNodes

    def __routeAlreadyExplored(self, positions, keysCollected, distance):
        if tuple(positions) not in self.__exploredKeySets:
            return False
        routes = self.__exploredKeySets[tuple(positions)]
        c = "".join(sorted(keysCollected))
        if c not in routes:
            return False
        prevDist = routes[c]
        return distance >= prevDist

    def __addRouteToAlreadyExplored(self, positions, keysCollected, distance):
        if tuple(positions) not in self.__exploredKeySets:
            self.__exploredKeySets[tuple(positions)] = {}
        self.__exploredKeySets[tuple(positions)]["".join(sorted(keysCollected))] = distance

    def __buildGlobalMap(self):
        for sp in self.__startPos:
            self.__exploreFromThroughDoors(sp)
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
        positions = copy.deepcopy(self.__startPos)
        keysCollected = []
        keysToExplore = [(positions, keysCollected, 0)]
        stop = False
        depth = 0
        while not stop:
            print("At depth ", depth)
            depth += 1
            newKeysToExplore = []
            for (positions, keysCollected, dist) in keysToExplore:
                newKeysCollected = copy.deepcopy(keysCollected)
                noNewKeysFound = True
                for pos in positions:
                    if pos in self.__maze:
                        if self.__maze[pos] in self.__keysSet:
                            foundKey = self.__maze[pos]
                            if foundKey not in newKeysCollected:
                                newKeysCollected.append(foundKey)
                for posP in range(len(positions)):
                    pos = positions[posP]
                    newKeys = self.__findAccessibleKeysInGlobalMap(pos, newKeysCollected)
                    for k in newKeys:
                        noNewKeysFound = False
                        newPositions = copy.deepcopy(positions)
                        newPositions[posP] = self.__keysInMap[k]
                        newDist = dist + newKeys[k]
                        if not self.__routeAlreadyExplored(newPositions, newKeysCollected, newDist):
                            newKeysToExplore.append((newPositions, newKeysCollected, newDist))
                            self.__addRouteToAlreadyExplored(newPositions, newKeysCollected, newDist)
                if noNewKeysFound:
                    if True if minDistance is None else dist < minDistance:
                        minDistance = dist
                        bestRoute = newKeysCollected
            if len(newKeysToExplore) == 0:
                stop = True
            else:
                keysToExplore = newKeysToExplore
        return minDistance, bestRoute

    def solve(self):
        self.__buildGlobalMap()
        # self.__printGlobalMap()
        minDist, keysCollected = self.__buildRoutesWide()
        return minDist, keysCollected


