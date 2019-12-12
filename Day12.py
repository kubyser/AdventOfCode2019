from NBodySimulator import NBodySimulator

import math

def isPrime(n):
    if n < 2:
        return False
    for number in islice(count(2), int(sqrt(n) - 1)):
        if n % number == 0:
            return False
    return True

def main():
    b1 = [[-1, 0, 2],[2,-10,-7],[4,-8,8],[3,5,-1]]
    b2 = [[-8,-10,0],[5,5,10],[2,-7,3],[9,-8,-3]]
    testData = [[6,-2,-7],[-6,-7,-4],[-9,11,0],[-3,-4,6]]
    system = NBodySimulator(testData)
    numSteps = system.calculate(0, True)
#    for i in range(1000):
#        system.calculate()
#        print("After ", i+1, " steps:")
    for x in system.bodies:
        print("body =", x)
    print("Steps until repeated: ", numSteps)
    totalEnergy = system.calculateTotalEnergy()
    print("Total energy: ", totalEnergy)

def lcm(a,b): return abs(a * b) / math.gcd(a,b) if a and b else 0


def findRepetition():
    x = 135024
    y = 231614
    z = 102356
    xy = int(lcm(x,y))
    print(xy)
    xyz = int(lcm(xy,z))
    print(xyz)

if __name__ == '__main__':
    findRepetition()