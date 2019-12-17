class FFT:

    __pattern = (0, 1, 0, -1)


    @staticmethod
    def __processPhase(signal):
        outSignal = [0] * len(signal)
        for i in range(len(signal)):
            patSize = len(FFT.__pattern)
            longPatSize = patSize * (i+1)
            res = 0
            for j in range(len(signal)):
                modifierPos = ((j+1) % longPatSize) // (i+1)
                modifier = FFT.__pattern[modifierPos]
                value = signal[j] * modifier
                res += value
            outSignal[i] = abs(res) % 10
        return outSignal

    @staticmethod
    def processSignal(signal, numPhases, numReturnDigits = 0):
        signal = [int(char) for char in signal]
        for i in range(numPhases):
            signal = FFT.__processPhase(signal)
            #print("After ", i, " phase:", signal)
        if numReturnDigits > 0:
            signal = signal[:numReturnDigits]
        resStr = ""
        for x in signal:
            resStr += str(x)
        return resStr

    @staticmethod
    def processMultipliedSignal(signal, numPhases, numReturnDigits = 0):
        offset = int(signal[:7])
        signal = [int(char) for char in signal] * 100
        for i in range(numPhases):
            signal = FFT.__processPhase(signal)
            print("Done ", i, " phase")
        if numReturnDigits > 0:
            signal = signal[offset:offset+numReturnDigits]
        else:
            signal = signal[offset:]
        resStr = ""
        for x in signal:
            resStr += str(x)
        return resStr



