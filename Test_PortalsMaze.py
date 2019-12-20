import unittest
from PortalsMaze import PortalsMaze

class PortalsMazeTestCase(unittest.TestCase):
    def test_maze1(self):
        f = open("day20_input_test1.txt", "r")
        maze = PortalsMaze(f.read().splitlines())
        f.close()
        minSteps, portals = maze.findPath()
        self.assertEqual(23, minSteps)
        self.assertEqual(['BC', 'DE', 'FG'], portals)

    def test_maze2(self):
        f = open("day20_input_test2.txt", "r")
        maze = PortalsMaze(f.read().splitlines())
        f.close()
        minSteps, portals = maze.findPath()
        self.assertEqual(58, minSteps)
        self.assertEqual(['AS', 'QG', 'BU', 'JO'], portals)

    def test_pt1(self):
        f = open("day20_input.txt", "r")
        maze = PortalsMaze(f.read().splitlines())
        f.close()
        minSteps, portals = maze.findPath()
        self.assertEqual(692, minSteps)
        self.assertEqual(['JY', 'QD', 'AN', 'VN', 'TG', 'JM', 'LF', 'BU', 'WJ', 'RX'], portals)


if __name__ == '__main__':
    unittest.main()
