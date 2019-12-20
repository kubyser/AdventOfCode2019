from TractorBeam import TractorBeam

def main():
    tractor = TractorBeam("day19_input.txt")
    # res = tractor.checkAtPosition((0,0))
    # print(res)
    # res = tractor.scanArea(200, 200, 700, 800)
    # tractor.printField()
    tractor.findSanta(10, 10, 1000, 1000)
    tractor.waitToClose()

if __name__ == "__main__":
    main()