class Body:
    def __init__(self, name, sun, moons, depth):
        self.name = name
        self.sun = sun
        self.moons = moons
        self.depth = depth

def readInputData():
    f = open("day6_input.txt")
    s = f.read().splitlines()
    f.close()
    return s

def buildUniverse(p):
    universe = {}
    for s in p:
        s = s.split(")")
        if s[1] in universe:
            body = universe[s[1]]
            if body.sun is not None:
                print("ERROR: sun not null on existing body: ", s[1])
                return {}
        else:
            body = Body(s[1], None, [], 0)
            universe[body.name] = body
        if s[0] in universe:
            sun = universe[s[0]]
        else:
            sun = Body(s[0], None, [], 0)
            universe[sun.name] = sun
        body.sun = sun
        sun.moons.append(body)
    return universe


def calcDepth(root):
    for x in root.moons:
        x.depth = root.depth + 1
        calcDepth(x)

def printUniverse(universe):
    for b in universe.values():
        print(b.name)
        print("Depth: ", b.depth)
        print("Sun: ", b.sun.name if b.sun is not None else "NONE")
        print("Moons:")
        for m in b.moons:
            print(m.name)
        print ("---")

def distGoingUp(src, dest, skip = None):
    if src.name == dest.name:
        return 0
    for x in src.moons:
        if x == skip:
            continue
        r = distGoingUp(x, dest)
        if r is not None:
            return r+1
    return None

def findRoute(src, dest, skip = None):
    dUp = distGoingUp(src, dest, skip)
    if dUp is not None:
        return dUp
    if src.sun is None:
        print("ERROR: reached the COM and still not found")
        return None
    return findRoute(src.sun, dest, src) + 1

# ============================================

p = readInputData()
universe = buildUniverse(p)
print("Done building the universe")
#printUniverse(universe)

calcDepth(universe["COM"])
print("Done calculating orbit depths")

sum = 0
for b in universe.values():
    sum = sum + b.depth
print("Sum of orbit depths: ", sum)

src = universe["YOU"].sun
dest = universe["SAN"].sun
d = findRoute(src, dest)
print("Orbit transfers from YOU to SAN: ", d)

