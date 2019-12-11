import unittest
from HullPaintingRobot import HullPaintingRobot
from IntComputer import IntComputer


class HullPaintingRobotTestCase(unittest.TestCase):
    def test_robot(self):
        robot = HullPaintingRobot([3,100,104,1,104,0,3,100,104,0,104,0,3,100,104,1,104,1,99])
        robot.run()
        self.assertEqual({(0, 0): 1, (-1, 0): 0, (-1, -1): 1}, robot.visited)

    def test_part1(self):
        p = IntComputer.readProgram("day11_input.txt")
        robot = HullPaintingRobot(p)
        robot.run()
        self.assertEqual(2343, len(robot.visited))

    def test_part2(self):
        p = IntComputer.readProgram("day11_input.txt")
        robot = HullPaintingRobot(p)
        robot.run(1)
        self.assertEqual(249, len(robot.visited))


if __name__ == '__main__':
    unittest.main()
