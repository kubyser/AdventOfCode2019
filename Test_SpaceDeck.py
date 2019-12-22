import unittest
from SpaceShuffle import SpaceShuffle


class SpaceDeckTestCase(unittest.TestCase):
    def test_dealIntotoNewStack(self):
        ss = SpaceShuffle(10)
        ss.dealIntoNewStack()
        self.assertEqual([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], ss.getDeck())

    def test_cutNCardsPositive(self):
        ss = SpaceShuffle(10)
        ss.cutNCards(3)
        self.assertEqual([3, 4, 5, 6, 7, 8, 9, 0, 1, 2], ss.getDeck())

    def test_cutNCardsNrgative(self):
        ss = SpaceShuffle(10)
        ss.cutNCards(-4)
        self.assertEqual([6, 7, 8, 9, 0, 1, 2, 3, 4, 5], ss.getDeck())

    def test_dealWithIncrementN(self):
        ss = SpaceShuffle(10)
        ss.dealWithIncrementN(3)
        self.assertEqual([0, 7, 4, 1, 8, 5, 2, 9, 6, 3], ss.getDeck())

    def test_combinedShuffle(self):
        ss = SpaceShuffle(10)
        ss.dealIntoNewStack()
        ss.cutNCards(-2)
        ss.dealWithIncrementN(7)
        ss.cutNCards(8)
        ss.cutNCards(-4)
        ss.dealWithIncrementN(7)
        ss.cutNCards(3)
        ss.dealWithIncrementN(9)
        ss.dealWithIncrementN(3)
        ss.cutNCards(-1)
        self.assertEqual([9, 2, 5, 8, 1, 4, 7, 0, 3, 6], ss.getDeck())

    def test_parseDealIntotoNewStack(self):
        ss = SpaceShuffle(10)
        ss.shuffleInstruction("deal into new stack")
        self.assertEqual([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], ss.getDeck())

    def test_parseCutNCardsPositive(self):
        ss = SpaceShuffle(10)
        ss.shuffleInstruction("cut 3")
        self.assertEqual([3, 4, 5, 6, 7, 8, 9, 0, 1, 2], ss.getDeck())

    def test_parseCutNCardsNrgative(self):
        ss = SpaceShuffle(10)
        ss.shuffleInstruction("cut -4")
        self.assertEqual([6, 7, 8, 9, 0, 1, 2, 3, 4, 5], ss.getDeck())

    def test_parseDealWithIncrementN(self):
        ss = SpaceShuffle(10)
        ss.shuffleInstruction("deal with increment 3")
        self.assertEqual([0, 7, 4, 1, 8, 5, 2, 9, 6, 3], ss.getDeck())

    def test_shuffleFromFile(self):
        ss = SpaceShuffle(10)
        ss.runFromFile("day22_input_test1.txt")
        self.assertEqual([9, 2, 5, 8, 1, 4, 7, 0, 3, 6], ss.getDeck())


if __name__ == '__main__':
    unittest.main()
