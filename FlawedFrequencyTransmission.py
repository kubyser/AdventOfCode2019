import time


class FFT:

    __pattern = (0, 1, 0, -1)


    @staticmethod
    def __processPhase(signal):
        lenSignal = len(signal)
        outSignal = [0] * lenSignal
        startTime = time.time()
        fullCalcCycles = 3
        fullCalc = True
        for i in range(lenSignal):
            if i == fullCalcCycles: #lenSignal / 64:
                fullCalc = False
            if fullCalc:
                res = 0
            stop = False
            startPlus = i
            segments = []
            while not stop:
                endPlus = startPlus + i+1
                startMinus = startPlus + (i+1)*2
                endMinus = startMinus + i+1
                if endMinus > lenSignal:
                    endMinus = lenSignal
                    if startMinus > lenSignal:
                        startMinus = lenSignal
                        if endPlus > lenSignal:
                            endPlus = lenSignal
                            if startPlus > lenSignal:
                                startPlus = lenSignal
                if not fullCalc or i == fullCalcCycles-1:
                    segments.append([startPlus, endPlus, startMinus, endMinus])
                if fullCalc:
                    res = res + sum(signal[startPlus:endPlus]) - sum(signal[startMinus:endMinus])
                startPlus += (i+1)*4
                if startPlus >= lenSignal:
                    stop = True
            if not fullCalc:
                for n in range(len(prevSegments)):
                    if n >= len(segments):
                        res -= sum(signal[prevSegments[n][0]:prevSegments[n][1]])
                        res += sum(signal[prevSegments[n][2]:prevSegments[n][3]])
                    else:
                        res -= sum(signal[prevSegments[n][0]:min(segments[n][0], prevSegments[n][1])])
                        res += sum(signal[max(prevSegments[n][1], segments[n][0]):segments[n][1]])
                        res += sum(signal[prevSegments[n][2]:min(segments[n][2], prevSegments[n][3])])
                        res -= sum(signal[max(prevSegments[n][3], segments[n][2]):segments[n][3]])
            outSignal[i] = abs(res) % 10
            prevSegments = segments
            #if i % 10000 == 0: print("Calculated ",i,"elements of",lenSignal)
        elapsedTime = time.time() - startTime
        print("Phase done. Elapsed time: ", elapsedTime)
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
        signal = [int(char) for char in signal] * 10000
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



