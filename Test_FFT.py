import unittest
from FlawedFrequencyTransmission import FFT

class FFTTestCase(unittest.TestCase):
    def test_processing(self):
        s1 = '12345678'
        res = FFT.processSignal(s1, 4)
        self.assertEqual("01029498", res)
        s1 = '80871224585914546619083218645595'
        res = FFT.processSignal(s1, 100, 8)
        self.assertEqual("24176176", res)
        s1 = '19617804207202209144916044189917'
        res = FFT.processSignal(s1, 100, 8)
        self.assertEqual("73745418", res)
        s1 = '69317163492948606335995924319873'
        res = FFT.processSignal(s1, 100, 8)
        self.assertEqual("52432133", res)


if __name__ == '__main__':
    unittest.main()
