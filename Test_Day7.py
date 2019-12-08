import unittest
from queue import Queue

from Day7 import IntComputer
from Day7 import IntComputerThread
from Day7 import readProgram
from Day7 import Chain
from Day7 import findMaxThrust


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

    def runSingleComputerThreaded(self, p, inValues):
        t = IntComputerThread(IntComputer(p, Queue(), Queue()))
        t.start()
        for x in inValues:
            t.computer.inQueue.put(x)
        t.join()
        outValues = []
        while not t.computer.outQueue.empty():
            outValues.append(t.computer.outQueue.get())
        return outValues

    def test_IntComputerThreadSingle(self):
        self.assertEqual(self.runSingleComputerThreaded([3,9,8,9,10,9,4,9,99,-1,8],[7]),[0])
        self.assertEqual(self.runSingleComputerThreaded([3,9,8,9,10,9,4,9,99,-1,8],[8]),[1])
        p = readProgram("day5_input.txt")
        self.assertEqual(self.runSingleComputerThreaded(p,[5]), [2369720])

    def test_chain(self):
        # no loop
        self.assertEqual(Chain([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],5,0,[4,3,2,1,0]).compute(), 43210)
        self.assertEqual(Chain([3,23,3,24,1002,24,10,24,1002,23,-1,23,
                                101,5,23,23,1,24,23,23,4,23,99,0,0], 5, 0, [0,1,2,3,4]).compute(), 54321)
        self.assertEqual(Chain([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                                1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], 5, 0, [1,0,4,3,2]).compute(), 65210)
        # loop
        self.assertEqual(Chain([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                                27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], 5, 0, [9,8,7,6,5], True).compute(), 139629729)
        self.assertEqual(Chain([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
                                -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
                                53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], 5, 0, [9,7,8,5,6], True).compute(), 18216)

    def test_day7(self):
        # part 1
        self.assertEqual(findMaxThrust([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], False),
                         ([4,3,2,1,0], 43210))
        self.assertEqual(findMaxThrust([3,23,3,24,1002,24,10,24,1002,23,-1,23,
                                        101,5,23,23,1,24,23,23,4,23,99,0,0], False),
                         ([0,1,2,3,4], 54321))
        self.assertEqual(findMaxThrust([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                                        1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], False),
                         ([1,0,4,3,2], 65210))
        p = readProgram("day7_input.txt")
        self.assertEqual(findMaxThrust(p, False), ([3, 4, 1, 2, 0], 359142))
        # part 2
        self.assertEqual(findMaxThrust([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                                        27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], True),
                         ([9,8,7,6,5], 139629729))
        self.assertEqual(findMaxThrust([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
                                        -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
                                        53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], True),
                         ([9,7,8,5,6], 18216))
        p = readProgram("day7_input.txt")
        self.assertEqual(findMaxThrust(p, True), ([9, 7, 8, 6, 5], 4374895))


if __name__ == '__main__':
    unittest.main()
