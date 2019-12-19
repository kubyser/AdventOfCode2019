import unittest
from MazeAndKeys import MazeAndKeys


class MazeAndKeysTestCase(unittest.TestCase):
    def test_simpleMaze1(self):
        m1 = ["#########",
              "#b.A.@.a#",
              "#########"]
        minDist, keysCollected = MazeAndKeys(m1).solve()
        self.assertEqual(8, minDist)
        self.assertEqual(['a', 'b'], keysCollected)

    def test_simpleMaze2(self):
        m2 = ["########################",
              "#f.D.E.e.C.b.A.@.a.B.c.#",
              "######################.#",
              "#d.....................#",
              "########################"]
        maze = MazeAndKeys(m2)
        minDist, keysCollected = maze.solve()
        self.assertEqual(86, minDist)
        self.assertEqual(['a', 'b', 'c', 'd', 'e', 'f'], keysCollected)

    def test_simpleMaze3(self):
        m3 = ["########################",
              "#...............b.C.D.f#",
              "#.######################",
              "#.....@.a.B.c.d.A.e.F.g#",
              "########################"]
        maze = MazeAndKeys(m3)
        minDist, keysCollected = maze.solve()
        self.assertEqual(132, minDist)
        self.assertEqual(['b', 'a', 'c', 'd', 'f', 'e', 'g'], keysCollected)

    def test_simpleMaze5(self):
        m5 = ["########################",
              "#@..............ac.GI.b#",
              "###d#e#f################",
              "###A#B#C################",
              "###g#h#i################",
              "########################"]
        minDist, keysCollected = MazeAndKeys(m5).solve()
        self.assertEqual(81, minDist)
        self.assertEqual(['a', 'c', 'f', 'i', 'd', 'g', 'b', 'e', 'h'],
                         keysCollected)

    def test_multimaze1(self):
        m6 = ["#######",
              "#a.#Cd#",
              "##@#@##",
              "#######",
              "##@#@##",
              "#cB#Ab#",
              "#######"]
        minDist, keysCollected = MazeAndKeys(m6).solve()
        self.assertEqual(8, minDist)

    def test_multimaze2(self):
        m7 = ["###############",
              "#d.ABC.#.....a#",
              "######@#@######",
              "###############",
              "######@#@######",
              "#b.....#.....c#",
              "###############"]
        minDist, keysCollected = MazeAndKeys(m7).solve()
        self.assertEqual(24, minDist)

    def test_multimaze3(self):
        m8 = ["#############",
              "#DcBa.#.GhKl#",
              "#.###@#@#I###",
              "#e#d#####j#k#",
              "###C#@#@###J#",
              "#fEbA.#.FgHi#",
              "#############"]
        minDist, keysCollected = MazeAndKeys(m8).solve()
        self.assertEqual(32, minDist)

    def test_multimaze4(self):
        m9 = ["#############",
              "#g#f.D#..h#l#",
              "#F###e#E###.#",
              "#dCba@#@BcIJ#",
              "#############",
              "#nK.L@#@G...#",
              "#M###N#H###.#",
              "#o#m..#i#jk.#",
              "#############"]
        minDist, keysCollected = MazeAndKeys(m9).solve()
        self.assertEqual(72, minDist)

    def test_multimaze5(self):
        m7 = ["###############",
              "#d.ABC.#.....a#",
              "######@#@######",
              "###############",
              "######@#@######",
              "#b.....#.....c#",
              "###############"]
        minDist, keysCollected = MazeAndKeys(m7).solve()
        self.assertEqual(24, minDist)


if __name__ == '__main__':
    unittest.main()
