from IntComputer import IntComputer


def main():
    p = IntComputer.readProgram("day9_input.txt")
    comp = IntComputer(p)
    comp.compute()

if __name__ == '__main__':
    main()