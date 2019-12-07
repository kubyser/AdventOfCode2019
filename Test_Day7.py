import unittest
from queue import Queue

from Day7 import IntComputer
from Day7 import readProgram

class IntComputerTestCase(unittest.TestCase):

    def test_single_computer(self):
        p = [2,4,4,5,99,0]
        comp = IntComputer(p)
        comp.compute()
        self.assertEqual(comp.program, [2,4,4,5,99,9801])
        comp = IntComputer([1,1,1,4,99,5,6,0,99])
        comp.compute()
        self.assertEqual(comp.program, [30,1,1,4,2,5,6,0,99])

    def test_day2(self):
        p = [1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,23,6,27,2,9,27,31,1,5,31,35,1,35,10,39,1,39,10,43,2,
             43,9,47,1,6,47,51,2,51,6,55,1,5,55,59,2,59,10,63,1,9,63,67,1,9,67,71,2,71,6,75,1,5,75,79,1,5,79,83,1,9,83,
             87,2,87,10,91,2,10,91,95,1,95,9,99,2,99,9,103,2,10,103,107,2,9,107,111,1,111,5,115,1,115,2,119,1,119,6,0,
             99,2,0,14,0]
        comp = IntComputer(p)
        comp.compute()
        self.assertEqual(comp.program[0], 3516593)
        p = [1,77,49,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,23,6,27,2,9,27,31,1,5,31,35,1,35,10,39,1,39,10,43,2,
             43,9,47,1,6,47,51,2,51,6,55,1,5,55,59,2,59,10,63,1,9,63,67,1,9,67,71,2,71,6,75,1,5,75,79,1,5,79,83,1,9,83,
             87,2,87,10,91,2,10,91,95,1,95,9,99,2,99,9,103,2,10,103,107,2,9,107,111,1,111,5,115,1,115,2,119,1,119,6,0,
             99,2,0,14,0]
        comp = IntComputer(p)
        comp.compute()
        self.assertEqual(comp.program[0], 19690720)

    def runSingleComputer(self, p, inValues):
        comp = IntComputer(p, Queue(), Queue())
        for x in inValues:
            comp.inQueue.put(x)
        comp.compute()
        outValues = []
        while not comp.outQueue.empty():
            outValues.append(comp.outQueue.get())
        return outValues

    def test_day5(self):
        p = readProgram("day5_input.txt")
        res = self.runSingleComputer(p, [1])
        self.assertEqual(res[-1], 13933662)
        self.assertEqual(self.runSingleComputer([3,9,8,9,10,9,4,9,99,-1,8], [7]), [0])
        self.assertEqual(self.runSingleComputer([3,9,8,9,10,9,4,9,99,-1,8], [8]), [1])
        self.assertEqual(self.runSingleComputer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],[0]),[0])
        self.assertEqual(self.runSingleComputer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],[-5]),[1])
        self.assertEqual(self.runSingleComputer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1],[0]),[0])
        self.assertEqual(self.runSingleComputer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1],[222]),[1])
        p = readProgram("day5_input.txt")
        self.assertEqual(self.runSingleComputer(p,[5]), [2369720])


if __name__ == '__main__':
    unittest.main()
