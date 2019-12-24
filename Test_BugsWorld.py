import unittest
from BugsWorld import BugsWorld

class BugsWorldTestCase(unittest.TestCase):
    def test_pt1(self):
        f = open("day24_input.txt", "r")
        p = f.read().splitlines()
        f.close()
        bw = BugsWorld(5, 5, False, False)
        bw.readField(p)
        bw.run(0, True)
        self.assertEqual(2130474, bw.getBiodiversity())
        self.assertEqual(6, bw.getNumBugs())

    def test_limitedRun(self):
        p = ["..#..",
             "##..#",
             "##...",
             "#####",
             ".#.##"]
        bw = BugsWorld(5, 5, False, False)
        bw.readField(p)
        bw.run(12, False)
        self.assertEqual(32233453, bw.getBiodiversity())
        self.assertEqual(19, bw.getNumBugs())

    def test_recursive(self):
        p1 = ["....#",
              "#..#.",
              "#..##",
              "..#..",
              "#...."]
        bw = BugsWorld(5, 5, True, False)
        bw.readField(p1)
        bw.run(10, False)
        self.assertEqual(124455948, bw.getBiodiversity())
        self.assertEqual(99, bw.getNumBugs())

    def test_pt2(self):
        f = open("day24_input.txt", "r")
        p = f.read().splitlines()
        f.close()
        bw = BugsWorld(5, 5, True, False)
        bw.readField(p)
        bw.run(200, False)
        self.assertEqual(3005334292, bw.getBiodiversity())
        self.assertEqual(1923, bw.getNumBugs())



if __name__ == '__main__':
    unittest.main()
