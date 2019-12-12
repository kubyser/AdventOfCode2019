import copy

class NBodySimulator:

    class Body:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

            self.vx = 0
            self.vy = 0
            self.vz = 0

        def equals(self, b):
            return (self.x, self.y, self.z, self.vx, self.vy, self.vz) == (b.x, b.y, b.z, b.vx, b.vy, b.vz)

        def applyGravityOf(self, b, mutual=False):
            ax = 1 if self.x < b.x else -1 if self.x > b.x else 0
            ay = 1 if self.y < b.y else -1 if self.y > b.y else 0
            az = 1 if self.z < b.z else -1 if self.z > b.z else 0
            self.vx += ax
            self.vy += ay
            self.vz += az
            if mutual:
                b.vx -= ax
                b.vy -= ay
                b.vz -= az


        def applyVelocity(self):
            self.x += self.vx
            self.y += self.vy
            self.z += self.vz

    def calculateTotalEnergy(self):
        energy = 0
        for a in self.bodies:
            potential = abs(a.x) + abs(a.y) + abs(a.z)
            kinetic = abs(a.vx) + abs(a.vy) + abs(a.vz)
            energy += potential * kinetic
        return energy


    def __init__(self, bodiesPositions):
        self.bodies = []
        for body in bodiesPositions:
            x = body[0]
            y = body[1]
            z = body[2]
            self.bodies.append(self.Body(x, y, z))
        self.initialBodies = copy.deepcopy(self.bodies)
        self.initialTotalEnergy = self.calculateTotalEnergy()
        self.numBodies = len(self.bodies)

    def sameAsInitial(self, axis = None):
        for i in range(self.numBodies):
            if axis is None:
                if not self.bodies[i].equals(self.initialBodies[i]):
                    return False
            elif axis == 0:
                if self.bodies[i].x != self.initialBodies[i].x:
                    return False
                if self.bodies[i].vx != self.initialBodies[i].vx:
                    return False
            elif axis == 1:
                if self.bodies[i].y != self.initialBodies[i].y:
                    return False
                if self.bodies[i].vy != self.initialBodies[i].vy:
                    return False
            elif axis == 2:
                if self.bodies[i].z != self.initialBodies[i].z:
                    return False
                if self.bodies[i].vz != self.initialBodies[i].vz:
                    return False
        return True


    def calculate(self, steps = 1, stopWhenRepeats = False):
        i = 0
        fx = False
        fy = False
        fz = False
        while (i<steps) or ((steps == 0) and stopWhenRepeats):
            for a in range(self.numBodies-1):
                for b in range(a+1, self.numBodies):
                    self.bodies[a].applyGravityOf(self.bodies[b], True)
            for a in self.bodies:
                a.applyVelocity()
            if stopWhenRepeats:
                if i % 100000 == 0:
                    print("Done ", i, " steps")
                if self.sameAsInitial() or (fx and fy and fz):
                    return i+1
                if not fx and self.sameAsInitial(0):
                    print("repeat X: ", i+1)
                    fx = True
                if not fy and self.sameAsInitial(1):
                    print("repeat Y: ", i+1)
                    fy = True
                if not fz and self.sameAsInitial(2):
                    print("repeat Z: ", i+1)
                    fz = True
            i += 1
        return None






