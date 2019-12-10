import math

class SkyMap:
    class Asteroid:
        def __init__(self, id, x, y):
            self.id = id
            self.x = x
            self.y = y
            self.hiddenAsteroidIds = []

    def areCollinear(self, a, b, c):
        eps = 0.0000001
        ab = math.sqrt((a.x-b.x)*(a.x-b.x) + (a.y - b.y)*(a.y - b.y))
        bc = math.sqrt((c.x-b.x)*(c.x-b.x) + (c.y - b.y)*(c.y - b.y))
        ac = math.sqrt((a.x-c.x)*(a.x-c.x) + (a.y - c.y)*(a.y - c.y))
        c1 = ab+bc
        c2 = ab+ac
        c3 = bc+ac
        return abs(ab+bc-ac)<eps  or abs(ab+ac - bc)<eps or abs(bc+ac - ab)<eps


    def findEdges(self, a, b, c):
        if (a.x - b.x) * (a.x - c.x) < 0:
            return b, c
        if (b.x - a.x) * (b.x - c.x) < 0:
            return a, c
        if (c.x - b.x) * (c.x - a.x) < 0:
            return a, b
        if (a.y - b.y) * (a.y - c.y) < 0:
            return b, c
        if (b.y - a.y) * (b.y - c.y) < 0:
            return a, c
        if (c.y - b.y) * (c.y - a.y) < 0:
            return a, b
        print("ERROR: can't find mid of three points")
        return None, None

    def getVisibleAsteroidsCount(self, a):
        t = len(self.asteroids)
        h = len(a.hiddenAsteroidIds)
        return len(self.asteroids) - len(a.hiddenAsteroidIds) - 1

    def getVisibleAsteroids(self, a):
        res = []
        for x in self.asteroids:
            if (x.id != a.id) and (x.id not in a.hiddenAsteroidIds):
                res.append(x)
        return res

    def findAsteroidWithMostVisible(self):
        maxVisible = 0
        res = None
        for x in self.asteroids:
            if self.getVisibleAsteroidsCount(x) > maxVisible:
                maxVisible = self.getVisibleAsteroidsCount(x)
                res = x
        return res

    def __init__(self, mapList):
        self.asteroids = []
        id = 0
        for x in range(len(mapList[0])):
            for y in range(len(mapList)):
                if mapList[y][x] == '#':
                    self.asteroids.append(self.Asteroid(id, x, y))
                    id += 1
        for i in range(len(self.asteroids) - 2):
            for j in range(i+1, len(self.asteroids) - 1):
                for k in range(j+1, len(self.asteroids)):
                    if self.areCollinear(self.asteroids[i], self.asteroids[j], self.asteroids[k]):
                        b, c = self.findEdges(self.asteroids[i], self.asteroids[j], self.asteroids[k])
                        if c.id not in b.hiddenAsteroidIds:
                            b.hiddenAsteroidIds.append(c.id)
                        if b.id not in c.hiddenAsteroidIds:
                            c.hiddenAsteroidIds.append(b.id)
