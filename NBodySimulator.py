import copy

class Vector:
    def __init__(self, x, y, z):
        self.p = [x, y, z]

    def equals(self, b):
        for i in range(len(self.p)):
            if self.p[i] != b.p[i]:
                return False
        return True


class NBodySimulator:

    class Body:
        def __init__(self, pos):
            self.pos = pos
            self.speed = Vector(0, 0, 0)


        def applyGravityOf(self, b):
            for i in range(len(self.pos.p)):
                if self.pos.p[i] > b.pos.p[i]:
                    self.speed.p[i] -= 1
                elif self.pos.p[i] < b.pos.p[i]:
                    self.speed.p[i] += 1

        def applyVelocity(self):
            for i in range(len(self.pos.p)):
                self.pos.p[i] += self.speed.p[i]

    def calculateTotalEnergy(self):
        energy = 0
        for a in self.bodies:
            potential = 0
            kinetic = 0
            for i in range(len(a.pos.p)):
                potential += abs(a.pos.p[i])
                kinetic += abs(a.speed.p[i])
            energy += potential * kinetic
        return energy


    def __init__(self, bodiesPositions):
        self.bodies = []
        for body in bodiesPositions:
            x = body[0]
            y = body[1]
            z = body[2]
            self.bodies.append(self.Body(Vector(x, y, z)))
        self.initialBodies = copy.deepcopy(self.bodies)
        self.initialTotalEnergy = self.calculateTotalEnergy()

    def sameAsInitial(self):
        for i in range(len(self.bodies)):
            if not self.bodies[i].pos.equals(self.initialBodies[i].pos):
                return False
            if not self.bodies[i].speed.equals(self.initialBodies[i].speed):
                return False
        return True


    def calculate(self, steps = 1, stopWhenRepeats = False):
        i = 0
        while (i<steps) or ((steps == 0) and stopWhenRepeats):
            for a in self.bodies:
                for b in self.bodies:
                    if a == b:
                        continue
                    a.applyGravityOf(b)
            for a in self.bodies:
                a.applyVelocity()
            if stopWhenRepeats:
                if i % 100000 == 0:
                    print("Done ", i, " steps")
                if self.calculateTotalEnergy() == self.initialTotalEnergy:
                    print("Same total energy after ", i, " steps")
                if self.sameAsInitial():
                    return i+1
            i += 1
        return None






