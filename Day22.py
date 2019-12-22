from SpaceShuffle import SpaceShuffle

def main():
    ss = SpaceShuffle(10)
    print(ss.getDeck())
    # ss.runFromFile("day22_input.txt")
    # ss.dealIntoNewStack()
    ss.cutNCards(1)
    print(ss.getDeck())
    ss.dealWithIncrementN(3)
    print(ss.getDeck())
    ss.cutNCards(2)
    print(ss.getDeck())
    # print(ss.getPositionOfCard(2019))

if __name__ == "__main__":
    main()