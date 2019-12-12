from NBodySimulator import NBodySimulator

def main():
    b1 = [[-1, 0, 2],[2,-10,-7],[4,-8,8],[3,5,-1]]
    b2 = [[-8,-10,0],[5,5,10],[2,-7,3],[9,-8,-3]]
    testData = [[6,-2,-7],[-6,-7,-4],[-9,11,0],[-3,-4,6]]
    system = NBodySimulator(testData)
    system.calculate(1000)
#    for i in range(1000):
#        system.calculate()
#        print("After ", i+1, " steps:")
#        for x in system.bodies:
#            print("pos = ", x.pos.p, "    vel=", x.speed.p)
    totalEnergy = system.calculateTotalEnergy()
    print("Total energy: ", totalEnergy)

if __name__ == '__main__':
    main()