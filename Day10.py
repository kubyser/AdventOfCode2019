from SkyMap import SkyMap

def main():
    f = open("day10_input.txt", "r")
    m = f.read().splitlines()
    f.close()
    s = SkyMap(m)
    bestAsteroid = s.findAsteroidWithMostVisible()
    print("Best: [", bestAsteroid.x, ",", bestAsteroid.y, "] : ", s.getVisibleAsteroidsCount(bestAsteroid), " visible asteroids")
    v = s.getVisibleSortedByAngles(bestAsteroid)
    i = 1
    for a in v:
        print("Kill ", i, " at [", a[0].x, ",", a[0].y, "], angle=", a[1])
        i+=1

if __name__ == '__main__':
    main()