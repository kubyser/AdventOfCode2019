from SpaceShuffle import SpaceShuffle

def main():
    ss = SpaceShuffle(119315717514047)
    # print(ss.getDeck())
    ss.runFromFile("day22_input.txt")
    print(ss.getPositionOfCard(2019))
    return
    ss.cutNCards(2)
    print(ss.getDeck())
    ss.dealIntoNewStack()
    print(ss.getDeck())
    ss.dealWithIncrementN(3)
    print(ss.getDeck())
    ss.cutNCards(2)
    print(ss.getDeck())

if __name__ == "__main__":
    main()