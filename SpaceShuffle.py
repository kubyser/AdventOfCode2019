class SpaceShuffle:

    class Card:
        def __init__(self, value, prev, next):
            self.value = value
            self.prev = prev
            self.next = next


    def __init__(self, numCards):
        self.__numCards = numCards
        self.__deck = {}
        self.__directionRight = True
        for i in range(numCards):
            card = self.Card(i, None, None)
            if i > 0:
                card.prev = self.__deck[i-1]
                self.__deck[i-1].next = card
            self.__deck[i] = card
        self.__deck[0].prev = self.__deck[numCards-1]
        self.__deck[numCards-1].next = self.__deck[0]
        self.__startCard = self.__deck[0]
        self.__startPos = 0


    def __getLoopedPos(self, p):
            if p >= self.__numCards:
                return p - self.__numCards
            elif p < 0:
                return self.__numCards + p
            else:
                return p

    def __move(self, p, n):
        res = p
        absN = abs(n)
        direction = self.__directionRight if n>=0 else not self.__directionRight
        for i in range(absN):
            res = res.next if direction else res.prev
        return res

    def getDeck(self):
        p = self.__startCard
        res = []
        for i in range(self.__numCards):
            res.append(p.value)
            p = self.__move(p, 1)
        return res

    def dealIntoNewStack(self):
        self.__startCard = self.__startCard.prev if self.__directionRight else self.__startCard.next
        self.__startPos + 1 if not self.__directionRight else -1
        self.__directionRight = not self.__directionRight

    def cutNCards(self, n):
        # self.__startPos = self.__getLoopedPos(self.__startPos + self.__directionMultiplier * self.__increment * n)
        self.__startCard = self.__move( self.__startCard, n)
        self.__startPos = self.__getLoopedPos(self.__startPos + (n * 1 if self.__directionRight else -1))

    def dealWithIncrementN(self, n):
        p = self.__startCard
        newDeck = {}
        for i in range(self.__numCards):
            newPos = self.__getLoopedPos(self.__startPos + ((i * n) % self.__numCards) *
                                         (1 if self.__directionRight else -1))
            newCard = self.Card(p.value, None, None)
            newDeck[newPos] = newCard
            if self.__getLoopedPos(newPos-1) in newDeck:
                newDeck[self.__getLoopedPos(newPos-1)].next = newCard
                newCard.prev = newDeck[self.__getLoopedPos(newPos-1)]
            if self.__getLoopedPos(newPos+1) in newDeck:
                newDeck[self.__getLoopedPos(newPos+1)].prev = newCard
                newCard.next = newDeck[self.__getLoopedPos(newPos+1)]
            p = self.__move(p, 1)
        self.__deck = newDeck
        self.__startCard = newDeck[self.__startPos]


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
        p = self.__startCard
        for i in range(self.__numCards):
            if p.value == card:
                return i
            p = self.__move(p, 1)
        return None

