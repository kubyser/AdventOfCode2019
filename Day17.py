from ASCII import ASCII

def main():
    asc = ASCII("day17_input.txt", True)
    asc.sendToRobot("A,B,A,C,A,B,C,B,C,B")
    asc.sendToRobot("R,8,L,10,L,12,R,4")
    asc.sendToRobot("R,8,L,12,R,4,R,4")
    asc.sendToRobot("R,8,L,10,R,8")
    asc.sendToRobot("y")
    asc.run()
    #res = asc.calculateIntersectionsAlignment()
    #print("Alignment = ", res)
    asc.waitToClose()

if __name__ == "__main__":
    main()