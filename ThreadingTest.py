from queue import Queue
from threading import Thread

class Computer(Thread):

    def __init__(self, name, inQueue, outQueue):
        Thread.__init__(self)
        self.name = name
        self.inQueue = inQueue
        self.outQueue = outQueue

    def run(self):
        stop = False
        while not stop:
            print("Computer ", self.name, " at input")
            s = self.inQueue.get()
            print("Computer ", self.name, " read value: ", s)
            self.outQueue.put(s+1)
            if s > 100:
                stop = True

def main():
    queue = Queue()
    computers = []
    for x in range(5):
        computer = Computer(str(x), queue, Queue())
        queue = computer.outQueue
        computers.append(computer)
    computers[0].inQueue = computers[-1].outQueue
    for c in computers:
        c.start()
    s = int(input("Input value: "))
    computers[0].inQueue.put(s)
    print("Waiting for all threads to finish")
    for c in computers:
        c.join()
    res = computers[-1].outQueue.get()
    print("Done! Last result: ", res)

if __name__ == '__main__':
    main()
