import unittest

from Day8 import SpaceImageFormat
from Day8 import calcForLayersWithLessTransparents

class SpaceImageFormatTestCase(unittest.TestCase):
    def test_part1(self):
        image = SpaceImageFormat("100012210012201212010102", 3, 2)
        self.assertEqual(calcForLayersWithLessTransparents(image), 6)
        f = open("day8_input.txt", "r")
        s = f.read()
        f.close()
        image = SpaceImageFormat(s, 25, 6)
        res = calcForLayersWithLessTransparents(image)
        self.assertEqual(res, 1806)


if __name__ == '__main__':
    unittest.main()
