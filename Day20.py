from PortalsMaze import PortalsMaze

def main():
    f = open("day20_input.txt", "r")
    maze = PortalsMaze(f.read().splitlines())
    f.close()
    # maze.printMaze()
    minSteps, portals = maze.findPath()
    print("Route found! min steps = ", minSteps)
    print("Portals visited: ", portals)

if __name__ == "__main__":
    main()