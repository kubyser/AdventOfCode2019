class SpaceShuffle:

    def __init__(self, numCards, createDeck=True):
        self.__numCards = numCards
        if createDeck:
            self.__deck = [0] * numCards
            for i in range(numCards):
                self.__deck[i] = i

    @staticmethod
    def extended_gcd(aa, bb):
        lastremainder, remainder = abs(aa), abs(bb)
        x, lastx, y, lasty = 0, 1, 1, 0
        while remainder:
            lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
            x, lastx = lastx - quotient*x, x
            y, lasty = lasty - quotient*y, y
        return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

    @staticmethod
    def modinv(a, m):
        g, x, y = SpaceShuffle.extended_gcd(a, m)
        if g != 1:
            raise ValueError
        return x % m

    def __getLoopedPos(self, p):
        if p >= self.__numCards:
            return p - self.__numCards
        elif p < 0:
            return self.__numCards + p
        else:
            return p

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

    def runFromList(self, commands):
        for s in commands:
            self.shuffleInstruction(s)


    def getPositionOfCard(self, card):
        return self.__deck.index(card)


    def reverseDealIntoNewStack(self, searchPos):
        if isinstance(searchPos, list):
            return [self.__numCards - x - 1 for x in searchPos]
        else:
            return self.__numCards - searchPos - 1

    def reverseCutNCards(self, searchPos, n):
        if isinstance(searchPos, list):
            return [self.__getLoopedPos(x + n) for x in searchPos]
        else:
            return self.__getLoopedPos(searchPos + n)

    def solveCogruence(self, pos, inc):
        r = SpaceShuffle.modinv(self.__numCards, inc)
        m = r*(inc - (pos % inc))
        d = m % inc
        return d

    def reverseDealWithIncrementN(self, searchPos, increment):
        if isinstance(searchPos, list):
            res = []
            for x in searchPos:
                n = self.solveCogruence(x, increment)
                res.append((n * self.__numCards + x) // increment)
            return res
        else:
            n = self.solveCogruence(searchPos, increment)
            return (n * self.__numCards + searchPos) // increment

    def reverseShuffleInstruction(self, searchPos, instruction):
        knownCommands = {}
        knownCommands["deal into new stack"] = (False, self.reverseDealIntoNewStack)
        knownCommands["cut"] = (True, self.reverseCutNCards)
        knownCommands["deal with increment"] = (True, self.reverseDealWithIncrementN)
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
                        return knownCommands[s][1](searchPos, arg)
                    else:
                        return knownCommands[s][1](searchPos)
        if not found:
            raise Exception("Instruction not recognized", instruction)

    def reverseRunFromFile(self, searchPos, fileName, repeatTimes=1):
        f = open(fileName, "r")
        lines = f.read().splitlines()
        lines.reverse()
        f.close()
        res = searchPos
        for i in range(repeatTimes):
            for s in lines:
                res = self.reverseShuffleInstruction(res, s)
        return res

    def reorderFromList(self, commands):
        while True:
            found = False
            i = 0
            while i < len(commands)-1:
                if commands[i][0] == commands[i+1][0]:
                    found = True
                    if commands[i][0] == "deal into new stack":
                        commands.pop(i)
                        commands.pop(i)
                    elif commands[i][0] == "cut":
                        newCommand = ("cut",(commands[i][1] + commands[i+1][1]) % self.__numCards)
                        commands[i] = newCommand
                        commands.pop(i+1)
                    elif commands[i][0] == "deal with increment":
                        newCommand = ("deal with increment",(commands[i][1] * commands[i+1][1]) % self.__numCards)
                        commands[i] = newCommand
                        commands.pop(i+1)
                    else:
                        raise Exception("Unknown command during reordering")
                elif commands[i][0] == "deal into new stack" and commands[i+1][0] == "cut":
                    found = True
                    newCommand = ("cut", self.__numCards - commands[i+1][1])
                    commands[i] = newCommand
                    commands[i+1] = ("deal into new stack", None)
                    i += 1
                elif commands[i][0] == "cut" and commands[i+1][0] == "deal with increment":
                    found = True
                    newCommand = ("cut", (commands[i][1] * commands[i+1][1]) % self.__numCards)
                    commands[i] = commands[i+1]
                    commands[i+1] = newCommand
                    i += 1
                elif commands[i][0] == "deal into new stack" and commands[i+1][0] == "deal with increment":
                    found = True
                    # newCommand = ("cut", -(commands[i+1][1]-1) + self.__numCards + 1 - commands[i+1][1])
                    newCommand = ("cut", self.__numCards + 1 - commands[i+1][1])
                    commands[i] = commands[i+1]
                    commands[i+1] = newCommand
                    commands.insert(i+2, ("deal into new stack", None))
                    i += 2
                else:
                    i += 1
            if not found:
                break
        return commands

    def combineNTimes(self, commands, n):
        if n == 1:
            return commands
        newCommands = commands * 2
        combined = self.reorderFromList(newCommands)
        res = self.combineNTimes(combined, n // 2)
        if n % 2 != 0:
            res += commands
            return self.reorderFromList(res)
        else:
            return res

    def reorderFromFile(self, fileName, times=1):
        commands = []
        f = open(fileName, "r")
        lines = f.read().splitlines()
        knownCommands = {}
        knownCommands["deal into new stack"] = (False, self.reverseDealIntoNewStack, "d")
        knownCommands["cut"] = (True, self.reverseCutNCards, "c")
        knownCommands["deal with increment"] = (True, self.reverseDealWithIncrementN, "i")
        for instruction in lines:
            for s in knownCommands:
                if len(instruction) >= len(s):
                    if instruction[0:len(s)] == s:
                        if knownCommands[s][0]:
                            try:
                                arg = int(instruction[len(s) + 1:])
                            except Exception as exc:
                                raise Exception("Numerical argument can't be parsed", instruction, exc)
                            commands.append((s, arg))
                        else:
                            commands.append((s, None))
        print(commands)
        commands = self.reorderFromList(commands)
        if times > 1:
            commands = self.combineNTimes(commands, times)
        res = []
        for c in commands:
            if c[0] == "deal into new stack":
                res.append("deal into new stack")
            elif c[0] == "cut":
                res.append("cut " + str(c[1]))
            elif c[0] == "deal with increment":
                res.append("deal with increment " + str(c[1]))
            else:
                raise Exception("Unknown command during reordering")
        print(res)
        # for c in res:             print(c)
        return res

