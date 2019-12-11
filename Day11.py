from HullPaintingRobot import HullPaintingRobot
from IntComputer import IntComputer

def printRobotMessage(res):
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    for a in res.keys():
        if a[0] < minX:
            minX = a[0]
        elif a[0] > maxX:
            maxX = a[0]
        if a[1] < minY:
            minY = a[1]
        elif a[1] > maxY:
            maxY = a[1]
    for j in range(0, maxY - minY + 1):
        line = ''
        for i in range(0, maxX - minX + 1):
            if (i+minX, maxY-j) in res:
                c = res[(i+minX, maxY-j)]
            else:
                c = 0
            line = line + ('#' if c == 1 else ' ')
        print(line)


def main():
    p = [3,100,104,1,104,0,
         3,100,104,0,104,0,
         3,100,104,1,104,0,
         3,100,104,1,104,1,99]
    p = IntComputer.readProgram("day11_input.txt")
    robot = HullPaintingRobot(p)
    robot.run(1)
    print("Done!")
    print("Number of visited spaces: ", len(robot.visited))
#    print(robot.visited)
    printRobotMessage(robot.visited)


if __name__ == '__main__':
    main()