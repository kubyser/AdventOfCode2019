from FlawedFrequencyTransmission import FFT

def main():
    s1 = open("day16_input.txt", "r").read()
    #s1 = "03036732577212944063491565474664"
    res = FFT.processMultipliedSignal(s1, 100, 8)
    #res = FFT.processSignal(s1, 4)
    print("Result: ", res)

if __name__ == '__main__':
    main()