from RepairDroid import RepairDroid
from IntComputer import IntComputer

def main():
    p = IntComputer.readProgram("day15_input.txt")
    #p1 = [3,100,104,1,3,100,104,1,3,100,104,1,3,100,104,1,3,100,104,1,3,100,104,2,1105,1,0,99]
    droid = RepairDroid(p)
    res = droid.explore()
    droid.printField()
    if res != None:
        print("All done! Distance to oxygen tank=", res)
    minutes = droid.calculateTimeToFillWithOxygen()
    droid.printField()
    print("Minutes to fill with oxygen: ", minutes)


if __name__ == '__main__':
    main()