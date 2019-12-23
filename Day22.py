from SpaceShuffle import SpaceShuffle

def main():
    ss1 = SpaceShuffle(119315717514047, False)
    # ss1 = SpaceShuffle(10007)
    # for i in range(10):
    #     ss1.runFromFile("day22_input.txt")
    # print(ss1.getDeck())
    # ss2 = SpaceShuffle(119315717514047, False)
    # commands = ss2.reorderFromFile("day22_input.txt", 101741582076661)
    # return
    # ss2.runFromList(commands)
    # print(ss2.getDeck())
    # return
    # searchPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    searchPos = 2020
    # 101,741,582,076,661
    # p = ss1.reverseRunFromFile(searchPos, "day22_input.txt", 101741582076661)
    p = ss1.reverseRunFromFile(searchPos, "day22_input_combined.txt")
    print("Final value at ", searchPos, "=", p)

if __name__ == "__main__":
    main()