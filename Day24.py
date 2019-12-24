from BugsWorld import BugsWorld

def main():
    p1 = ["....#",
          "#..#.",
          "#..##",
          "..#..",
          "#...."]
    f = open("day24_input.txt", "r")
    p = f.read().splitlines()
    f.close()
    bw = BugsWorld(5, 5, True, False)
    bw.readField(p)
    # bw.drawField()
    bw.printField()
    bw.run(200, False)
    bw.printField()
    print("Biodiversity=", bw.getBiodiversity())
    print("Number of bugs:", bw.getNumBugs())
    # bw.waitToClose()

if __name__ == "__main__":
    main()