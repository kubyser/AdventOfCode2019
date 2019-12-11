from HullPaintingRobot import HullPaintingRobot
from IntComputer import IntComputer

def main():
    p = IntComputer.readProgram("day11_input.txt")
#    p = [3,100,104,1,104,0,3,100,104,0,104,0,3,100,104,1,104,1,99]
    robot = HullPaintingRobot(p)
    robot.run()
    print("Done!")
    print("Number of visited spaces: ", len(robot.visited))
    print("Visited: ", robot.visited)


if __name__ == '__main__':
    main()