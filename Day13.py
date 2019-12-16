from ArcadeCabinet import ArcadeCabinet
from IntComputer import IntComputer

def printField(field):
    for i in field.keys():
        print("(",i[0],',',i[1],"): ", field[i])

def main():
    p = IntComputer.readProgram("day13_input.txt")
    cab = ArcadeCabinet(p)
    cab.run()
    print("Done.")
    #printField(cab.field)
    print("Number of block (2) tiles: ", cab.getNumTiles(2))
    #cab.drawField()

if __name__ == '__main__':
    main()