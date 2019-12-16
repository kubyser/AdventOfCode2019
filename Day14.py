from NanoFactory import NanoFactory

def main():
    #p = ["10 ORE => 10 A","1 ORE => 1 B","7 A, 1 B => 1 C","7 A, 1 C => 1 D","7 A, 1 D => 1 E","7 A, 1 E => 1 FUEL"]
    p = open("day14_input.txt", "r").read().splitlines()
    factory = NanoFactory(p)
    factory.requestMaterial("FUEL", 3412429)
    res = factory.getRequiredAmountOf("ORE")
    print ("Done! Required amount of ore: ", res)

if __name__ == "__main__":
    main()