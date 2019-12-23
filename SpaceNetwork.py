from IntComputer import IntComputer, IntComputerThread
from queue import Queue, Empty

class SpaceNetwork:

    def __init__(self, numComputers, fileName):
        program = IntComputer.readProgram(fileName)
        self.__computers = []
        self.__inQueues = []
        self.__outQueues = []
        self.__natPackage = (None, None)
        for i in range(numComputers):
            inQueue = Queue()
            outQueue = Queue()
            self.__inQueues.append(inQueue)
            self.__outQueues.append(outQueue)
            computer = IntComputerThread(IntComputer(program, inQueue, outQueue, True, 0.1))
            self.__computers.append(computer)

    def __readValueOrNone(self, queue):
        try:
            a = queue.get(False)
            return a
        except Empty:
            return None

    def __sendPackage(self, dest, x, y):
        print("Sending to", dest, ": x =", x, " y =", y)
        if dest == 255:
            print("Destination 255!!!!")
            self.__natPackage = (x, y)
            return
        self.__computers[dest].lock.acquire()
        self.__inQueues[dest].put(x)
        self.__inQueues[dest].put(y)
        self.__computers[dest].lock.release()

    def run(self):
        print("Starting...")
        control = []
        lastYToZero = None
        for i in range(len(self.__computers)):
            print("Booting up computer", i)
            self.__inQueues[i].put(i)
            self.__computers[i].start()
            control.append([None, None, None])
        print("All computers booted up!")
        while True:
            active = False
            for i in range(len(self.__computers)):
                # print("Checking queue", i)
                outQueue = self.__outQueues[i]
                while not outQueue.empty():
                    active = True
                    # print("Not empty!")
                    for j in range(len(control[i])):
                        if control[i][j] is None:
                            control[i][j] = self.__readValueOrNone(outQueue)
                            if control[i][len(control[i])-1] is not None:
                                self.__sendPackage(control[i][0], control[i][1], control[i][2])
                                control[i][0] = None
                                control[i][1] = None
                                control[i][2] = None
                            break
            if not active and self.__natPackage[0] is not None:
                print("IDLE NETWORK! sending to 0 x=", self.__natPackage[0], "y=", self.__natPackage[1])
                self.__sendPackage(0, self.__natPackage[0], self.__natPackage[1])
                if self.__natPackage[1] == lastYToZero:
                    print("Sent same Y value twice to zero: ", lastYToZero)
                    input("Press Enter...")
                else:
                    lastYToZero = self.__natPackage[1]
                self.__natPackage = (None, None)




