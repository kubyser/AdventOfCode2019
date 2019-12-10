import unittest
from SkyMap import SkyMap

def readLinesFromFile(name):
    f = open(name, "r")
    m = f.read().splitlines()
    f.close()
    return m

class SkyMapTestCase(unittest.TestCase):
    def test_skymap(self):
        m1 = ['.#..#',
              '.....',
              '#####',
              '....#',
              '...##']
        s = SkyMap(m1)
        res = [(0,2,6),(1,0,7),(1,2,7),(2,2,7),(3,2,7),(3,4,8),(4,0,7),(4,2,5),(4,3,7),(4,4,7)]
        self.assertEqual(len(res), len(s.asteroids))
        for i in range(len(s.asteroids)):
            self.assertEqual(res[i], (s.asteroids[i].x, s.asteroids[i].y, s.getVisibleAsteroidsCount(s.asteroids[i])))
        s = SkyMap(readLinesFromFile("day10_input_test1.txt"))
        b = s.findAsteroidWithMostVisible()
        self.assertEqual((5,8,33), (b.x, b.y, s.getVisibleAsteroidsCount(b)))
        s = SkyMap(readLinesFromFile("day10_input_test2.txt"))
        b = s.findAsteroidWithMostVisible()
        self.assertEqual((1,2,35), (b.x, b.y, s.getVisibleAsteroidsCount(b)))
        s = SkyMap(readLinesFromFile("day10_input_test3.txt"))
        b = s.findAsteroidWithMostVisible()
        self.assertEqual((6,3,41), (b.x, b.y, s.getVisibleAsteroidsCount(b)))
        s = SkyMap(readLinesFromFile("day10_input_test4.txt"))
        b = s.findAsteroidWithMostVisible()
        self.assertEqual((11,13,210), (b.x, b.y, s.getVisibleAsteroidsCount(b)))


if __name__ == '__main__':
    unittest.main()
