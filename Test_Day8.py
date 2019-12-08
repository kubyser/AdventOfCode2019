import unittest

from Day8 import SpaceImageFormat
from Day8 import calcForLayersWithLessZeros

class SpaceImageFormatTestCase(unittest.TestCase):
    def test_part1(self):
        image = SpaceImageFormat("100012210012201212010102", 3, 2)
        self.assertEqual(calcForLayersWithLessZeros(image), 6)
        f = open("day8_input.txt", "r")
        s = f.read()
        f.close()
        image = SpaceImageFormat(s, 25, 6)
        res = calcForLayersWithLessZeros(image)
        self.assertEqual(res, 1806)

    def test_part2(self):
        image = SpaceImageFormat("120212210212201212010001", 3, 2)
        self.assertEqual("110011", image.bitmapToString())
        f = open("day8_input.txt", "r")
        s = f.read()
        f.close()
        image = SpaceImageFormat(s, 25, 6)
        self.assertEqual("001100110011110111000110000010100101000010010100100001010010111001001010010000101111010000111001111010010100101000010100100100110010010100001001010010",
                         image.bitmapToString())




if __name__ == '__main__':
    unittest.main()
