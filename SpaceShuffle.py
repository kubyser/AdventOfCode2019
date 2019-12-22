class SpaceShuffle:

    def __init__(self, numCards, searchPos=0):
        self.__numCards = numCards
        self.__startPos = 0
        self.__directionMultiplier = 1
        self.__increment = 1
        self.__searchPos = searchPos

    def __getLoopedPos(self, p):
        if p >= self.__numCards:
            return p - self.__numCards
        elif p < 0:
            return self.__numCards + p
        else:
            return p

    def __getValueOfPos(self, pos):
        n = 0
        while (n * self.__numCards + pos) % self.__increment != 0:
            n += 1
        res = (n * self.__numCards + pos) // self.__increment
        return res

    def getDeckOld(self):
        p = self.__startPos
        res = []
        for i in range(self.__numCards):
            res.append(self.__getValueOfPos(p))
            p = self.__getLoopedPos(p+1)
        return res

    def getDeck(self):
        res = []
        values = {}
        for value in range(self.__numCards):

            pos = (self.__getLoopedPos(value - self.__startPos) * self.__increment) % self.__numCards + self.__startPos
            values[self.__getLoopedPos(pos - self.__startPos)] = value
        # print(values)
        for i in range(self.__numCards):
            res.append(values[i])
        return res


    def dealIntoNewStack(self):
        self.__startPos = self.__getLoopedPos(self.__startPos - self.__directionMultiplier * self.__increment)
        self.__directionMultiplier = -self.__directionMultiplier
        return

    def cutNCards(self, n):
        # self.__startPos = self.__getLoopedPos(self.__startPos + self.__directionMultiplier * self.__increment * n)
        self.__startPos = self.__getLoopedPos(self.__startPos + n)

    def dealWithIncrementN(self, n):
        self.__increment *= n

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


    def reverseDealWithIncrement(self, searchPos, increment):
        n = 0
        while (n * self.__numCards + searchPos) % increment != 0:
            n += 1
        prevPos = (n * self.__numCards + searchPos) // increment
        return
