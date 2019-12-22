class SpaceShuffle:

    def __init__(self, numCards):
        self.__deck = [0] * numCards
        for i in range(numCards):
            self.__deck[i] = i

    def getDeck(self):
        return self.__deck

    def dealIntoNewStack(self):
        self.__deck.reverse()
        return

    def cutNCards(self, n):
        tempDeck = self.__deck[n:]
        tempDeck += self.__deck[0:n]
        self.__deck = tempDeck

    def dealWithIncrementN(self, n):
        tempDeck = [None] * len(self.__deck)
        for i in range(len(self.__deck)):
            tempDeck[(i * n) % len(self.__deck)] = self.__deck[i]
        self.__deck = tempDeck

    def shuffleInstruction(self, instruction):
        knownCommands = {}
        knownCommands["deal into new stack"] = (False, self.dealIntoNewStack)
        knownCommands["cut"] = (True, self.cutNCards)
        knownCommands["deal with increment"] = (True, self.dealWithIncrementN)
        found = False
        for s in knownCommands:
            if len(instruction) >= len(s):
                if instruction[0:len(s)] == s:
                    found = True
                    if knownCommands[s][0]:
                        try:
                            arg = int(instruction[len(s) + 1 :])
                        except Exception as exc:
                            raise Exception("Numerical argument can't be parsed", instruction, exc)
                        knownCommands[s][1](arg)
                    else:
                        knownCommands[s][1]()
        if not found:
            raise Exception("Instruction not recognized", instruction)

    def runFromFile(self, fileName):
        f = open(fileName, "r")
        lines = f.read().splitlines()
        f.close()
        for s in lines:
            self.shuffleInstruction(s)

    def getPositionOfCard(self, card):
        return self.__deck.index(card)

