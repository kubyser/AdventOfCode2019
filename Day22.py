from SpaceShuffle import SpaceShuffle

def main():
    ss = SpaceShuffle(10007)
    # print(ss.getDeck())
    ss.runFromFile("day22_input.txt")
    print(ss.getDeck())
    print(ss.getPositionOfCard(2019))

if __name__ == "__main__":
    main()