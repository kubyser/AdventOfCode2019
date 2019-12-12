import unittest
from NBodySimulator import NBodySimulator

class NBodySimulatorTestCase(unittest.TestCase):
    def test_NBody_calculations(self):
        b1 = [[-1, 0, 2],[2,-10,-7],[4,-8,8],[3,5,-1]]
        system = NBodySimulator(b1)
        system.calculate(10)
        totalEnergy = system.calculateTotalEnergy()
        self.assertEqual(179, totalEnergy)
        b2 = [[-8,-10,0],[5,5,10],[2,-7,3],[9,-8,-3]]
        system = NBodySimulator(b1)
        system.calculate(10)
        totalEnergy = system.calculateTotalEnergy()
        self.assertEqual(1940, totalEnergy)

if __name__ == '__main__':
    unittest.main()
