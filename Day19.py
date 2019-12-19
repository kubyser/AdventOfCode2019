from TractorBeam import TractorBeam

def main():
    tractor = TractorBeam("day19_input.txt")
    # res = tractor.checkAtPosition((0,0))
    # print(res)
    res = tractor.scanArea(50, 50)
    tractor.printField()
    print(res)

if __name__ == "__main__":
    main()