import unittest
from SpaceShuffle import SpaceShuffle


class SpaceDeckTestCase(unittest.TestCase):
    def test_dealIntoNewStack(self):
        ss = SpaceShuffle(10)
        ss.dealIntoNewStack()
        self.assertEqual([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], ss.getDeck())

    def test_cutNCardsPositive(self):
        ss = SpaceShuffle(10)
        ss.cutNCards(3)
        self.assertEqual([3, 4, 5, 6, 7, 8, 9, 0, 1, 2], ss.getDeck())

    def test_cutNCardsNegative(self):
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

    def test_parseCutNCardsNegative(self):
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

    def test_reverseDealIntoNewStack(self):
        ss = SpaceShuffle(10, False)
        searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = ss.reverseDealIntoNewStack(searchPos)
        self.assertEqual([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], p)

    def test_reverseCutNCardsPositive(self):
        ss = SpaceShuffle(10, False)
        searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = ss.reverseCutNCards(searchPos, 3)
        self.assertEqual([3, 4, 5, 6, 7, 8, 9, 0, 1, 2], p)

    def test_reverseCutNCardsNegative(self):
        ss = SpaceShuffle(10, False)
        searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = ss.reverseCutNCards(searchPos, -4)
        self.assertEqual([6, 7, 8, 9, 0, 1, 2, 3, 4, 5], p)

    def test_reverseDealWithIncrementN(self):
        ss = SpaceShuffle(10, False)
        searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = ss.reverseDealWithIncrementN(searchPos, 3)
        self.assertEqual([0, 7, 4, 1, 8, 5, 2, 9, 6, 3], p)

    def test_reverseCombinedShuffle(self):
        ss = SpaceShuffle(10, False)
        searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = ss.reverseCutNCards(searchPos, -1)
        p = ss.reverseDealWithIncrementN(p, 3)
        p = ss.reverseDealWithIncrementN(p, 9)
        p = ss.reverseCutNCards(p, 3)
        p = ss.reverseDealWithIncrementN(p, 7)
        p = ss.reverseCutNCards(p, -4)
        p = ss.reverseCutNCards(p, 8)
        p = ss.reverseDealWithIncrementN(p, 7)
        p = ss.reverseCutNCards(p, -2)
        p = ss.reverseDealIntoNewStack(p)
        self.assertEqual([9, 2, 5, 8, 1, 4, 7, 0, 3, 6], p)

    def test_reverseParseDealIntoNewStack(self):
        ss = SpaceShuffle(10, False)
        searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = ss.reverseShuffleInstruction(searchPos, "deal into new stack")
        self.assertEqual([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], p)

    def test_reverseParseCutNCardsPositive(self):
        ss = SpaceShuffle(10, False)
        searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = ss.reverseShuffleInstruction(searchPos, "cut 3")
        self.assertEqual([3, 4, 5, 6, 7, 8, 9, 0, 1, 2], p)

    def test_reverseParseCutNCardsNegative(self):
        ss = SpaceShuffle(10, False)
        searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = ss.reverseShuffleInstruction(searchPos, "cut -4")
        self.assertEqual([6, 7, 8, 9, 0, 1, 2, 3, 4, 5], p)

    def test_reverseParseDealWithIncrementN(self):
        ss = SpaceShuffle(10, False)
        searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = ss.reverseShuffleInstruction(searchPos, "deal with increment 3")
        self.assertEqual([0, 7, 4, 1, 8, 5, 2, 9, 6, 3], p)

    def test_reverseShuffleFromFile(self):
        ss = SpaceShuffle(10, False)
        searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = ss.reverseRunFromFile(searchPos, "day22_input_test1.txt")
        self.assertEqual([9, 2, 5, 8, 1, 4, 7, 0, 3, 6], p)


if __name__ == '__main__':
    unittest.main()
