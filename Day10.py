from SkyMap import SkyMap

def main():
    m1 = ['.#..#',
         '.....',
         '#####',
         '....#',
         '...##']
    m2 = ['.#...',
          '.....',
          '...#.',
          '....#',
          '.....']
    f = open("day10_input.txt", "r")
    m = f.read().splitlines()
    f.close()
    s = SkyMap(m)
    bestAsteroid = s.findAsteroidWithMostVisible()
    print("Best: [", bestAsteroid.x, ",", bestAsteroid.y, "] : ", s.getVisibleAsteroidsCount(bestAsteroid), " visible asteroids")

if __name__ == '__main__':
    main()