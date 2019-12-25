from IntComputer import IntComputerAsciiTerminal, IntComputer

def main():
    comp = IntComputerAsciiTerminal(IntComputer.readProgram("day25_input.txt"))
    comp.run()

if __name__ == "__main__":
    main()