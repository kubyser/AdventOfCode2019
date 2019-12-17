from ASCII import ASCII

def main():
    asc = ASCII("day17_input.txt")
    asc.run()
    res = asc.calculateIntersectionsAlignment()
    print("Alignment = ", res)
    asc.waitToClose()

if __name__ == "__main__":
    main()